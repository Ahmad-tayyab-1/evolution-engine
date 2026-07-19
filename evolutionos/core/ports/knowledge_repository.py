"""
KnowledgeRepository Port Interface (`Plan.md` Section 5 / Appendix B).
Abstract boundary contract defining persistence operations for KnowledgeRecords and Beliefs without DB dependencies.
"""
from abc import ABC, abstractmethod
from typing import List, Optional
from evolutionos.core.domain.ontology import KnowledgeRecord, Belief


class KnowledgeRepository(ABC):
    @abstractmethod
    def save_record(self, record: KnowledgeRecord) -> str:
        pass

    @abstractmethod
    def get_record(self, record_id: str) -> Optional[KnowledgeRecord]:
        pass

    @abstractmethod
    def query_records(self, record_type: Optional[str] = None, status: str = "ACTIVE") -> List[KnowledgeRecord]:
        pass

    @abstractmethod
    def save_belief(self, belief: Belief) -> str:
        pass

    @abstractmethod
    def get_belief(self, belief_id: str) -> Optional[Belief]:
        pass
