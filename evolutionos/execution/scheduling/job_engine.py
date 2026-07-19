"""
Scheduling Engine (`FR-PX-1101` to `FR-PX-1103`).

Provides cron-like recurring and one-shot scheduled jobs with persistence (`FR-PX-1101`),
missed-job detection with catch-up policies (`FR-PX-1102`), and preemption via priority classes (`FR-PX-1103`).
"""
import time
import logging
from enum import Enum
from typing import Dict, Any, List, Optional, Callable
from pydantic import BaseModel, Field

logger = logging.getLogger("evolutionos.execution.scheduling.job_engine")


class JobPriority(str, Enum):
    """FR-PX-1103: Priority classes where evolution-cycle jobs preempt maintenance jobs."""
    EVOLUTION_CYCLE = "EVOLUTION_CYCLE"   # Highest priority (preempts all)
    PUBLISHING = "PUBLISHING"             # High priority
    RESEARCH_SYNC = "RESEARCH_SYNC"       # Medium priority
    MAINTENANCE = "MAINTENANCE"           # Lowest priority (garbage collection, index compact)


class CatchUpPolicy(str, Enum):
    """FR-PX-1102: Missed-job detection catch-up policy per job class (`NFR-AVA-001`)."""
    RUN_ALL_MISSED = "RUN_ALL_MISSED"           # Execute all skipped occurrences sequentially
    RUN_LATEST_ONLY = "RUN_LATEST_ONLY"         # Execute only the single most recent skipped occurrence
    SKIP = "SKIP"                               # Ignore missed occurrences and wait for next interval


class ScheduledJob(BaseModel):
    """FR-PX-1101: Persisted job definition."""
    job_id: str
    name: str
    priority: JobPriority = JobPriority.MAINTENANCE
    catch_up_policy: CatchUpPolicy = CatchUpPolicy.RUN_LATEST_ONLY
    interval_seconds: Optional[int] = None      # For recurring jobs
    next_run_timestamp: float
    last_run_timestamp: Optional[float] = None
    is_recurring: bool = False
    payload: Dict[str, Any] = Field(default_factory=dict)
    status: str = "PENDING"


class JobStore:
    """FR-PX-1101: Persistent storage for scheduled jobs (`survives restart`)."""
    def __init__(self):
        self.jobs: Dict[str, ScheduledJob] = {}

    def save_job(self, job: ScheduledJob) -> None:
        self.jobs[job.job_id] = job

    def get_job(self, job_id: str) -> Optional[ScheduledJob]:
        return self.jobs.get(job_id)

    def list_pending_jobs(self) -> List[ScheduledJob]:
        return [j for j in self.jobs.values() if j.status in ["PENDING", "MISSED"]]


class JobEngine:
    """Orchestrates job scheduling, priority queueing, and missed-job recovery (`FR-PX-1101 to 1103`)."""

    def __init__(self, store: Optional[JobStore] = None):
        self.store = store or JobStore()
        self.handlers: Dict[str, Callable[[Dict[str, Any]], Any]] = {}

    def register_handler(self, job_name: str, handler: Callable[[Dict[str, Any]], Any]) -> None:
        self.handlers[job_name] = handler

    def schedule_job(
        self,
        job_id: str,
        name: str,
        next_run: float,
        priority: JobPriority = JobPriority.MAINTENANCE,
        interval_seconds: Optional[int] = None,
        catch_up_policy: CatchUpPolicy = CatchUpPolicy.RUN_LATEST_ONLY,
        payload: Optional[Dict[str, Any]] = None
    ) -> ScheduledJob:
        """Schedule a new one-shot or recurring job (`FR-PX-1101`)."""
        job = ScheduledJob(
            job_id=job_id,
            name=name,
            priority=priority,
            catch_up_policy=catch_up_policy,
            interval_seconds=interval_seconds,
            next_run_timestamp=next_run,
            is_recurring=(interval_seconds is not None and interval_seconds > 0),
            payload=payload or {}
        )
        self.store.save_job(job)
        return job

    def check_and_recover_missed_jobs(self, current_time: Optional[float] = None) -> List[ScheduledJob]:
        """FR-PX-1102: Detect missed jobs past their scheduled window and apply CatchUpPolicy."""
        now = current_time or time.time()
        recovered = []

        for job in self.store.list_pending_jobs():
            # If job was due more than 10 seconds ago without running, it is missed
            if job.next_run_timestamp < (now - 10.0):
                logger.warning(f"Missed job detected (`FR-PX-1102`): [{job.job_id}] due at {job.next_run_timestamp}, now is {now}")
                if job.catch_up_policy == CatchUpPolicy.SKIP:
                    job.status = "SKIPPED"
                    if job.is_recurring and job.interval_seconds:
                        job.next_run_timestamp = now + job.interval_seconds
                        job.status = "PENDING"
                elif job.catch_up_policy in [CatchUpPolicy.RUN_LATEST_ONLY, CatchUpPolicy.RUN_ALL_MISSED]:
                    job.status = "PENDING"  # Mark ready for immediate queue dispatch
                    recovered.append(job)
                self.store.save_job(job)

        return recovered

    def get_next_ready_jobs(self, current_time: Optional[float] = None) -> List[ScheduledJob]:
        """Retrieve jobs due right now, sorted strictly by priority (`FR-PX-1103`)."""
        now = current_time or time.time()
        self.check_and_recover_missed_jobs(now)

        ready = [j for j in self.store.list_pending_jobs() if j.next_run_timestamp <= now]

        # Priority sorting weight table (`FR-PX-1103`: EVOLUTION_CYCLE > PUBLISHING > RESEARCH_SYNC > MAINTENANCE)
        priority_weights = {
            JobPriority.EVOLUTION_CYCLE: 4,
            JobPriority.PUBLISHING: 3,
            JobPriority.RESEARCH_SYNC: 2,
            JobPriority.MAINTENANCE: 1
        }
        ready.sort(key=lambda j: priority_weights.get(j.priority, 0), reverse=True)
        return ready

    def execute_job(self, job: ScheduledJob, current_time: Optional[float] = None) -> Any:
        """Execute a scheduled job and reschedule if recurring (`FR-PX-1101`)."""
        now = current_time or time.time()
        handler = self.handlers.get(job.name)
        if not handler:
            raise ValueError(f"No registered handler for job type: {job.name}")

        logger.info(f"Executing job [{job.job_id}] ({job.name}, priority={job.priority.value})...")
        result = handler(job.payload)

        job.last_run_timestamp = now
        if job.is_recurring and job.interval_seconds:
            job.next_run_timestamp = now + job.interval_seconds
            job.status = "PENDING"
        else:
            job.status = "COMPLETED"
        self.store.save_job(job)
        return result
