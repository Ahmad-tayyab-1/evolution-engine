
# 📚 EvolutionOS Documentation Set (Final)

```
docs/
│
├── 01_EvolutionOS_SRS_Foundation.md
├── 02_Evolution_Core.md
├── 03_Content_Intelligence.md
├── 04_Platform_Engineering.md
└── 05_Operations_and_Roadmap.md
```

---

# We start with

# 01_EvolutionOS_SRS_Foundation.md

---

# TABLE OF CONTENTS

```
1. Document Information

2. Executive Summary

3. Product Vision

4. Mission Statement

5. Philosophy

6. Core Principles

7. Problem Statement

8. Product Goals

9. Non Goals

10. Stakeholders

11. Target Users

12. Scope

13. Terminology

14. EvolutionOS Cognitive Architecture

15. Capabilities

16. Engines

17. System Thinking Model

18. Functional Requirements

19. Non Functional Requirements

20. Quality Attributes

21. Design Principles

22. Constraints

23. Assumptions

24. Risks

25. Success Metrics

26. Acceptance Criteria

27. Future Vision
```

---

# 1. Document Information

| Item          | Value                                                               |
| ------------- | ------------------------------------------------------------------- |
| Document Name | EvolutionOS Software Requirements Specification                     |
| Version       | 1.0 (Foundation Draft)                                              |
| Status        | Architecture Baseline                                               |
| Project       | EvolutionOS                                                         |
| Document Type | Software Requirements Specification (SRS)                           |
| Audience      | Developers, Architects, Researchers, Contributors                   |
| Purpose       | Define the complete foundation of EvolutionOS before implementation |

---

# 2. Executive Summary

EvolutionOS is an autonomous evolutionary intelligence platform.

Unlike traditional automation systems, its primary objective is **not content generation**. Content generation is merely one mechanism through which the platform conducts experiments in the real world.

The platform is designed to continuously improve itself by observing outcomes, extracting knowledge, updating beliefs, planning new experiments, and repeating this process indefinitely.

The first execution environment is YouTube.

However, YouTube is intentionally designed as a replaceable execution layer.

The Evolution Core must remain independent of any specific platform.

This separation allows the same intelligence to eventually operate on:

* YouTube
* Blogs
* Podcasts
* TikTok
* Instagram
* X
* LinkedIn
* Future digital platforms

without redesigning its reasoning architecture.

The long-term objective is to build a reusable autonomous intelligence capable of learning from real-world feedback.

---

# 3. Product Vision

## Vision Statement

> Build an autonomous intelligence that continuously improves its decision-making by conducting measurable experiments in real-world environments.

The product should become progressively more intelligent as its experience grows.

Unlike conventional AI assistants that forget previous interactions or repeatedly make the same mistakes, EvolutionOS accumulates durable knowledge.

Knowledge becomes the primary product.

Videos, articles, or other published artifacts are simply experiments that generate new knowledge.

---

# 4. Mission Statement

EvolutionOS exists to answer one fundamental question:

> **How can an artificial intelligence continuously improve itself through experience without requiring human intervention?**

The project seeks to transform AI from a passive responder into an active learner.

Its mission is to:

* Observe reality
* Form hypotheses
* Execute experiments
* Measure outcomes
* Learn from evidence
* Improve future decisions

This cycle forms the foundation of the entire platform.

---

# 5. Philosophy

EvolutionOS is built upon several philosophical principles.

## 5.1 Knowledge Compounds

Knowledge should never be discarded.

Every experiment contributes permanent value.

Mistakes are treated as assets because they improve future decision quality.

---

## 5.2 Evidence Overrides Assumptions

No belief is permanent.

Every assumption must be supported by evidence.

When evidence changes, beliefs change.

---

## 5.3 Explainability

Every important decision must be explainable.

The system should always be able to answer questions such as:

* Why was this topic selected?
* Why was this thumbnail chosen?
* Why was this hook generated?
* Which evidence supported this decision?
* What confidence level exists?

Opaque decision-making is unacceptable.

---

## 5.4 Continuous Evolution

Improvement is never complete.

The system is expected to evolve indefinitely.

There is no concept of a "finished" model.

Instead, every execution cycle contributes to future capability.

---

## 5.5 Platform Independence

The intelligence layer must never depend on YouTube.

Execution environments are interchangeable.

This principle guarantees long-term adaptability.

---

# 6. Core Principles

The following principles govern every architectural decision.

### CP-001

Every published artifact is an experiment.

---

### CP-002

Every experiment must produce measurable learning.

---

### CP-003

Knowledge is the primary asset.

---

### CP-004

Beliefs must include confidence.

---

### CP-005

Learning never stops.

---

### CP-006

The system must justify every strategic decision.

---

### CP-007

Experiments change one variable whenever practical to improve attribution.

---

### CP-008

The platform optimizes long-term intelligence rather than short-term metrics.

---

### CP-009

Human intervention should be minimized after deployment.

---

### CP-010

Every subsystem must contribute to the core evolution loop:

```
Observe

↓

Learn

↓

Update Knowledge

↓

Reason

↓

Plan

↓

Experiment

↓

Execute

↓

Observe Again
```

---

# 7. Problem Statement

Current AI content automation systems suffer from several fundamental limitations:

* They generate outputs but do not accumulate durable knowledge.
* They cannot explain why a strategy succeeds or fails.
* They repeat unsuccessful patterns because they lack structured memory.
* They optimize for content production rather than learning.
* They are tightly coupled to a specific platform.

As a result, they behave as automation pipelines instead of adaptive systems.

EvolutionOS is intended to solve these problems by placing **learning, reasoning, and knowledge accumulation** at the center of the architecture.

---

Excellent. Now we move from **vision** to the actual architecture. This section is where EvolutionOS becomes different from every other AI automation project.

---

# 8. Product Goals

## 8.1 Primary Goal

The primary objective of EvolutionOS is **not** to maximize views, subscribers, or revenue.

The primary objective is:

> **Continuously improve decision-making through measurable experimentation and accumulated knowledge.**

Every other metric is a consequence of better decisions.

---

## 8.2 Long-Term Objectives

### PG-001 — Autonomous Learning

The system shall improve its future decisions using evidence gathered from previous experiments.

---

### PG-002 — Persistent Knowledge

Knowledge shall persist across executions, deployments, and software versions.

The system must never "forget" successful strategies unless evidence indicates they are no longer effective.

---

### PG-003 — Explainable Intelligence

Every strategic decision shall reference:

* supporting evidence
* confidence level
* originating experiments
* affected beliefs

No critical decision shall be a black box.

---

### PG-004 — Platform Independence

The Evolution Core shall operate independently of YouTube.

Replacing the execution platform must not require redesigning the intelligence layer.

---

### PG-005 — Continuous Adaptation

The system shall continuously adapt to:

* changing audience behavior
* market trends
* niche saturation
* platform algorithm changes
* emerging content opportunities

---

### PG-006 — Autonomous Operation

After installation and configuration, EvolutionOS should operate without routine human intervention.

Expected manual tasks:

* Initial deployment
* API configuration
* Optional policy updates
* System upgrades

Everything else should be autonomous.

---

# 9. Non-Goals

Defining what EvolutionOS **will not** become is just as important.

### NG-001

EvolutionOS is **not** a simple AI content generator.

---

### NG-002

EvolutionOS is **not** a collection of prompt templates.

---

### NG-003

EvolutionOS is **not** designed to maximize upload frequency at the expense of learning quality.

---

### NG-004

EvolutionOS will not optimize solely for short-term metrics.

Long-term knowledge accumulation takes priority.

---

### NG-005

EvolutionOS is not tightly coupled to any specific AI model.

All LLM providers should be replaceable.

---

### NG-006

EvolutionOS is not dependent on a single niche.

The niche itself is an experimental variable.

---

# 10. Stakeholders

## Primary Stakeholder

System Owner

Responsibilities:

* Deploy system
* Configure API keys
* Define high-level objectives
* Review performance

---

## Secondary Stakeholders

Open Source Contributors

Responsibilities

* Improve algorithms
* Extend capabilities
* Fix defects
* Add providers

---

Researchers

Responsibilities

* Evaluate learning algorithms
* Measure intelligence growth
* Design experiments

---

Future Developers

Responsibilities

* Extend modules
* Maintain architecture
* Implement new execution environments

---

# 11. Target Users

EvolutionOS is intended for users interested in building autonomous learning systems rather than simple automation.

Potential users include:

* AI engineers
* DevOps engineers
* Software architects
* Researchers
* Content creators interested in experimentation
* Open-source contributors

---

# 12. Scope

## In Scope

The platform includes:

### Intelligence

* Knowledge acquisition
* Reasoning
* Learning
* Reflection
* Planning
* Experimentation
* Decision making

---

### Content

* Research
* Story generation
* Hook optimization
* Visual planning
* Publishing
* Analytics

---

### Infrastructure

* Dashboard
* Database
* Scheduler
* Monitoring
* Logging
* Worker management
* Deployment

---

### Evolution

* Knowledge graph
* Belief management
* Confidence tracking
* Rule discovery
* Experiment management
* Strategy evolution

---

## Out of Scope

The following are intentionally excluded.

* Manual editing workflows
* Manual topic selection
* Manual thumbnail creation
* Manual script writing
* Manual publishing
* Manual analytics processing
* Manual experiment tracking

The philosophy is **automation by design**.

---

# 13. Terminology

| Term        | Definition                                                              |
| ----------- | ----------------------------------------------------------------------- |
| Capability  | A high-level cognitive ability of EvolutionOS.                          |
| Engine      | A subsystem implementing a capability.                                  |
| Experiment  | A controlled attempt to validate a hypothesis.                          |
| Belief      | A conclusion with associated confidence and evidence.                   |
| Knowledge   | Structured information retained from experiments.                       |
| Fitness     | Numerical measure of long-term success.                                 |
| Mutation    | Intentional variation introduced into an experiment.                    |
| Reflection  | Analysis comparing predictions with actual outcomes.                    |
| World Model | Internal representation of the external environment.                    |
| Candidate   | A possible title, hook, topic, script, or strategy awaiting evaluation. |
| Observation | Raw data collected from execution environments.                         |

---

# 14. EvolutionOS Cognitive Architecture

This is the defining architectural concept of EvolutionOS.

Instead of organizing the system around software modules, EvolutionOS is organized around **Capabilities**.

A capability represents **what the system is able to do**.

An engine represents **how that capability is implemented**.

This separation improves modularity and future extensibility.

---

## Cognitive Layer

```text
                    EVOLUTIONOS

                         │

 ┌─────────────────────────────────────────────┐
 │              CAPABILITIES                   │
 └─────────────────────────────────────────────┘

 Learn
 Reason
 Create
 Observe
 Evolve

                         │

                         ▼

 ┌─────────────────────────────────────────────┐
 │                 ENGINES                     │
 └─────────────────────────────────────────────┘

 Knowledge Engine
 Learning Engine
 Reflection Engine
 Belief Engine
 Decision Engine
 Strategy Engine
 Research Engine
 Story Engine
 Visual Engine
 Publishing Engine
 Analytics Engine
 Experiment Engine
 Mutation Engine
 Fitness Engine
 Memory Engine
```

Capabilities remain stable even if individual engines evolve.

---

# 15. Capability Definitions

## Capability: Learn

Purpose:

Transform observations into durable knowledge.

Responsible for:

* knowledge extraction
* lesson generation
* reflection
* confidence updates

Implemented by:

* Knowledge Engine
* Learning Engine
* Reflection Engine

---

## Capability: Reason

Purpose:

Make explainable decisions using accumulated knowledge.

Responsible for:

* planning
* inference
* strategy
* prioritization
* confidence evaluation

Implemented by:

* Belief Engine
* Decision Engine
* Strategy Engine

---

## Capability: Create

Purpose:

Transform strategies into publishable content.

Responsible for:

* research
* storytelling
* scene planning
* visual composition
* publishing

Implemented by:

* Research Engine
* Story Engine
* Visual Engine
* Publishing Engine

---

## Capability: Observe

Purpose:

Understand the external world through measurable feedback.

Responsible for:

* analytics collection
* trend monitoring
* competitor awareness
* audience behavior

Implemented by:

* Analytics Engine
* Trend Engine
* Competitor Intelligence Engine

---

## Capability: Evolve

Purpose:

Improve the entire system over time.

Responsible for:

* experimentation
* mutation
* fitness optimization
* memory consolidation

Implemented by:

* Experiment Engine
* Mutation Engine
* Fitness Engine
* Memory Engine

---

## Architectural Principle AP-001

> **Capabilities define what EvolutionOS can do. Engines define how it does it.**

This distinction is mandatory throughout the project.

All future modules, APIs, and documentation must map to one Capability first and then to one or more Engines.

---

Excellent. This is where the document stops being a product description and becomes a **true software specification**.

From this point forward, every requirement will have an ID and should be traceable to implementation.

---

# 16. System Thinking Model

## 16.1 Overview

EvolutionOS is designed as a **closed adaptive feedback system**.

Unlike traditional software that executes predefined workflows, EvolutionOS continuously modifies its own future behavior based on observed outcomes.

The platform shall be modeled as an iterative learning cycle rather than a linear pipeline.

The core system loop is:

```text
Observe
    │
    ▼
Interpret
    │
    ▼
Learn
    │
    ▼
Update Knowledge
    │
    ▼
Update Beliefs
    │
    ▼
Reason
    │
    ▼
Plan
    │
    ▼
Generate Experiments
    │
    ▼
Execute
    │
    ▼
Measure Results
    │
    └─────────────────────┐
                          ▼
                     Observe Again
```

This loop is mandatory.

No subsystem may bypass it.

---

## 16.2 Learning Before Production

Traditional automation systems optimize for production.

EvolutionOS optimizes for learning.

Therefore:

```
Learning > Production
Knowledge > Output
Evidence > Assumptions
Long-Term Fitness > Short-Term Metrics
```

Example

Traditional AI

```
Generate
↓

Upload
↓

Done
```

EvolutionOS

```
Generate

↓

Predict

↓

Execute

↓

Observe

↓

Compare

↓

Reflect

↓

Learn

↓

Improve
```

Execution is only one stage of learning.

---

## 16.3 Feedback Hierarchy

Not all feedback has equal value.

The platform shall classify observations into multiple levels.

### Level 1

Operational Feedback

Examples

* upload succeeded
* render failed
* API timeout

Purpose

Maintain platform health.

---

### Level 2

Performance Feedback

Examples

CTR

Retention

Watch Time

Subscribers

Purpose

Measure experiment outcome.

---

### Level 3

Behavioral Feedback

Examples

Audience skipped introduction.

Audience replayed explanation.

Audience left after advertisement.

Purpose

Improve storytelling.

---

### Level 4

Strategic Feedback

Examples

Cybersecurity consistently outperforms history.

Question hooks outperform statistic hooks.

10-minute videos outperform 20-minute videos.

Purpose

Improve long-term planning.

---

### Level 5

Evolutionary Feedback

Examples

Current learning strategy is ineffective.

Mutation rate too high.

Exploration phase should continue.

Purpose

Improve EvolutionOS itself.

---

# 17. Functional Requirements

Each requirement shall have:

* Identifier
* Description
* Priority
* Rationale
* Related Capability

---

## Capability: Learn

---

### FR-001

Title

Observation Storage

Requirement

The platform shall permanently store every measurable observation generated during execution.

Priority

Critical

Capability

Learn

Rationale

Future learning depends on historical evidence.

---

### FR-002

Knowledge Persistence

The platform shall preserve accumulated knowledge across restarts and software upgrades.

Priority

Critical

Capability

Learn

---

### FR-003

Lesson Extraction

After every completed experiment the platform shall generate one or more structured lessons.

Each lesson shall include

* observation
* interpretation
* confidence
* supporting evidence

---

### FR-004

Reflection Generation

The platform shall automatically compare predicted outcomes against actual outcomes.

---

### FR-005

Confidence Update

Every belief shall have a confidence score.

Confidence shall increase when evidence supports the belief.

Confidence shall decrease when contradictory evidence appears.

---

### FR-006

Knowledge Consolidation

Duplicate lessons shall be merged into unified knowledge whenever similarity exceeds a configurable threshold.

---

### FR-007

Knowledge Decay

Knowledge may gradually lose confidence when it has not been validated over time.

Knowledge shall never be deleted automatically without policy approval.

---

## Capability: Reason

---

### FR-008

Decision Explainability

Every strategic decision shall reference supporting evidence.

---

### FR-009

Hypothesis Generation

Before every experiment the platform shall generate an explicit hypothesis.

Example

```
Question hooks

↓

Increase CTR

↓

for Engineering

↓

by 8%
```

---

### FR-010

Strategy Selection

The platform shall generate multiple strategies before selecting one.

---

### FR-011

Risk Evaluation

Every experiment shall receive a calculated risk score.

---

### FR-012

Decision Traceability

The platform shall be capable of reconstructing the reasoning path behind every decision.

---

## Capability: Create

---

### FR-013

Topic Generation

Generate multiple candidate topics.

Never produce only one candidate.

---

### FR-014

Story Planning

Every script shall be based on a narrative structure.

Minimum sections

* Hook
* Context
* Conflict
* Development
* Resolution
* Reflection

---

### FR-015

Visual Strategy

Before generating visuals the platform shall determine the most suitable visual style.

Possible strategies

* Documentary

* Maps

* Timelines

* Motion graphics

* Stock footage

* Hybrid

---

### FR-016

Candidate Evaluation

Topics

Hooks

Titles

Thumbnails

Visual strategies

shall all be ranked before publication.

---

### FR-017

Publishing

The platform shall autonomously publish approved content.

---

## Capability: Observe

---

### FR-018

Analytics Collection

Collect

CTR

Retention

Watch Time

Subscribers

Comments

Impressions

Traffic Sources

Returning Viewers

---

### FR-019

Trend Monitoring

Continuously identify emerging opportunities.

---

### FR-020

Competitor Awareness

Maintain structured information about relevant channels and competitors.

The purpose is **trend awareness**, not copying content.

---

## Capability: Evolve

---

### FR-021

Controlled Mutation

Each experiment should modify only one or a small number of variables whenever practical.

---

### FR-022

Fitness Calculation

Every experiment shall produce a fitness score.

---

### FR-023

Experiment Registry

Maintain a permanent history of all experiments.

---

### FR-024

Evolution Timeline

Store every strategic evolution event.

---

### FR-025

Self Improvement

The platform shall periodically evaluate whether its own learning process requires adjustment.

---

# 18. Requirement Traceability

Every feature implemented within EvolutionOS must be traceable.

```
Capability

↓

Engine

↓

Requirement

↓

Implementation

↓

Test

↓

Observation

↓

Knowledge
```

Example

```
Capability

Learn

↓

Knowledge Engine

↓

FR-003

↓

lesson_generator.py

↓

Unit Test

↓

Experiment #218

↓

Knowledge Rule #412
```

No implementation should exist without a corresponding requirement.

---

This section establishes the engineering discipline that the rest of the project will follow. In the next part, we'll define the **Non-Functional Requirements (NFRs)**—performance, reliability, scalability, security, observability, maintainability, extensibility, and autonomy—followed by **Quality Attributes**, **Design Constraints**, and **Acceptance Criteria** that every implementation must satisfy.


Perfect. From this point onward, I'm going to write this as if I'm the Chief Software Architect writing the official SRS. I'll also start introducing requirement IDs, rationale, measurable acceptance criteria, and architecture decisions.

---

# 19. Non-Functional Requirements (NFR)

## 19.1 Overview

Functional requirements describe **what EvolutionOS does**.

Non-functional requirements describe **how well EvolutionOS must perform** while doing it.

These requirements are mandatory across every subsystem and are not tied to a single engine.

Every future implementation must satisfy these requirements.

---

# 19.2 Performance Requirements

## NFR-PERF-001 — Decision Latency

### Requirement

The Decision Engine shall generate a strategic decision within a configurable maximum response time.

### Rationale

Long decision times delay the evolution loop and reduce system responsiveness.

### Acceptance Criteria

* Average decision latency remains within the configured threshold under normal workload.
* Latency is measured and logged for every decision.

---

## NFR-PERF-002 — Knowledge Retrieval

### Requirement

The Knowledge Engine shall support efficient retrieval of relevant knowledge without requiring a full scan of stored records.

### Rationale

As the knowledge base grows, lookup performance must remain practical.

### Design Decision

Knowledge retrieval should rely on indexed lookups and structured relationships rather than sequential searches wherever feasible.

---

## NFR-PERF-003 — Concurrent Operations

### Requirement

Independent tasks shall execute concurrently when they do not share mutable state.

Examples:

* Analytics collection
* Research
* Asset downloading
* Competitor monitoring

### Rationale

Concurrency improves throughput without affecting reasoning quality.

---

## NFR-PERF-004 — Resource Awareness

The platform shall continuously monitor CPU, memory, storage, and network usage.

High resource utilization shall trigger adaptive behavior, such as delaying non-critical background tasks.

---

# 19.3 Reliability Requirements

---

## NFR-REL-001 — Fault Isolation

Failure of one engine shall not terminate the entire platform.

Example

If the Research Engine fails, the Learning Engine must continue processing previous experiments.

---

## NFR-REL-002 — Automatic Retry

Recoverable failures shall be retried using configurable retry policies with exponential backoff.

Applicable to:

* API requests
* Downloads
* Uploads
* Database operations

---

## NFR-REL-003 — Graceful Degradation

If an external provider becomes unavailable, the platform shall continue operating using available providers whenever possible.

Example

Groq unavailable

↓

Fallback to Gemini

↓

Continue experiment

---

## NFR-REL-004 — Persistent State

Unexpected shutdowns shall not cause permanent loss of accumulated knowledge.

Critical state shall be recoverable after restart.

---

# 19.4 Availability Requirements

---

## NFR-AVA-001

Scheduler availability shall be continuously monitored.

Missed scheduled jobs shall be detected and rescheduled automatically.

---

## NFR-AVA-002

The platform shall automatically resume incomplete workflows after restart.

Example

```text
Research Complete

Story Generated

Rendering In Progress

↓

Server Crash

↓

Restart

↓

Continue Rendering
```

Restarting from the beginning is not acceptable.

---

# 19.5 Scalability Requirements

---

## NFR-SCL-001

The architecture shall support increasing workload without redesigning the Evolution Core.

Future scaling examples:

* More workers
* More execution platforms
* More AI providers
* Larger knowledge base

---

## NFR-SCL-002

Every major engine shall expose well-defined interfaces.

Internal implementation changes must not affect unrelated engines.

---

## NFR-SCL-003

Execution environments shall be replaceable.

Examples

Current

YouTube

Future

Blog

Podcast

TikTok

LinkedIn

No Evolution Core changes required.

---

# 19.6 Security Requirements

---

## NFR-SEC-001

Secrets shall never be hardcoded.

Examples

API Keys

Database passwords

OAuth credentials

---

## NFR-SEC-002

Sensitive configuration shall be loaded securely during runtime.

---

## NFR-SEC-003

Secrets shall never appear in application logs.

---

## NFR-SEC-004

Administrative actions shall generate immutable audit records.

---

# 19.7 Maintainability Requirements

---

## NFR-MNT-001

Every engine shall have a single clearly defined responsibility.

---

## NFR-MNT-002

Modules shall communicate through stable interfaces.

---

## NFR-MNT-003

Circular dependencies between engines are prohibited.

---

## NFR-MNT-004

Every public interface shall be documented.

---

## NFR-MNT-005

Every feature shall reference at least one Functional Requirement.

No orphan implementation is permitted.

---

# 19.8 Observability Requirements

---

## NFR-OBS-001

Every engine shall emit structured logs.

Minimum information

* timestamp
* engine
* event
* severity
* correlation ID

---

## NFR-OBS-002

Critical metrics shall be collected continuously.

Examples

Decision latency

Learning throughput

Knowledge growth

Experiment duration

API failures

Rendering time

Upload success rate

---

## NFR-OBS-003

The platform shall expose health status for every engine.

Health states

* Healthy
* Degraded
* Failed
* Recovering

---

# 19.9 Explainability Requirements

This is one of the defining characteristics of EvolutionOS.

---

## NFR-EXP-001

Every strategic decision shall be explainable.

Example

Why was this topic selected?

↓

Because

Rule #82

Confidence

91%

Supported by

18 experiments

---

## NFR-EXP-002

Every generated belief shall reference supporting evidence.

---

## NFR-EXP-003

Every experiment shall preserve its complete reasoning history.

Future users must be able to reconstruct why an experiment existed.

---

# 19.10 Adaptability Requirements

---

## NFR-ADP-001

The platform shall adapt to changing evidence without manual intervention.

---

## NFR-ADP-002

Beliefs shall evolve continuously.

Confidence is dynamic.

Never static.

---

## NFR-ADP-003

Strategies shall automatically evolve based on accumulated knowledge.

---

# 19.11 Testability Requirements

---

## NFR-TST-001

Every engine shall be testable independently.

---

## NFR-TST-002

Every requirement shall have at least one verification method.

Possible methods

* Unit test
* Integration test
* Simulation
* Manual verification (only where unavoidable)

---

## NFR-TST-003

The platform shall support replaying historical experiments for regression testing.

---

# 19.12 Portability Requirements

---

## NFR-PRT-001

EvolutionOS shall run on:

* Linux
* Docker
* Local workstation
* AWS EC2

without source code modification.

---

## NFR-PRT-002

The platform shall support operation on resource-constrained infrastructure.

Initial design target:

Single AWS Free Tier EC2 instance.

---

# 19.13 Autonomy Requirements

These requirements distinguish EvolutionOS from traditional automation software.

---

## NFR-AUT-001

Following initial installation and configuration, routine operation shall require no human intervention.

---

## NFR-AUT-002

The system shall autonomously:

* discover opportunities
* generate hypotheses
* execute experiments
* analyze outcomes
* update knowledge
* improve future decisions

---

## NFR-AUT-003

The system shall detect when its own learning process becomes ineffective and trigger self-evaluation.

---

# Architectural Decision Record (ADR)

## ADR-001 — Why Capabilities Instead of Services?

### Context

Traditional software architectures organize functionality around services or modules. While effective for business applications, this structure does not reflect how an adaptive intelligence operates.

### Decision

EvolutionOS introduces a **Capabilities layer** above individual engines.

Capabilities answer the question:

> **"What cognitive ability does the system possess?"**

Examples:

* Learn
* Reason
* Create
* Observe
* Evolve

Engines then implement those capabilities.

### Rationale

This separation provides several advantages:

* A stable cognitive model even as implementations evolve.
* Easier navigation of the architecture.
* Clear mapping from goals to implementation.
* Reusability of capabilities across different execution environments.

### Consequences

Positive:

* Better modularity.
* Clearer documentation.
* Simpler extension to future platforms (blogs, podcasts, social media).

Trade-off:

* Slightly more complex architecture due to the additional abstraction layer.

---

Excellent. Now we move into what I consider the **engineering constitution** of EvolutionOS.

This section defines the rules that **every future developer, AI agent, and contributor must follow**. If a future implementation violates these principles, it should be considered an architectural defect.

---

# 20. Quality Attributes

## 20.1 Overview

Quality Attributes define the characteristics that EvolutionOS must exhibit regardless of implementation details.

Unlike Functional Requirements, which describe **what the system does**, Quality Attributes describe **how the system should behave** throughout its lifecycle.

Every architectural decision must improve at least one Quality Attribute without significantly degrading another.

---

# QA-001 Explainability

## Definition

Every significant action performed by EvolutionOS shall be explainable to a human observer.

This includes:

* Decisions
* Recommendations
* Belief updates
* Knowledge creation
* Strategy selection
* Experiment generation

---

## Motivation

Most AI systems behave as black boxes.

EvolutionOS shall behave as a transparent intelligence.

A developer must always be able to ask:

> Why?

And receive a complete answer.

---

## Required Outputs

Every strategic decision shall expose:

Decision ID

Timestamp

Responsible Capability

Responsible Engine

Supporting Rules

Supporting Evidence

Confidence Score

Alternative Candidates

Rejected Candidates

Expected Outcome

Actual Outcome

Reflection Report

---

## Example

```text
Decision #482

Capability:
Reason

Engine:
Decision Engine

Decision:
Use Question Hook

Evidence:
18 Previous Experiments

Average CTR:
11.8%

Confidence:
92%

Rejected Strategy:
Statistic Hook

Reason:
Lower historical fitness
```

---

## Acceptance Criteria

Every dashboard decision page must contain sufficient information for a developer to reconstruct the reasoning process.

---

# QA-002 Adaptability

## Definition

EvolutionOS must continuously adapt to new information.

No rule is permanent.

No strategy is permanent.

No niche is permanent.

Everything evolves.

---

## Architectural Implications

Beliefs require confidence.

Knowledge requires timestamps.

Rules require evidence.

Strategies require expiration.

Experiments require comparison.

---

## Adaptation Cycle

```text
Observation

↓

Evidence

↓

Knowledge

↓

Belief Update

↓

Strategy Update

↓

Experiment

↓

New Observation
```

---

## Acceptance Criteria

The platform shall demonstrate measurable strategic changes after accumulating new evidence.

---

# QA-003 Modularity

## Definition

Every subsystem shall have a clearly defined responsibility.

Responsibilities shall not overlap unnecessarily.

---

## Rules

One capability

↓

Many engines

One engine

↓

One responsibility

---

## Good Example

Knowledge Engine

Stores knowledge.

Learning Engine

Creates knowledge.

Decision Engine

Uses knowledge.

---

## Bad Example

Decision Engine

Stores knowledge

Generates stories

Publishes videos

Updates analytics

This violates separation of concerns.

---

## Acceptance Criteria

Removing an engine should affect only its associated capability.

---

# QA-004 Extensibility

## Definition

EvolutionOS must be extendable without redesigning existing architecture.

---

## Example

Today

```text
Research Engine

↓

Google Search
```

Tomorrow

```text
Research Engine

↓

Google

Wikipedia

ArXiv

Reddit

News APIs
```

The Research Engine remains unchanged.

Only providers change.

---

## Required Extension Points

LLM Providers

Search Providers

Image Providers

Video Providers

Publishing Platforms

Storage Backends

Knowledge Databases

---

## Acceptance Criteria

Adding a new provider shall not require modifications to unrelated engines.

---

# QA-005 Maintainability

## Definition

The platform shall remain understandable after years of development.

---

## Required Practices

Stable interfaces

Clear naming

Requirement traceability

Architecture Decision Records

Documentation

Unit testing

Integration testing

---

## Acceptance Criteria

A new developer should understand any engine by reading only:

Engine documentation

Public interfaces

Requirements

---

# QA-006 Reliability

## Definition

EvolutionOS shall continue operating despite failures.

---

## Reliability Principles

Retry

Recovery

Isolation

Fallback

Graceful degradation

---

## Failure Example

```text
Gemini API

↓

Unavailable

↓

Fallback

↓

OpenAI

↓

Continue Learning
```

No knowledge should be lost.

---

# QA-007 Observability

EvolutionOS should observe itself.

Every engine produces:

Logs

Metrics

Health

Events

Tracing

---

## Dashboard Requirements

System Health

Experiment Queue

Knowledge Growth

Decision Latency

CPU

Memory

Storage

Provider Health

Worker Health

---

# QA-008 Testability

Everything should be testable.

Not just code.

Ideas.

Beliefs.

Experiments.

Strategies.

---

Example

Question Hook

↓

Hypothesis

↓

Experiment

↓

Result

↓

Pass/Fail

---

# QA-009 Intelligence Growth

This quality attribute is unique.

Traditional software measures:

Availability

Latency

Errors

EvolutionOS also measures:

**Intelligence Growth**

---

## Intelligence Indicators

Knowledge Count

Knowledge Quality

Prediction Accuracy

Decision Accuracy

Confidence Calibration

Experiment Success Rate

Rule Accuracy

Belief Stability

---

## Intelligence KPI

The platform shall become more accurate over time.

If prediction accuracy is decreasing,

the system is not evolving.

---

# QA-010 Platform Independence

The intelligence must not depend upon YouTube.

Today

```text
Evolution Core

↓

YouTube
```

Tomorrow

```text
Evolution Core

↓

YouTube

↓

Blogs

↓

TikTok

↓

LinkedIn

↓

Podcast
```

The core remains unchanged.

---

# 21. Design Principles

This chapter defines the permanent engineering rules.

Every pull request should reference these principles.

---

## DP-001

Knowledge Before Automation

Automation exists to generate knowledge.

Not the other way around.

---

## DP-002

Everything Is An Experiment

Nothing is published without a measurable hypothesis.

---

## DP-003

Evidence Over Intuition

The platform shall trust measurements over assumptions.

---

## DP-004

Capabilities Before Engines

Always determine

"What capability is required?"

before designing

"Which engine should implement it?"

---

## DP-005

Loose Coupling

Engines communicate through contracts.

Never through internal implementation details.

---

## DP-006

Single Responsibility

Every engine has one reason to change.

---

## DP-007

Platform Independence

Execution platforms are plugins.

The Evolution Core is permanent.

---

## DP-008

AI Provider Independence

No engine shall depend on one LLM provider.

Support multiple providers through abstraction.

---

## DP-009

Knowledge Is Immutable

Historical observations are never edited.

Corrections create new knowledge rather than rewriting history.

---

## DP-010

Confidence Is Mandatory

Every belief

Every rule

Every prediction

Every recommendation

must include confidence.

---

## DP-011

Controlled Mutation

The platform should modify only a few variables per experiment whenever practical.

This improves causal attribution.

---

## DP-012

Reflection Is Required

Every completed experiment shall end with reflection.

No exceptions.

---

## DP-013

Everything Is Measured

If something cannot be measured,

it cannot improve.

---

## DP-014

Human Override Exists

Although autonomous,

the owner must always be able to:

Pause

Resume

Approve

Reject

Rollback

Experiments.

---

## DP-015

Architecture Over Features

Adding features that violate the architecture is prohibited.

Architecture has priority over convenience.

---

# Architecture Decision Record

## ADR-002 — Why Knowledge Is the Center of the Architecture

### Context

Most AI systems place the LLM at the center of the architecture.

This makes the model responsible for reasoning, memory, and decision-making.

### Decision

EvolutionOS places the **Knowledge Layer** at the center instead.

LLMs become interchangeable tools used by the system rather than the system itself.

### Rationale

This provides:

* Provider independence.
* Persistent learning.
* Explainability.
* Long-term memory.
* Better experimentation.
* Lower vendor lock-in.

### Consequences

Positive:

* Easier to swap AI providers.
* Knowledge survives model changes.
* Decisions become reproducible.

Trade-off:

* Requires significantly more engineering effort.

---

## ADR-003 — Why YouTube Is Treated as an Execution Environment

### Decision

YouTube is not part of the Evolution Core.

It is an execution plugin.

### Rationale

The intelligence should be reusable across any platform capable of producing measurable feedback.

This decision ensures EvolutionOS can evolve beyond content creation into a general-purpose autonomous experimentation system.

---

At this point, Volume 1 is around **65–70% complete**. The remaining sections are:

* **22. Constraints**
* **23. Assumptions**
* **24. Risk Register**
* **25. Success Metrics**
* **26. Acceptance Criteria**
* **27. Future Vision**
* **Appendix A — Requirement Index**
* **Appendix B — Glossary**
* **Appendix C — Architecture Decision Register (ADR-001 to ADR-020)**

These final chapters will complete the Foundation document and make it a true architectural specification rather than just an SRS.
Excellent. From this point forward, we're defining the governance of EvolutionOS. These sections answer questions like:

* **What limitations does the system have?**
* **What assumptions is it allowed to make?**
* **What can go wrong?**
* **How do we know if it's succeeding?**

These chapters are critical because they influence every implementation decision.

---

# 22. Constraints

## 22.1 Purpose

Constraints define the boundaries within which EvolutionOS must operate.

Unlike requirements, constraints are limitations imposed by technology, infrastructure, cost, external systems, or design philosophy.

Every future implementation shall acknowledge and respect these constraints.

---

# 22.2 Infrastructure Constraints

---

## CON-INF-001

### AWS Free Tier First

### Requirement

The initial reference implementation shall be capable of operating on a single AWS Free Tier EC2 instance.

### Rationale

The project should remain accessible to individual developers and researchers without requiring significant infrastructure costs.

### Implications

Initial architecture shall prioritize:

* Low memory usage
* Efficient CPU utilization
* Lightweight services
* Background task scheduling
* Incremental processing

---

## CON-INF-002

### Stateless Workers

Execution workers shall remain stateless whenever practical.

Persistent state belongs only to dedicated storage systems.

Benefits

* Easier recovery
* Horizontal scaling
* Simpler deployment

---

## CON-INF-003

### Containerized Deployment

Every major service shall support containerized deployment.

Reference deployment uses Docker Compose.

Future deployment may use Kubernetes without architectural changes.

---

## CON-INF-004

### Resource Awareness

The platform shall monitor available resources and dynamically adjust workload.

Example

```text
CPU > 90%

↓

Pause non-critical tasks

↓

Continue essential evolution loop
```

---

# 22.3 Financial Constraints

---

## CON-FIN-001

### Minimize Operational Cost

Architecture decisions should minimize recurring operational expenses.

Preference order

1. Open-source solutions
2. Free-tier cloud services
3. Paid services only when necessary

---

## CON-FIN-002

### AI Provider Flexibility

The platform shall not assume unlimited AI usage.

Reasoning tasks should be optimized to minimize token consumption.

Heavy inference should occur only when justified.

---

## CON-FIN-003

### Storage Optimization

Raw data should not be retained indefinitely.

EvolutionOS stores:

Knowledge

Beliefs

Metrics

Experiments

Rules

instead of every intermediate artifact forever.

Storage policies shall be configurable.

---

# 22.4 Technical Constraints

---

## CON-TEC-001

### Language Independence

The architecture shall not depend on any programming language.

The reference implementation may use Python.

Future implementations may replace components without changing architecture.

---

## CON-TEC-002

### AI Model Independence

No subsystem shall rely upon one specific AI model.

Supported providers may include

OpenAI

Gemini

Anthropic

Groq

Local models

Future providers

Switching providers must not require redesign.

---

## CON-TEC-003

### Vendor Independence

Avoid vendor lock-in whenever practical.

External APIs should remain behind abstraction layers.

---

## CON-TEC-004

### Event-Driven Communication

Independent engines shall communicate using events whenever appropriate.

Avoid tightly coupled synchronous chains.

---

# 22.5 Data Constraints

---

## CON-DAT-001

Knowledge records shall be immutable.

Corrections create new records.

Historical evidence remains intact.

---

## CON-DAT-002

Every experiment receives a globally unique identifier.

---

## CON-DAT-003

Every observation receives a timestamp.

---

## CON-DAT-004

Every belief records:

Current confidence

Supporting evidence

Contradicting evidence

Creation date

Last validation

---

# 22.6 Ethical Constraints

---

## CON-ETH-001

EvolutionOS shall respect platform terms of service.

---

## CON-ETH-002

The platform shall clearly distinguish between:

Observed facts

Predictions

Hypotheses

Beliefs

Generated content

---

## CON-ETH-003

Confidence shall never be represented as certainty.

---

## CON-ETH-004

Evidence must always be traceable.

---

# 23. Assumptions

## 23.1 Purpose

Assumptions describe conditions that EvolutionOS expects to be true.

If assumptions become invalid, adaptation may be required.

---

# Infrastructure Assumptions

---

## ASM-INF-001

Persistent storage is available.

---

## ASM-INF-002

Internet connectivity exists during scheduled operations.

---

## ASM-INF-003

System clock is reasonably accurate.

---

## ASM-INF-004

Docker runtime is available.

---

## ASM-INF-005

Background scheduling is operational.

---

# AI Assumptions

---

## ASM-AI-001

One or more LLM providers are available.

---

## ASM-AI-002

Model quality will generally improve over time.

Architecture should remain compatible with future models.

---

## ASM-AI-003

Prompt behavior may change.

Prompt versions must therefore be tracked.

---

## ASM-AI-004

LLMs may produce hallucinations.

Independent verification may be required.

---

# Knowledge Assumptions

---

## ASM-KNW-001

Knowledge improves through accumulated evidence.

---

## ASM-KNW-002

No belief remains permanently valid.

---

## ASM-KNW-003

Confidence should evolve continuously.

---

## ASM-KNW-004

Contradictory evidence is valuable.

---

# Platform Assumptions

---

## ASM-PLT-001

Execution environments produce measurable feedback.

---

## ASM-PLT-002

Analytics APIs remain accessible.

---

## ASM-PLT-003

Platform algorithms evolve over time.

EvolutionOS must therefore evolve continuously.

---

# User Assumptions

---

## ASM-USR-001

The owner provides valid credentials.

---

## ASM-USR-002

The owner defines high-level objectives.

Example

```text
Grow Documentary Channel

rather than

Generate this exact title.
```

EvolutionOS determines implementation.

---

# 24. Risk Register

## 24.1 Purpose

Risk management is an architectural responsibility.

Every major risk should include:

* Identifier
* Description
* Likelihood
* Impact
* Mitigation
* Recovery Strategy

---

# RSK-001

## AI Provider Failure

Likelihood

Medium

Impact

High

Description

Primary AI provider becomes unavailable.

Mitigation

Provider abstraction layer.

Automatic fallback.

Recovery

Retry using secondary provider.

---

# RSK-002

## Knowledge Corruption

Likelihood

Low

Impact

Critical

Description

Knowledge database becomes inconsistent.

Mitigation

Versioned snapshots.

Integrity validation.

Append-only event history.

Recovery

Rollback to last verified snapshot.

Replay event log.

---

# RSK-003

## Poor Learning

Description

System repeatedly draws incorrect conclusions.

Mitigation

Reflection Engine.

Confidence decay.

Contradictory evidence handling.

Periodic self-evaluation.

---

# RSK-004

## Local Optimum

Description

EvolutionOS becomes trapped in one strategy and stops exploring.

Mitigation

Mandatory exploration rate.

Controlled mutations.

Randomized experiments.

---

# RSK-005

## Platform Algorithm Changes

Description

Execution platform changes ranking behavior.

Mitigation

Continuous experimentation.

Belief updates.

Trend detection.

---

# RSK-006

## Knowledge Explosion

Description

Knowledge base grows faster than practical management.

Mitigation

Knowledge consolidation.

Duplicate detection.

Hierarchical organization.

Knowledge graph indexing.

---

# RSK-007

## API Cost Escalation

Description

Increasing AI usage creates unacceptable operational cost.

Mitigation

Caching.

Model selection.

Task prioritization.

Token budgeting.

---

# RSK-008

## False Correlation

Description

System incorrectly assumes one variable caused success.

Mitigation

Controlled experiments.

Single-variable mutations where possible.

Statistical significance thresholds.

---

# Architecture Decision Record

## ADR-004 — Why Knowledge Is Immutable

### Context

Many systems overwrite old information when new data arrives.

### Decision

EvolutionOS treats historical knowledge as immutable evidence.

Knowledge is never rewritten.

Instead:

* New evidence is added.
* Beliefs are updated.
* Confidence changes.
* Historical records remain available.

### Rationale

This preserves the ability to audit learning over time, reproduce historical decisions, and understand why previous strategies were chosen.

### Consequences

Positive:

* Complete learning history.
* Strong auditability.
* Easier debugging.
* Better explainability.

Trade-offs:

* Larger storage requirements.
* Need for knowledge consolidation mechanisms.

---

At this point, **Volume 1 is approximately 90% complete**. The remaining sections will define:

* **Success Metrics (system intelligence KPIs, not just YouTube metrics)**
* **Acceptance Criteria**
* **Future Vision**
* **Appendix A: Requirement Index**
* **Appendix B: Complete Glossary**
* **Appendix C: Architecture Decision Register (ADR-001 through ADR-020 roadmap)**

Those final chapters will formally close the Foundation document and establish the baseline that all future volumes must follow.
Excellent. This is the final major chapter of **Volume 1**. After this, EvolutionOS has a complete constitutional document that every future volume must follow.

This section is one of the most important because it answers:

> **How do we know EvolutionOS is actually becoming more intelligent?**

Traditional software measures uptime and latency.

EvolutionOS must measure **intelligence growth**.

---

# 25. Success Metrics

## 25.1 Purpose

Success metrics define how the platform evaluates itself.

Unlike conventional software, EvolutionOS has two independent goals:

1. Operate reliably
2. Become more intelligent over time

Both must be measured independently.

---

# Metric Categories

```text
System Health
↓

Operational Success
↓

Knowledge Growth
↓

Decision Quality
↓

Experiment Quality
↓

Evolution Quality
↓

Business Outcome
```

The platform should never optimize only for business outcomes.

---

# 25.2 System Health Metrics

---

## KPI-SYS-001

Platform Availability

Definition

Percentage of scheduled evolution cycles completed successfully.

Target

> 99%

---

## KPI-SYS-002

Engine Health

Measure

Healthy

Degraded

Recovering

Failed

Each engine maintains an independent health score.

---

## KPI-SYS-003

Queue Completion Rate

Definition

Percentage of scheduled tasks completed without manual intervention.

---

## KPI-SYS-004

Recovery Time

Average recovery time after unexpected failure.

---

# 25.3 Knowledge Metrics

This category is unique.

Knowledge is the product.

---

## KPI-KNW-001

Knowledge Growth Rate

Measure

How much validated knowledge is created every week.

Formula

```text
Validated Rules Created

/

Week
```

---

## KPI-KNW-002

Knowledge Quality

Not all knowledge is valuable.

Each rule receives

Evidence Count

Confidence

Validation Count

Contradiction Count

Age

Usage Frequency

---

Knowledge Quality Score

```text
Confidence

×

Evidence

×

Validation

−

Contradictions
```

---

## KPI-KNW-003

Knowledge Reuse

Measure

How often previous knowledge contributes to future decisions.

High reuse indicates learning.

---

## KPI-KNW-004

Duplicate Knowledge

Percentage of duplicated knowledge.

Goal

As low as possible.

---

# 25.4 Belief Metrics

Beliefs are dynamic.

The platform measures their quality.

---

## KPI-BEL-001

Belief Stability

How often beliefs change.

Too stable

↓

No learning

Too unstable

↓

Poor reasoning

Healthy systems balance both.

---

## KPI-BEL-002

Confidence Calibration

Question

Does

90%

confidence actually succeed

90%

of the time?

If not

confidence estimates are inaccurate.

---

# 25.5 Decision Metrics

---

## KPI-DEC-001

Decision Accuracy

Prediction

↓

Reality

↓

Difference

The smaller the difference

the better the reasoning.

---

## KPI-DEC-002

Decision Explainability

Every decision should reference

Rules

Evidence

Confidence

Experiments

Reflection

Goal

100%

---

## KPI-DEC-003

Decision Consistency

Similar situations should produce similar reasoning.

Unexpected inconsistency indicates architectural problems.

---

# 25.6 Experiment Metrics

Experiments are the engine of evolution.

---

## KPI-EXP-001

Experiment Success Rate

Percentage of experiments producing useful learning.

Not

successful videos.

Successful learning.

---

## KPI-EXP-002

Learning Yield

Formula

```text
New Validated Rules

/

Experiment
```

Higher yield

means more learning.

---

## KPI-EXP-003

Mutation Effectiveness

Measures

How often mutations improve fitness.

---

## KPI-EXP-004

Hypothesis Accuracy

Question

How often was the prediction correct?

---

# 25.7 Evolution Metrics

This category measures whether EvolutionOS itself is evolving.

---

## KPI-EVO-001

Fitness Growth

Average fitness trend over time.

Expected

Positive.

---

## KPI-EVO-002

Prediction Improvement

Prediction error should decrease.

Month after month.

---

## KPI-EVO-003

Knowledge Efficiency

Less data

↓

Better decisions

Evolution should increase efficiency.

---

## KPI-EVO-004

Adaptation Speed

How quickly can the platform recover after

Algorithm changes

Audience changes

New niche

New provider

---

# 25.8 Business Metrics

Business metrics exist

but they are not the primary objective.

---

Examples

CTR

Retention

Subscribers

Views

Revenue

Returning Viewers

Watch Time

These are treated as evidence

not goals.

---

# 26. Acceptance Criteria

## Purpose

Acceptance Criteria define when EvolutionOS can be considered correctly implemented.

Every major subsystem should satisfy these criteria before release.

---

# AC-001

Knowledge survives restart.

---

# AC-002

Beliefs update automatically.

---

# AC-003

Every decision is explainable.

---

# AC-004

Every experiment generates reflection.

---

# AC-005

Historical knowledge remains accessible.

---

# AC-006

Multiple AI providers operate interchangeably.

---

# AC-007

Platform continues after provider failure.

---

# AC-008

Capabilities remain independent.

Replacing Story Engine

↓

Does not affect Learning Engine.

---

# AC-009

Execution platform can be replaced.

Example

Replace

YouTube

↓

Blog

without changing

Evolution Core.

---

# AC-010

Prediction accuracy improves over time.

If prediction accuracy becomes worse

Evolution has failed.

---

# AC-011

Knowledge quality increases continuously.

---

# AC-012

The platform requires no routine human operation after deployment.

---

# AC-013

Every experiment is reproducible.

Given the same historical knowledge

the reasoning path should be reconstructable.

---

# 27. Future Vision

EvolutionOS Version 1

YouTube

↓

Learns

↓

Improves

---

Version 2

Multi-platform

YouTube

Blog

Podcast

LinkedIn

TikTok

Instagram

---

Version 3

Business Intelligence

Marketing Optimization

SEO

Advertising

Sales Experiments

Website Optimization

---

Version 4

Scientific Research

Autonomous hypothesis generation

Literature review

Experiment planning

Result interpretation

Knowledge graph expansion

---

Version 5

General Evolution Platform

At this stage

EvolutionOS no longer specializes in content creation.

Instead

it becomes a reusable autonomous intelligence framework capable of learning from any measurable environment.

Possible execution environments include:

* Software engineering
* Financial forecasting
* Scientific experimentation
* Industrial optimization
* Robotics
* Education
* Healthcare decision support (subject to domain-specific validation and regulatory requirements)
* Business strategy

The same Evolution Core remains unchanged.

Only the execution layer changes.

---

# Final Architectural Principle

> **EvolutionOS is not software that creates content.**
>
> **It is software that learns from reality.**
>
> Content is only one of the environments in which it learns.

---

# Appendix A — Requirement Traceability Matrix (Template)

| Capability | Engine            | Requirement ID | Implementation         | Test Case  |
| ---------- | ----------------- | -------------- | ---------------------- | ---------- |
| Learn      | Knowledge Engine  | FR-001         | knowledge_service.py   | TC-KNW-001 |
| Learn      | Learning Engine   | FR-003         | lesson_generator.py    | TC-LRN-003 |
| Reason     | Decision Engine   | FR-010         | decision_engine.py     | TC-DEC-010 |
| Create     | Story Engine      | FR-014         | story_builder.py       | TC-STY-014 |
| Observe    | Analytics Engine  | FR-018         | analytics_collector.py | TC-OBS-018 |
| Evolve     | Experiment Engine | FR-021         | experiment_manager.py  | TC-EVO-021 |

Every implemented feature must map back to a requirement.

---

# Appendix B — Cognitive Architecture Summary

```text
                    EvolutionOS
                         │
               Cognitive Capabilities
                         │
 ┌────────┬────────┬────────┬────────┬────────┐
 │ Learn  │ Reason │ Create │Observe │Evolve  │
 └────────┴────────┴────────┴────────┴────────┘
                         │
                  Specialized Engines
                         │
        Knowledge • Learning • Reflection
        Belief • Decision • Strategy
        Research • Story • Visual
        Analytics • Trend • Competitor
        Experiment • Mutation • Fitness • Memory
                         │
                  Execution Environments
                         │
      YouTube → Blog → Podcast → Social → Future Domains
```

---

# Appendix C — Architecture Decision Register (Initial Index)

The following ADRs are defined in Volume 1 or will be expanded in later volumes:

* ADR-001 — Why Capabilities Instead of Services
* ADR-002 — Why Knowledge Is the Center of the Architecture
* ADR-003 — Why YouTube Is an Execution Environment
* ADR-004 — Why Knowledge Is Immutable
* ADR-005 — Why Every Decision Must Be Explainable
* ADR-006 — Why Experiments Are the Unit of Progress
* ADR-007 — Why Confidence Is Mandatory
* ADR-008 — Why Platform Independence Is a Core Requirement
* ADR-009 — Why Event-Driven Communication Is Preferred
* ADR-010 — Why Evolution Is Optimized Over Content Production
* ADR-011 to ADR-020 — Reserved for implementation-phase architectural decisions

---

## Volume 1 Status

At this point, **Volume 1 is complete as a foundational specification**.

One recommendation before moving to Volume 2: I think we should add one more foundational artifact that isn't typically part of an SRS but would be invaluable for this project—a **System Ontology**.

This would formally define every core concept (`Knowledge`, `Belief`, `Rule`, `Observation`, `Hypothesis`, `Experiment`, `Decision`, `Fitness`, etc.), their attributes, relationships, and lifecycle. It would become the canonical vocabulary for the database schema, APIs, prompts, documentation, and code, preventing different modules from using the same terms with different meanings. I believe that ontology will make the entire architecture significantly more coherent as the project grows.
# 📚 EvolutionOS Documentation Set — Volumes 2–5

---
---

# 02_EvolutionOS_SRS_Evolution_Core.md

# VOLUME 2 — EVOLUTION CORE

---

# 1. Evolution Core Overview

## 1.1 Purpose

The Evolution Core is the permanent, platform-independent intelligence of EvolutionOS.

It contains no knowledge of YouTube, videos, thumbnails, or any execution environment. It knows only:

* Observations
* Knowledge
* Beliefs
* Hypotheses
* Experiments
* Decisions
* Fitness

Everything else is a plugin.

## 1.2 Core Boundary Rule

### EC-BND-001

No Evolution Core module shall import, reference, or depend upon any execution-layer concept.

**Forbidden inside the Core:**

```
video, thumbnail, youtube, upload, render, scene, narration
```

**Permitted inside the Core:**

```
observation, evidence, belief, hypothesis, experiment,
decision, mutation, fitness, knowledge, strategy
```

### EC-BND-002

The Core communicates with execution layers exclusively through:

1. **Experiment Directives** (Core → Execution)
2. **Observation Events** (Execution → Core)

```text
┌─────────────────────────────┐
│       EVOLUTION CORE        │
│                             │
│  Learn Reason Evolve        │
└──────┬───────────────▲──────┘
       │               │
  Experiment      Observation
  Directives        Events
       │               │
┌──────▼───────────────┴──────┐
│      EXECUTION LAYER        │
│   (YouTube, Blog, Podcast)  │
└─────────────────────────────┘
```

---

# 2. Cognitive Architecture

## 2.1 Layered Model

```text
Layer 5   GOVERNANCE          (policies, ethics, overrides)
Layer 4   EVOLUTION           (experiment, mutation, fitness)
Layer 3   REASONING           (belief, decision, strategy)
Layer 2   LEARNING            (knowledge, lessons, reflection)
Layer 1   PERCEPTION          (observations, normalization)
Layer 0   MEMORY SUBSTRATE    (event store, knowledge graph)
```

### EC-ARC-001

Dependencies shall flow downward only. Layer 3 may use Layer 2; Layer 2 may never use Layer 3.

### EC-ARC-002

Layer 0 (Memory Substrate) is the only layer permitted to perform persistence operations.

---

# 3. Capability Hierarchy

```text
EvolutionOS Core
│
├── LEARN
│   ├── Knowledge Engine        (store, index, retrieve)
│   ├── Learning Engine         (extract lessons from evidence)
│   └── Reflection Engine       (predicted vs actual analysis)
│
├── REASON
│   ├── Belief Engine           (confidence-weighted world model)
│   ├── Decision Engine         (candidate ranking, selection)
│   └── Strategy Engine         (long-horizon planning)
│
├── OBSERVE  (core-side)
│   ├── Observation Gateway     (ingestion, validation)
│   └── Signal Classifier       (feedback levels 1–5)
│
└── EVOLVE
    ├── Experiment Engine       (lifecycle management)
    ├── Hypothesis Engine       (falsifiable predictions)
    ├── Mutation Engine         (controlled variation)
    ├── Fitness Engine          (multi-objective scoring)
    └── Memory Engine           (consolidation, decay)
```

Note: **Create** and the collection side of **Observe** live in the Execution Layer (Volume 3). The Core only consumes normalized observations.

---

# 4. Domain Architecture

## 4.1 Bounded Contexts

| Context         | Aggregate Roots        | Owns                            |
| --------------- | ---------------------- | ------------------------------- |
| Perception      | Observation            | Raw & normalized evidence       |
| Knowledge       | KnowledgeRecord, Rule  | Immutable learning artifacts    |
| Belief          | Belief                 | Confidence-weighted conclusions |
| Experimentation | Experiment, Hypothesis | Scientific method lifecycle     |
| Decision        | Decision               | Choices + full reasoning trace  |
| Strategy        | Strategy               | Multi-experiment plans          |
| Fitness         | FitnessRecord          | Multi-objective evaluation      |

### EC-DOM-001

Each bounded context owns its data exclusively. Cross-context access occurs only through events or query interfaces — never direct table/collection access.

---

# 5. Learn Capability — Detailed Specification

## 5.1 Knowledge Engine

### FR-EC-101 — Knowledge Record Structure

Every knowledge record shall contain:

```yaml
KnowledgeRecord:
  id: UUID                    # globally unique
  type: enum                  # FACT | PATTERN | RULE | LESSON
  statement: string           # human-readable claim
  scope: ScopeDescriptor      # niche, format, audience, platform
  evidence_refs: [UUID]       # observations supporting this
  contradiction_refs: [UUID]  # observations contradicting this
  confidence: float           # 0.0–1.0, derived, never manual
  created_at: timestamp
  last_validated_at: timestamp
  validation_count: int
  status: enum                # CANDIDATE | ACTIVE | DEPRECATED | ARCHIVED
  provenance: ProvenanceChain # which experiment/reflection created it
```

### FR-EC-102 — Immutability

Knowledge records are append-only. Status transitions create new versions linked via `supersedes: UUID`. (Enforces ADR-004, DP-009.)

### FR-EC-103 — Retrieval Contract

The Knowledge Engine shall support:

* `query_by_scope(scope, min_confidence)` — indexed
* `query_related(knowledge_id, depth)` — graph traversal
* `query_contradictions(knowledge_id)`
* `query_for_decision(decision_context)` — relevance-ranked

### FR-EC-104 — Consolidation

When two records exceed a configurable similarity threshold (default 0.85 semantic similarity), the engine shall create a consolidated record referencing both, marking originals `ARCHIVED` — never deleted.

## 5.2 Learning Engine

### FR-EC-110 — Lesson Extraction Pipeline

```text
Completed Experiment
        │
        ▼
Gather: hypothesis + prediction + observations
        │
        ▼
Compute: outcome delta (predicted vs actual)
        │
        ▼
Attribute: which mutated variable(s) explain delta
        │
        ▼
Generate: candidate lessons (min 1, max configurable)
        │
        ▼
Score: statistical support (sample size, variance)
        │
        ▼
Emit: LessonExtracted event → Knowledge Engine
```

### FR-EC-111 — Statistical Guardrails

A lesson may only reach `ACTIVE` status when:

* Supporting experiments ≥ `min_evidence_count` (default: 3)
* Effect size exceeds `noise_floor` (configurable per metric)
* No unresolved contradiction with confidence > own confidence

### FR-EC-112 — Contradiction Handling

Contradictory evidence shall never be discarded. It shall:

1. Attach to the affected record
2. Trigger confidence recalculation
3. If confidence drops below `deprecation_threshold` (default 0.35), transition record to `DEPRECATED`
4. Emit `BeliefRevisionRequired` event

## 5.3 Reflection Engine

### FR-EC-120 — Mandatory Reflection

Every experiment reaching terminal state shall produce exactly one ReflectionReport (enforces DP-012):

```yaml
ReflectionReport:
  experiment_id: UUID
  prediction: PredictionRecord
  actual: OutcomeRecord
  delta: DeltaAnalysis          # per-metric divergence
  surprise_score: float          # 0 = fully expected, 1 = fully unexpected
  attribution: [AttributionClaim]
  lessons_proposed: [UUID]
  calibration_impact: CalibrationDelta
  meta_notes: string             # observations about the learning process itself
```

### FR-EC-121 — Surprise Prioritization

High surprise scores (default > 0.6) shall be prioritized in the learning queue. Surprise is where the most learning value lives.

### FR-EC-122 — Meta-Reflection

Every N experiments (default: 20), the Reflection Engine shall perform meta-reflection: evaluating trends in prediction accuracy, calibration drift, and lesson yield. Output feeds NFR-AUT-003 (self-evaluation).

---

# 6. Reason Capability — Detailed Specification

## 6.1 Belief Engine

### FR-EC-201 — Belief Structure

```yaml
Belief:
  id: UUID
  statement: string
  scope: ScopeDescriptor
  confidence: float
  derived_from: [KnowledgeRecord.id]
  prior_confidence_history: [ConfidencePoint]  # full time series
  stability_score: float        # volatility measure
  last_challenged_at: timestamp
  status: ACTIVE | SUSPENDED | RETIRED
```

### FR-EC-202 — Confidence Update Function

Confidence updates shall use a Bayesian-inspired update:

```text
posterior = prior + learning_rate × (evidence_weight × direction − prior_pull)

where:
  evidence_weight  = f(sample_size, effect_size, recency)
  direction        = +1 supporting | −1 contradicting
  prior_pull       = regularization toward 0.5 when unvalidated
  learning_rate    = configurable, per belief type
```

Exact function is an implementation detail; requirements are:

* Monotonic in evidence direction
* Bounded (0.01, 0.99) — never certainty (CON-ETH-003)
* Recency-weighted
* Fully logged (every update produces a `ConfidenceUpdated` event)

### FR-EC-203 — Belief Decay

Beliefs unvalidated for `decay_window` (default: 90 days) shall decay toward 0.5 at a configurable rate, and emit `BeliefStale` events prompting validation experiments.

## 6.2 Decision Engine

### FR-EC-210 — Decision Protocol

Every strategic decision shall follow this mandatory protocol:

```text
1. FRAME       Define the decision context and objective
2. RETRIEVE    Query relevant knowledge + beliefs (ranked)
3. GENERATE    Produce ≥ 3 candidates (FR-013 generalized)
4. SCORE       Multi-criteria scoring per candidate
5. RISK        Compute risk score per candidate (FR-011)
6. SELECT      Choose per active policy (exploit vs explore)
7. RECORD      Persist full DecisionRecord
8. PREDICT     Attach measurable predicted outcome
```

### FR-EC-211 — DecisionRecord

```yaml
DecisionRecord:
  id: UUID
  context: DecisionContext
  candidates: [Candidate]          # ALL, including rejected
  scores: [CandidateScore]
  knowledge_used: [UUID]
  beliefs_used: [UUID]
  policy: EXPLOIT | EXPLORE | FORCED_EXPLORE
  selected: Candidate.id
  rejection_reasons: map<Candidate.id, string>
  risk_score: float
  prediction: PredictionRecord
  timestamp: timestamp
```

### FR-EC-212 — Exploration Policy

The Decision Engine shall enforce a minimum exploration rate (default: 15% of decisions) selecting non-optimal candidates deliberately, mitigating RSK-004 (local optimum).

Exploration rate shall be adaptive:

```text
IF fitness plateau detected (KPI-EVO-001 flat over window)
   → increase exploration rate
IF fitness volatile
   → decrease exploration rate
```

## 6.3 Strategy Engine

### FR-EC-220 — Strategy Structure

A Strategy is a multi-experiment plan pursuing a long-horizon objective:

```yaml
Strategy:
  id: UUID
  objective: string
  horizon: int                    # planned experiment count
  hypothesis_backlog: [UUID]
  active_experiments: [UUID]
  fitness_trend: [FitnessPoint]
  expiration: ExpirationPolicy    # every strategy expires (QA-002)
  status: DRAFT | ACTIVE | UNDER_REVIEW | RETIRED
```

### FR-EC-221 — Strategy Review Trigger

Strategies shall be automatically reviewed when any of:

* Fitness trend negative over `review_window`
* ≥ 3 constituent hypotheses falsified
* Environment shift detected (Level 5 feedback)
* Expiration reached

---

# 7. Observe Capability (Core-Side)

## 7.1 Observation Gateway

### FR-EC-301 — Normalized Observation Schema

All execution layers must submit observations in the canonical schema:

```yaml
Observation:
  id: UUID
  experiment_id: UUID
  source: string                # "youtube", "blog", ...
  metric: string                # canonical metric name
  value: numeric | structured
  unit: string
  measured_at: timestamp
  collection_window: Duration
  quality: QualityDescriptor    # completeness, reliability flags
```

### FR-EC-302 — Validation Rules

The Gateway shall reject or quarantine observations that:

* Reference unknown experiments
* Contain impossible values (e.g., CTR > 100%)
* Arrive outside plausible time windows
* Fail schema validation

Quarantined observations generate alerts, never silent drops.

## 7.2 Signal Classifier

### FR-EC-310

Every accepted observation shall be classified into feedback levels 1–5 (per Volume 1 §16.3) and routed:

| Level          | Routed To                             |
| -------------- | ------------------------------------- |
| 1 Operational  | Platform health (Volume 4 monitoring) |
| 2 Performance  | Fitness Engine + Reflection Engine    |
| 3 Behavioral   | Learning Engine (pattern extraction)  |
| 4 Strategic    | Strategy Engine + Belief Engine       |
| 5 Evolutionary | Meta-Reflection + Self-Optimization   |

---

# 8. Evolve Capability — Detailed Specification

## 8.1 Experiment Engine

### FR-EC-401 — Experiment Lifecycle State Machine

```text
DRAFT ──► HYPOTHESIZED ──► APPROVED ──► SCHEDULED ──► EXECUTING
                                                         │
                              ┌──────────────────────────┤
                              ▼                          ▼
                          FAILED                     MEASURING
                              │                          │
                              ▼                          ▼
                         REFLECTED ◄───────────────  COMPLETED
                              │
                              ▼
                          ARCHIVED
```

State rules:

* No experiment may reach `SCHEDULED` without an attached, falsifiable Hypothesis (FR-009)
* `FAILED` experiments still require reflection (failure is evidence)
* `ARCHIVED` is terminal and permanent (FR-023)

### FR-EC-402 — Experiment Record

```yaml
Experiment:
  id: UUID
  strategy_id: UUID
  hypothesis_id: UUID
  baseline_ref: UUID | null      # what it is compared against
  mutations: [Mutation]          # ideally length 1 (DP-011)
  directive: ExperimentDirective # instructions for execution layer
  predicted: PredictionRecord
  measurement_plan: MeasurementPlan
  state: <state machine above>
  risk_score: float
```

## 8.2 Hypothesis Engine

### FR-EC-410 — Falsifiability Requirement

Every hypothesis shall be expressed in the canonical falsifiable form:

```text
IF   <variable> is changed from <A> to <B>
IN   <scope>
THEN <metric> will change by <direction + magnitude>
WITHIN <measurement window>
WITH  expected confidence <x%>
```

A hypothesis lacking any element shall be rejected at validation.

### FR-EC-411 — Hypothesis Sources

Hypotheses shall be generated from (priority order):

1. Belief validation needs (stale/low-confidence beliefs)
2. Contradiction resolution
3. Strategic objectives
4. Surprise investigation (high surprise reflections)
5. Structured exploration (novelty search)

## 8.3 Mutation Engine

### FR-EC-420 — Mutation Taxonomy

```text
MutationClass
├── TOPIC        (subject matter variation)
├── STRUCTURE    (narrative/format variation)
├── PRESENTATION (hook, title, visual style)
├── TIMING       (schedule, cadence)
├── SCOPE        (niche, audience, length)
└── META         (mutation of the learning process itself)
```

### FR-EC-421 — Mutation Budget

Each experiment shall declare a mutation budget. Default: 1 mutation. Exceeding budget requires explicit justification recorded in the DecisionRecord (DP-011, RSK-008).

### FR-EC-422 — Mutation Distance

Every mutation shall record a `distance` score (how far from validated territory). Portfolio constraint: the active experiment set shall maintain a configurable distribution across distances (e.g., 70% near, 25% mid, 5% far).

## 8.4 Fitness Engine

### FR-EC-430 — Multi-Objective Fitness

Fitness is never a single number internally. It is a vector, reduced to a scalar only for ranking:

```yaml
FitnessVector:
  learning_yield: float       # validated lessons per experiment
  prediction_accuracy: float
  performance_delta: float    # vs baseline, per Level-2 metrics
  strategic_alignment: float
  cost_efficiency: float

FitnessScore: weighted_sum(FitnessVector, active_weight_profile)
```

### FR-EC-431 — Weight Profiles

Weight profiles are versioned configuration. Changing weights is itself an evolutionary event, recorded in the Evolution Timeline (FR-024).

### FR-EC-432 — Anti-Gaming Rule

`learning_yield` shall be computed only from lessons that later achieve `ACTIVE` status, preventing the system from inflating fitness by producing junk lessons.

## 8.5 Memory Engine

### FR-EC-440 — Consolidation Cycle

On a configurable schedule (default: daily), the Memory Engine shall:

1. Detect duplicate/similar knowledge → consolidate (FR-006)
2. Apply confidence decay to stale items (FR-007)
3. Recompute knowledge graph indexes
4. Produce a MemoryHealthReport

### FR-EC-441 — Forgetting Policy

Nothing is deleted. "Forgetting" = `ARCHIVED` status + removal from active retrieval indexes. Archived knowledge remains queryable for audit.

---

# 9. Cross-Capability Communication

## 9.1 Domain Event Architecture

### EC-EVT-001

All inter-context communication shall use domain events published to the event bus. Direct method calls across bounded contexts are prohibited (NFR-MNT-003, CON-TEC-004).

### 9.2 Core Event Catalog

| Event                       | Producer            | Primary Consumers                |
| --------------------------- | ------------------- | -------------------------------- |
| `ObservationReceived`       | Observation Gateway | Signal Classifier                |
| `ObservationClassified`     | Signal Classifier   | Per-level routing                |
| `ExperimentCompleted`       | Experiment Engine   | Reflection Engine                |
| `ReflectionProduced`        | Reflection Engine   | Learning Engine, Fitness Engine  |
| `LessonExtracted`           | Learning Engine     | Knowledge Engine                 |
| `KnowledgeActivated`        | Knowledge Engine    | Belief Engine                    |
| `BeliefRevised`             | Belief Engine       | Decision Engine, Strategy Engine |
| `BeliefStale`               | Belief Engine       | Hypothesis Engine                |
| `HypothesisProposed`        | Hypothesis Engine   | Decision Engine                  |
| `ExperimentDirectiveIssued` | Experiment Engine   | Execution Layer                  |
| `StrategyRevised`           | Strategy Engine     | Experiment Engine                |
| `FitnessComputed`           | Fitness Engine      | Strategy Engine, Meta-Reflection |
| `SelfEvaluationTriggered`   | Meta-Reflection     | Governance (Vol 5)               |

### EC-EVT-002 — Event Envelope

```yaml
EventEnvelope:
  event_id: UUID
  event_type: string
  occurred_at: timestamp
  correlation_id: UUID     # traces a full evolution cycle
  causation_id: UUID       # event that caused this event
  producer: EngineID
  schema_version: semver
  payload: <typed body>
```

`correlation_id` enables full reconstruction of any reasoning chain (FR-012, NFR-EXP-003).

---

# 10. Event Sourcing & CQRS

## ADR-011 — Event Sourcing for the Evolution Core

### Context
The Core requires: immutable history (ADR-004), decision reproducibility (AC-013), and experiment replay (NFR-TST-003).

### Decision
The Evolution Core shall use **event sourcing** as its persistence model. Current state (beliefs, knowledge status, experiment states) is a projection of the event log.

### Consequences
Positive: perfect audit trail, time-travel debugging, replay-based regression testing, natural fit with immutability constraints.
Trade-off: projection complexity, eventual consistency between write and read models.

## ADR-012 — CQRS Separation

Write model: aggregates validating commands, emitting events.
Read models (projections):

* **Knowledge Graph projection** — relationship queries
* **Decision Trace projection** — explainability queries (dashboard)
* **Fitness Timeline projection** — trend analysis
* **Belief Snapshot projection** — fast decision-time retrieval

### EC-CQRS-001
Read models are disposable and rebuildable from the event log at any time. This is verified by a scheduled rebuild test (Volume 4).

---

# 11. Aggregate Design

| Aggregate       | Invariants Enforced                                                            |
| --------------- | ------------------------------------------------------------------------------ |
| Experiment      | State machine legality; hypothesis attached before scheduling; mutation budget |
| Belief          | Confidence bounds; update provenance; decay rules                              |
| KnowledgeRecord | Immutability; status transitions; evidence linkage                             |
| Strategy        | Expiration; review triggers                                                    |
| Decision        | Candidate minimum; complete reasoning trace before selection commits           |

### EC-AGG-001
Aggregates shall be small. Cross-aggregate consistency is eventual, coordinated by process managers (sagas) — e.g., the **EvolutionCycleSaga** (§13).

---

# 12. Shared Data Model (Core Ontology Reference)

The canonical ontology is defined in Volume 5, Appendix C. The Core implements these entity types:

```text
Observation ──evidence-for──► KnowledgeRecord ──derives──► Belief
      │                             │                        │
      │                             ▼                        ▼
      └──measured-by──► Experiment ◄──validates── Hypothesis ◄─ generated-from
                            │
                            ▼
                     ReflectionReport ──proposes──► Lesson (KnowledgeRecord)
                            │
                            ▼
                      FitnessRecord ──informs──► Strategy ──plans──► Experiment
```

---

# 13. Global Evolution Cycle (Orchestration)

## FR-EC-501 — EvolutionCycleSaga

The full cycle is coordinated by a long-running saga:

```text
CYCLE START
  1. Memory Engine: consolidation pass
  2. Belief Engine: decay + stale detection
  3. Hypothesis Engine: generate/refresh backlog
  4. Strategy Engine: review active strategies
  5. Decision Engine: select next experiments (explore/exploit)
  6. Experiment Engine: issue directives → Execution Layer
  7. [Execution Layer runs — outside Core]
  8. Observation Gateway: ingest results
  9. Reflection Engine: reflect on completed experiments
 10. Learning Engine: extract lessons
 11. Fitness Engine: score
 12. Meta check: every Nth cycle → self-evaluation
CYCLE END → emit CycleCompleted → schedule next cycle
```

## FR-EC-502 — Cycle Resumability

The saga persists its position. After crash/restart, the cycle resumes from the last completed step (NFR-AVA-002).

## FR-EC-503 — Concurrent Cycles

Multiple experiments may be in-flight simultaneously; the saga manages a portfolio, not a single linear pipeline.

---

# 14. Core State Machines (Summary)

| Entity          | States                                                                                                        |
| --------------- | ------------------------------------------------------------------------------------------------------------- |
| Experiment      | DRAFT → HYPOTHESIZED → APPROVED → SCHEDULED → EXECUTING → MEASURING → COMPLETED/FAILED → REFLECTED → ARCHIVED |
| KnowledgeRecord | CANDIDATE → ACTIVE → DEPRECATED → ARCHIVED                                                                    |
| Belief          | ACTIVE ⇄ SUSPENDED → RETIRED                                                                                  |
| Strategy        | DRAFT → ACTIVE → UNDER_REVIEW → (ACTIVE \| RETIRED)                                                           |
| EvolutionCycle  | steps 1–12 with checkpoint persistence                                                                        |

All state transitions emit events. Illegal transitions are aggregate-level errors, logged and alerted.

---

# 15. Core Metrics

The Core exposes (feeding Volume 1 KPIs):

```text
core.knowledge.records_total{status}
core.knowledge.consolidations_total
core.beliefs.confidence_histogram
core.beliefs.stability_score
core.decisions.latency_seconds        (NFR-PERF-001)
core.decisions.exploration_ratio
core.experiments.by_state
core.experiments.learning_yield
core.reflection.surprise_histogram
core.prediction.error_trend           (KPI-EVO-002)
core.calibration.error                (KPI-BEL-002)
core.cycle.duration_seconds
core.eventstore.append_latency
```

---

# 16. Core Security

* EC-SEC-001: Core APIs are internal-only; never exposed to public networks. All external access flows through the API Gateway (Volume 3).
* EC-SEC-002: Event store writes require service identity authentication.
* EC-SEC-003: Governance override commands (pause/rollback, DP-014) require elevated credentials and produce immutable audit events (NFR-SEC-004).

---

# 17. Core Testing

| Test Type      | Target                                                                                           |
| -------------- | ------------------------------------------------------------------------------------------------ |
| Unit           | Every aggregate invariant, confidence math, fitness math                                         |
| Property-based | Confidence update function (bounds, monotonicity)                                                |
| Event replay   | Rebuild projections from historical log; assert identical state (AC-013)                         |
| Simulation     | Synthetic environment with known ground-truth rules — verify the Core discovers them (see below) |
| Regression     | Replay historical experiments after code changes (NFR-TST-003)                                   |

## FR-EC-601 — Simulation Harness (Critical)

The Core shall include a simulation environment with **planted ground-truth rules** (e.g., "format A yields +10% on metric X"). Acceptance: the Core must discover ≥ 80% of planted rules within a bounded number of simulated cycles, with calibrated confidence. This is the primary intelligence verification mechanism before real-world deployment.

---

# 18. Core Extension Framework

### EC-EXT-001
New engines register via a manifest declaring: capability served, events consumed, events produced, health endpoint.

### EC-EXT-002
The event catalog is versioned. New engines may add event types; changing existing payloads requires schema versioning with dual-read migration windows.

---
---

# 03_EvolutionOS_SRS_Platform_Execution.md

# VOLUME 3 — PLATFORM & EXECUTION LAYER

---

# 1. Platform Layer Overview

The Execution Layer translates abstract **Experiment Directives** from the Core into real-world actions, and returns normalized **Observations**.

```text
ExperimentDirective (abstract)
        │
        ▼
┌─────────────────────────────┐
│    WORKFLOW ORCHESTRATOR    │
└──────────────┬──────────────┘
               ▼
   Research → Story → Script → Narration
      → Visual Plan → Composition
      → Thumbnail → Publish
               │
               ▼
       Platform Adapter (YouTube v1)
               │
               ▼
        Analytics Collection
               │
               ▼
     Observation Normalizer → Core Gateway
```

### PX-001
The Execution Layer shall be fully replaceable without Core changes (AC-009).

### PX-002
The Execution Layer holds **no beliefs and makes no strategic decisions**. Tactical decisions (e.g., retry a render) are permitted; strategic decisions (e.g., which topic) are not.

---

# 2. Execution Layer Architecture

## 2.1 Directive Contract

```yaml
ExperimentDirective:
  experiment_id: UUID
  content_spec:
    topic_candidates: [TopicSpec]      # Core-ranked
    narrative_structure: StructureSpec # hook/context/conflict/... (FR-014)
    hook_strategy: HookSpec
    visual_strategy: VisualSpec        # documentary|maps|motion|... (FR-015)
    length_target: Duration
    title_candidates: [TitleSpec]
    thumbnail_strategy: ThumbSpec
  publishing_spec:
    platform: "youtube"
    schedule: SchedulePolicy
  measurement_plan:
    metrics: [MetricSpec]
    windows: [Duration]                # e.g., 24h, 72h, 7d, 28d
  constraints:
    budget: ResourceBudget
    approval_required: bool            # human-in-loop flag
```

### PX-003
The directive is the **only** input to the pipeline. If information is missing, the pipeline fails fast rather than improvising strategy.

---

# 3. Workflow Orchestrator

### FR-PX-101 — Pipeline as State Machine

```text
RECEIVED → RESEARCHING → STORY_DRAFTED → SCRIPTED
   → NARRATED → VISUALS_PLANNED → COMPOSING
   → THUMBNAIL_READY → AWAITING_APPROVAL?
   → PUBLISHING → PUBLISHED → MEASURING → REPORTED
```

### FR-PX-102 — Checkpointing
Every stage persists its output artifact reference before advancing. Crash recovery resumes from the last checkpoint (NFR-AVA-002 — never restart from scratch).

### FR-PX-103 — Stage Contracts
Each stage declares: input schema, output schema, timeout, retry policy, fallback behavior, and resource cost estimate.

### FR-PX-104 — Parallelization
Independent stages (e.g., thumbnail generation and narration) shall run concurrently (NFR-PERF-003).

### FR-PX-105 — Budget Enforcement
The orchestrator tracks cumulative cost (tokens, API calls, compute) against `ResourceBudget` and halts with a `BudgetExceeded` event rather than overspending (CON-FIN-002).

---

# 4. Research Pipeline

### FR-PX-201 — Multi-Source Research
The Research Engine aggregates from pluggable providers (QA-004): web search, Wikipedia, news APIs, academic sources. Provider list is configuration, not code.

### FR-PX-202 — Fact Ledger
All claims intended for the script shall be recorded in a Fact Ledger:

```yaml
Fact:
  claim: string
  sources: [SourceRef]        # ≥ 1 required
  source_tier: PRIMARY | SECONDARY | WEAK
  verification: CORROBORATED | SINGLE_SOURCE | DISPUTED
```

### FR-PX-203 — Hallucination Defense
No LLM-generated claim enters the script unless it exists in the Fact Ledger with at least `SINGLE_SOURCE` status (ASM-AI-004). Disputed facts require corroboration or exclusion.

### FR-PX-204 — Research Output
Structured ResearchDossier: verified facts, narrative angles, key entities, timeline, open questions — passed to Story Engine.

---

# 5. Story Generation Pipeline

### FR-PX-301 — Structure Compliance
Every story shall implement the directive's `StructureSpec` (default: Hook → Context → Conflict → Development → Resolution → Reflection, per FR-014).

### FR-PX-302 — Multi-Candidate Generation
The Story Engine generates ≥ 3 story treatments, scored against:

* Structure adherence
* Fact Ledger coverage (no unsupported claims)
* Hook strength heuristics (from Core-provided knowledge, passed in directive)
* Pacing profile

### FR-PX-303 — Retention-Aware Pacing
Each story is annotated with a pacing map (predicted attention curve segments), later compared against actual retention curves — producing Level-3 behavioral feedback.

---

# 6. Script Engine

### FR-PX-401 — Scene Decomposition
Scripts are decomposed into scenes:

```yaml
Scene:
  id: int
  narration_text: string
  duration_estimate: seconds
  visual_intent: VisualIntent    # what should be on screen
  emphasis: NORMAL | HIGH
  fact_refs: [Fact.id]           # traceability to ledger
```

### FR-PX-402 — Readability Constraints
Narration text shall satisfy configurable constraints: sentence length distribution, reading level, forbidden-phrase list, pronunciation annotations for TTS.

---

# 7. Narration Engine

### FR-PX-501 — TTS Provider Abstraction
Multiple TTS providers behind a common interface; provider selection by config + fallback chain (NFR-REL-003).

### FR-PX-502 — Quality Gate
Generated audio shall pass automated checks: duration vs estimate (±15%), silence detection, clipping detection, loudness normalization (EBU R128 target).

### FR-PX-503 — Regeneration Granularity
Failed audio regenerates per-scene, never full-script (cost efficiency).

---

# 8. Visual Planning Engine

### FR-PX-601 — Strategy Execution
The engine implements the directive's `VisualSpec` (documentary/maps/timelines/motion/stock/hybrid — FR-015). It does not choose the strategy; the Core did.

### FR-PX-602 — Shot List
Output is a deterministic ShotList mapping every scene to concrete visual assets:

```yaml
Shot:
  scene_id: int
  asset_type: STOCK | GENERATED | MAP | CHART | TEXT_CARD
  asset_query_or_spec: string
  duration: seconds
  transition: TransitionSpec
  license_requirement: LicenseClass
```

### FR-PX-603 — License Compliance
Every asset shall carry license metadata. Assets without verifiable licenses compatible with commercial publication are rejected (CON-ETH-001).

---

# 9. Video Composition Engine

### FR-PX-701 — Declarative Composition
Composition consumes ShotList + narration audio and renders deterministically. Same inputs → same output (reproducibility).

### FR-PX-702 — Render Profiles
Configurable profiles (resolution, bitrate, codec). Default targets platform-recommended specs.

### FR-PX-703 — Resource-Aware Rendering
Rendering respects host resource limits; on constrained hosts (CON-INF-001), rendering runs at reduced priority and may be time-shifted to low-load windows.

### FR-PX-704 — Validation
Post-render checks: duration match, audio sync drift < 50ms, black-frame detection, corrupt-file detection.

---

# 10. Thumbnail Engine

### FR-PX-801
Generates N thumbnail candidates per `ThumbSpec` (composition rules, text overlay policies, face/subject prominence heuristics from Core knowledge).

### FR-PX-802
Candidates are ranked by the Core's Decision Engine (via a synchronous evaluation request) — the Execution Layer never self-selects when strategy is involved.

### FR-PX-803
Where the platform supports it (YouTube A/B thumbnail testing), the adapter shall exploit native experimentation features and report per-variant metrics.

---

# 11. Publishing Engine

### FR-PX-901
Publishing executes the `SchedulePolicy`: immediate, scheduled slot, or optimal-window (window computed by Core knowledge, passed in directive).

### FR-PX-902 — Idempotency
Publish operations are idempotent; retries never create duplicate publications.

### FR-PX-903 — Metadata Assembly
Title, description, tags, chapters, end screens assembled from directive + templates. All metadata recorded to the experiment record.

### FR-PX-904 — Rollback Awareness
Where platform permits (unlisting/deleting), the engine supports governance-triggered rollback (DP-014).

---

# 12. Multi-Platform Adapters

## 12.1 Adapter Contract

Every platform adapter implements:

```text
PlatformAdapter:
  capabilities() → CapabilityManifest    # what it supports
  publish(artifact, metadata, schedule) → PublicationRef
  collect_metrics(ref, window) → [RawMetric]
  supports_native_ab() → bool
  rollback(ref) → Result
  health() → HealthStatus
```

### FR-PX-1001
Adding a new platform = implementing this contract + a metric mapping table. Zero Core changes (AC-009), zero orchestrator changes.

## 12.2 Metric Normalization

### FR-PX-1002
Each adapter ships a mapping from platform-native metrics to canonical Core metrics:

| Canonical         | YouTube             | Blog (future)   | Podcast (future) |
| ----------------- | ------------------- | --------------- | ---------------- |
| `attention_rate`  | Avg view duration % | Scroll depth    | Completion %     |
| `selection_rate`  | CTR                 | SERP/social CTR | Play rate        |
| `audience_growth` | Subscribers         | Email signups   | Followers        |
| `engagement`      | Likes+comments      | Comments/shares | Reviews          |

This mapping is what makes cross-platform knowledge transfer possible.

---

# 13. Scheduling Engine

* FR-PX-1101: Cron-like recurring jobs + one-shot scheduled jobs, persisted (survive restart).
* FR-PX-1102: Missed-job detection with catch-up policy per job class (NFR-AVA-001).
* FR-PX-1103: Priority classes — evolution-cycle jobs preempt maintenance jobs.

---

# 14. Asset Management

* FR-PX-1201: Content-addressed storage (hash-based) for all assets; automatic dedup.
* FR-PX-1202: Retention policy: intermediate artifacts (raw clips, temp renders) garbage-collected per configurable TTL; final artifacts + provenance retained (CON-FIN-003).
* FR-PX-1203: Every artifact links back to experiment_id (traceability).

---

# 15. AI Provider Management

### FR-PX-1301 — Provider Abstraction Layer

```text
LLMRequest → Router → [Provider Pool]
                        ├── selection by: task_class, cost, latency, health
                        ├── fallback chain (NFR-REL-003)
                        ├── rate limiting per provider
                        └── response validation
```

### FR-PX-1302 — Task Classes
Requests declare a task class (`REASONING_HEAVY`, `GENERATION_BULK`, `CLASSIFICATION_CHEAP`, ...). Routing policy maps classes to provider tiers (expensive models only where justified — CON-FIN-002).

### FR-PX-1303 — Caching
Deterministic-intent requests (embeddings, classifications of identical input) are cached (RSK-007 mitigation).

### FR-PX-1304 — Cost Ledger
Every request logs: provider, model, tokens in/out, cost estimate, task class, experiment_id. Aggregated into per-experiment cost (feeds FitnessVector.cost_efficiency).

---

# 16. Prompt Management

### FR-PX-1401 — Prompts as Versioned Artifacts
All prompts live in a registry with: semver version, task class, model compatibility list, evaluation scores, changelog (ASM-AI-003).

### FR-PX-1402 — Prompt Experiments
Prompt changes are themselves experiments: new versions are canary-tested against evaluation sets before promotion. Prompt performance regressions trigger automatic rollback to prior version.

### FR-PX-1403 — Output Contracts
Every prompt declares its expected output schema. Responses are validated; schema violations trigger structured-repair retry, then fallback provider, then failure.

---

# 17. Human Approval Framework

### FR-PX-1501 — Approval Modes

| Mode           | Behavior                                                 |
| -------------- | -------------------------------------------------------- |
| `AUTONOMOUS`   | No human gate (target state, NFR-AUT-001)                |
| `NOTIFY`       | Publish + notify owner                                   |
| `GATED`        | Hold at `AWAITING_APPROVAL` until approve/reject/timeout |
| `GATED_STRICT` | Hold indefinitely                                        |

### FR-PX-1502 — Progressive Autonomy
Default rollout: start `GATED`, and the system shall recommend transition to `NOTIFY`/`AUTONOMOUS` when its approval-prediction accuracy exceeds threshold (i.e., it learns to predict what the owner would reject — those rejections are Level-4 feedback).

### FR-PX-1503
Owner can always: pause, resume, approve, reject, rollback (DP-014). All such actions produce audit events.

---

# 18. Dashboard Architecture

## 18.1 Views

| View                   | Content                                                                         |
| ---------------------- | ------------------------------------------------------------------------------- |
| **Evolution Overview** | Fitness trend, knowledge growth, prediction accuracy, cycle status              |
| **Experiment Board**   | Kanban of experiments by state; drill-down to full record                       |
| **Decision Explorer**  | Any decision → candidates, evidence, confidence, rejections (QA-001 acceptance) |
| **Knowledge Browser**  | Search/graph-navigate knowledge; confidence histories                           |
| **Belief Inspector**   | Active beliefs, stability, calibration                                          |
| **Pipeline Monitor**   | Live workflow states, stage timings, failures                                   |
| **Cost Center**        | Provider spend, per-experiment cost, budget burn                                |
| **System Health**      | Engine health matrix, queues, resources (NFR-OBS-003)                           |
| **Approval Inbox**     | Pending gated items with full context                                           |

### FR-PX-1601
The Decision Explorer shall render the complete reasoning chain for any decision within 3 clicks from the overview — this operationalizes QA-001's acceptance criterion.

## 18.2 Technical Requirements
Read-only against CQRS projections (never the write model); real-time updates via event subscription; responsive; auth-gated.

---

# 19. User Management

* FR-PX-1701: Roles — `OWNER` (full control), `OPERATOR` (approve/pause), `VIEWER` (read-only), `SERVICE` (machine identities).
* FR-PX-1702: All privileged actions audited immutably (NFR-SEC-004).
* v1 scope: single-owner deployment; RBAC schema designed for future multi-user.

---

# 20. API Gateway

* FR-PX-1801: Single external entry point; Core services are never directly exposed (EC-SEC-001).
* FR-PX-1802: AuthN (token-based), rate limiting, request logging with correlation IDs.
* FR-PX-1803: Versioned API (`/v1/...`); breaking changes require new version.
* FR-PX-1804: Webhook endpoints for platform callbacks (e.g., upload processing notifications) with signature verification.

---

# 21. Notification System

* FR-PX-1901: Channels — email, webhook, dashboard. Pluggable.
* FR-PX-1902: Notification classes — `CRITICAL` (system failure, budget breach), `APPROVAL` (gated items), `DIGEST` (weekly evolution summary: what I learned, what I'll try next).
* FR-PX-1903: The weekly digest shall be generated from actual Core records (knowledge/reflections), not free-form LLM narrative — every claim in the digest links to a record.

---

# 22. Plugin & Extension Framework

### FR-PX-2001 — Extension Points

```text
PLUGIN TYPES
├── PlatformAdapter      (new execution environments)
├── LLMProvider
├── SearchProvider
├── MediaProvider        (TTS, image, video, stock)
├── StorageBackend
├── NotificationChannel
└── PipelineStage        (custom workflow stages)
```

### FR-PX-2002 — Plugin Manifest
Each plugin declares: type, version, config schema, capability manifest, health endpoint, resource footprint estimate.

### FR-PX-2003 — Isolation
Plugin failure shall not crash the orchestrator (NFR-REL-001). Plugins run with timeouts and circuit breakers.

---

# 23. Platform Security

* PX-SEC-001: All external API credentials via secrets manager (Volume 4); never in code/logs (NFR-SEC-001/003).
* PX-SEC-002: OAuth tokens (YouTube) stored encrypted at rest; refresh handled automatically; refresh failures alert `CRITICAL`.
* PX-SEC-003: Outbound request allow-listing for plugins.
* PX-SEC-004: Uploaded/downloaded media scanned for validity before processing.

---

# 24. Platform Testing

| Test                      | Approach                                                                        |
| ------------------------- | ------------------------------------------------------------------------------- |
| Stage contract tests      | Golden input/output per pipeline stage                                          |
| Adapter conformance suite | Every PlatformAdapter must pass a shared contract test suite                    |
| Pipeline integration      | Full dry-run mode: entire pipeline executes with `publish` stubbed              |
| Provider fallback         | Chaos tests killing primary providers mid-pipeline (NFR-REL-003)                |
| Resume tests              | Kill orchestrator at every stage boundary; assert checkpoint resume (FR-PX-102) |
| Load                      | Concurrent pipeline execution within Free Tier resource envelope                |

### FR-PX-2101 — Dry-Run Mode
A full end-to-end mode producing all artifacts without publishing, used for CI and pre-production validation.

---
---

# 04_EvolutionOS_SRS_Data_Infrastructure.md

# VOLUME 4 — DATA, INFRASTRUCTURE & OPERATIONS

---

# 1. Infrastructure Overview

## 1.1 Design Tension

Volume 1 imposes two competing constraints:

* CON-INF-001: run on a single AWS Free Tier EC2 instance
* NFR-SCL-001: scale without redesigning the Core

Resolution: **a modular monolith deployment of a logically distributed architecture.**

## ADR-013 — Modular Monolith First

### Decision
v1 deploys all services as containers on one host via Docker Compose, communicating through the same event bus abstraction they would use if distributed. Service boundaries are enforced logically (separate containers, separate DB schemas, event-only communication).

### Rationale
Free Tier compatibility, operational simplicity, and a guaranteed migration path: because services already communicate via events and own their data, moving a container to another host or Kubernetes requires configuration changes only.

---

# 2. System Topology

## 2.1 Reference Deployment (v1 — Single Host)

```text
┌──────────────────────── EC2 (t3.micro / t4g.small) ────────────────────────┐
│                                                                            │
│  ┌───────────┐  ┌────────────┐  ┌──────────────┐  ┌────────────────────┐  │
│  │  Gateway  │  │ Dashboard  │  │ Orchestrator │  │  Evolution Core     │  │
│  │  (API)    │  │  (Web)     │  │  (Pipelines) │  │  (Engines)          │  │
│  └─────┬─────┘  └─────┬──────┘  └──────┬───────┘  └─────────┬──────────┘  │
│        └──────────────┴────────────────┴────────────────────┘             │
│                                │                                          │
│  ┌───────────┐  ┌──────────────▼──────────┐  ┌──────────┐  ┌──────────┐   │
│  │ Scheduler │  │  Message Broker (Redis  │  │ Postgres │  │  Local   │   │
│  │           │  │  Streams, v1)           │  │          │  │  Cache   │   │
│  └───────────┘  └─────────────────────────┘  └──────────┘  └──────────┘   │
│                                                                            │
│  Heavy work (rendering) → nice-level throttled worker container            │
└────────────────────────────────────────────────────────────────────────────┘
                     │                              │
                     ▼                              ▼
              S3 (media/assets)            External APIs (LLM, YouTube, TTS)
```

## 2.2 Scale-Out Topology (Future)

Same containers, redistributed: broker → managed queue; Postgres → RDS; workers → autoscaled pool; Kubernetes optional. No code changes — configuration only (verified by INF-TST-004).

---

# 3. Microservice Architecture (Logical)

| Service           | Volume | Data Owned                             |
| ----------------- | ------ | -------------------------------------- |
| `core-engines`    | 2      | Event store, projections               |
| `orchestrator`    | 3      | Workflow state, checkpoints            |
| `adapters`        | 3      | Platform credentials, publication refs |
| `provider-router` | 3      | Cost ledger, cache                     |
| `gateway`         | 3      | Sessions, rate-limit state             |
| `dashboard`       | 3      | None (reads projections)               |
| `scheduler`       | 3      | Job definitions, run history           |

### INF-SVC-001
Each service: own schema/namespace, own migrations, health endpoint, structured logs, graceful shutdown (drain in-flight work, checkpoint, exit).

---

# 4. Database Architecture

## ADR-014 — PostgreSQL as the Universal Store (v1)

### Decision
v1 uses PostgreSQL for: event store, projections, workflow state, knowledge graph (via relational + `ltree`/recursive CTEs), and job persistence. Purpose-built stores (Neo4j, dedicated event stores, vector DBs) are deferred behind repository interfaces.

### Rationale
One battle-tested database fits Free Tier memory limits; interfaces preserve future migration (CON-TEC-003). Postgres with `pgvector` covers semantic similarity needs (FR-EC-104 consolidation) without a separate vector database.

### Consequences
Trade-off: graph queries less elegant than a native graph DB; acceptable at v1 scale, revisit at >1M knowledge records (RSK-006 threshold monitoring in place).

## 4.1 Schema Domains

```text
schema core_events      -- append-only event log
schema core_read        -- projections (rebuildable)
schema knowledge        -- records, edges, embeddings (pgvector)
schema workflow         -- orchestrator state, checkpoints
schema operations       -- jobs, audit, cost ledger
```

### INF-DB-001
`core_events` is append-only at the database level: no UPDATE/DELETE grants for any service role (hard enforcement of ADR-004).

---

# 5. Event Store Design

### INF-EVT-001 — Table Structure

```sql
events (
  sequence      BIGSERIAL PRIMARY KEY,   -- global order
  event_id      UUID UNIQUE,
  stream_id     UUID,                    -- aggregate id
  stream_type   TEXT,                    -- Experiment | Belief | ...
  version       INT,                     -- per-stream, optimistic concurrency
  event_type    TEXT,
  schema_ver    TEXT,
  correlation_id UUID,
  causation_id  UUID,
  occurred_at   TIMESTAMPTZ,
  payload       JSONB
)
UNIQUE (stream_id, version)              -- concurrency control
```

* INF-EVT-002: Writes use optimistic concurrency on `(stream_id, version)`.
* INF-EVT-003: Projections consume via the global `sequence` with persisted consumer offsets.
* INF-EVT-004: Snapshots every N events per aggregate (default 100) for load performance.
* INF-EVT-005: Payload schema evolution via `schema_ver` + upcaster functions; events are never rewritten.

---

# 6. Knowledge Graph Storage

```sql
knowledge_nodes (id, type, statement, scope JSONB, confidence,
                 status, embedding VECTOR, created_at, ...)

knowledge_edges (from_id, to_id, relation, weight, created_at)
  -- relations: EVIDENCE_FOR, CONTRADICTS, DERIVED_FROM,
  --            SUPERSEDES, RELATES_TO, CONSOLIDATED_INTO
```

* INF-KG-001: Indexes — scope (GIN), confidence (btree), embedding (HNSW/ivfflat) — satisfying NFR-PERF-002 (no full scans).
* INF-KG-002: Graph traversals via recursive CTEs, depth-capped (default 4).
* INF-KG-003: Nightly integrity job: orphan edges, confidence bound violations, illegal status transitions → alerts (RSK-002 mitigation).

---

# 7. Object Storage

* INF-OBJ-001: All media in S3 (or S3-compatible, e.g., MinIO for local dev). Content-addressed keys: `assets/{sha256}/{filename}`.
* INF-OBJ-002: Lifecycle policies: intermediates → delete after TTL (default 14d); published artifacts → Infrequent Access after 30d; provenance metadata retained forever in Postgres (CON-FIN-003).
* INF-OBJ-003: Free Tier awareness: storage monitor alerts at 80% of the 5GB free allocation; aggressive intermediate cleanup on constrained deployments.

---

# 8. Caching Strategy

| Cache                                   | Store | TTL                            |
| --------------------------------------- | ----- | ------------------------------ |
| LLM response cache (FR-PX-1303)         | Redis | 7d                             |
| Belief snapshots (decision hot path)    | Redis | invalidated on `BeliefRevised` |
| Knowledge query results                 | Redis | 1h, event-invalidated          |
| External API responses (trends, search) | Redis | per-provider policy            |

### INF-CCH-001
All caches are loss-tolerant: cache wipe degrades performance, never correctness.

---

# 9. Message Queue Architecture

## ADR-015 — Redis Streams (v1) Behind a Broker Interface

Redis Streams provides: consumer groups, persistence, replay from offset, dead-letter handling — sufficient for single-host scale, minimal memory footprint. The `MessageBroker` interface allows drop-in replacement (RabbitMQ/Kafka/SQS) at scale.

* INF-MQ-001: Every consumer group has a dead-letter stream; DLQ depth is an alerted metric.
* INF-MQ-002: Consumers are idempotent (at-least-once delivery assumed).
* INF-MQ-003: Event bus messages carry the EventEnvelope (Vol 2 §9.2) verbatim.

---

# 10. Scheduler Architecture

* INF-SCH-001: Job definitions persisted in Postgres; scheduler is stateless and restart-safe.
* INF-SCH-002: Leader election (advisory lock) permits future multi-instance schedulers without duplicate fires.
* INF-SCH-003: Missed-fire detection on startup: compare expected vs actual run history; apply per-job catch-up policy (NFR-AVA-001).
* INF-SCH-004: Job classes with priorities: `EVOLUTION_CYCLE` > `MEASUREMENT` > `MAINTENANCE` > `CLEANUP`. Under resource pressure, lower classes are deferred (NFR-PERF-004).

---

# 11. Search Architecture

* v1: Postgres full-text (`tsvector`) + `pgvector` semantic search — covering knowledge browser and consolidation similarity.
* INF-SRC-001: Search behind a `SearchIndex` interface; OpenSearch/Elasticsearch adoption deferred until measured need.

---

# 12. Configuration Management

* INF-CFG-001: Layered config: defaults → file → environment → runtime overrides. All layers logged at startup (secrets redacted).
* INF-CFG-002: Every tunable named in Volumes 1–3 (thresholds, rates, windows, budgets) shall be externally configurable without rebuild.
* INF-CFG-003: Config changes at runtime emit `ConfigChanged` audit events — because config changes can alter evolution behavior, they are part of the experiment record context.
* INF-CFG-004: Config schema validation at startup; invalid config = refuse to start (fail fast).

---

# 13. Secrets Management

* INF-SEC-001: v1 — encrypted environment via Docker secrets / SOPS-encrypted files; AWS deployments should prefer SSM Parameter Store (free tier) over hardcoded env files.
* INF-SEC-002: Secrets loaded at runtime only; never written to disk unencrypted, never logged (NFR-SEC-001/002/003).
* INF-SEC-003: Secret rotation procedure documented per provider; OAuth refresh automated (PX-SEC-002).

---

# 14. Deployment Architecture

## 14.1 Deployment Modes

| Mode      | Target           | Method                                                |
| --------- | ---------------- | ----------------------------------------------------- |
| Local dev | Workstation      | `docker compose --profile dev` (MinIO, mock adapters) |
| Reference | Single EC2       | `docker compose --profile prod`                       |
| Scale-out | Multi-host / K8s | Same images, Helm charts (future)                     |

* INF-DEP-001: Identical container images across all modes (NFR-PRT-001). Behavior differences via configuration only.
* INF-DEP-002: One-command bootstrap: `make deploy` provisions, migrates, seeds, and health-checks.
* INF-DEP-003: Zero-data-loss upgrades: `docker compose up` with new images performs graceful drain, migration, resume (NFR-REL-004, AC-001).

---

# 15. Containerization Strategy

* INF-CNT-001: Multi-stage builds; minimal runtime images; non-root users; pinned base images.
* INF-CNT-002: Per-container memory/CPU limits sized for the Free Tier envelope; the render worker gets the residual budget with lowest priority.
* INF-CNT-003: Health checks (liveness + readiness) on every container; compose restarts unhealthy containers (NFR-REL-001).

---

# 16. Kubernetes (Future)

Deferred by ADR-013. Readiness criteria for migration: sustained multi-experiment concurrency beyond single-host capacity, or multi-platform adapters requiring isolation. Pre-work already satisfied by design: stateless services (CON-INF-002), health probes, config-driven wiring, event-based comms.

---

# 17. CI/CD Pipeline

```text
Push → Lint → Unit Tests → Contract Tests → Build Images
     → Integration (dry-run pipeline, PX-2101)
     → Event Replay Regression (NFR-TST-003)
     → Simulation Gate (FR-EC-601 subset)
     → Publish Images → Deploy (manual gate v1)
```

* INF-CI-001: The **Simulation Gate** is mandatory: a reduced simulation run must show no degradation in planted-rule discovery vs baseline. Intelligence regressions block merge like test failures.
* INF-CI-002: Migrations tested against a snapshot of production-shaped data.
* INF-CI-003: Every image tagged with git SHA; running system reports its exact versions on the dashboard.

---

# 18. Monitoring & Observability

## 18.1 Stack (v1, Free-Tier-Sized)

Prometheus (metrics) + Loki or file-based structured logs + Grafana dashboards — or a lightweight equivalent bundled in compose. All optional components degrade gracefully if disabled on constrained hosts.

## 18.2 The Three Dashboards

1. **Machine Health** — CPU, memory, disk, container states, queue depths, API error rates
2. **Pipeline Health** — stage durations, failure rates, retry counts, budget burn
3. **Intelligence Health** — Core metrics (Vol 2 §15): prediction error trend, calibration error, knowledge growth, learning yield

### INF-OBS-001
Intelligence Health is a first-class operational dashboard, not an analytics afterthought — a declining KPI-EVO-002 is treated with the severity of an outage (per QA-009).

---

# 19. Logging Architecture

* INF-LOG-001: JSON structured logs; mandatory fields: timestamp, service, engine, event, severity, correlation_id (NFR-OBS-001).
* INF-LOG-002: `correlation_id` propagates from directive issuance through every pipeline stage to observation ingestion — one query reconstructs a full experiment's operational trail.
* INF-LOG-003: Secret-redaction filter on all log sinks (NFR-SEC-003), tested in CI with canary secrets.
* INF-LOG-004: Retention: operational logs 30d; audit logs indefinitely (separate immutable store).

---

# 20. Metrics & Alerting

## 20.1 Alert Policy

| Severity   | Examples                                                                | Action                 |
| ---------- | ----------------------------------------------------------------------- | ---------------------- |
| `CRITICAL` | Event store write failures, all-provider outage, OAuth dead, disk > 90% | Immediate notification |
| `WARNING`  | DLQ non-empty, calibration drift, budget 80%, provider degraded         | Digest + dashboard     |
| `INFO`     | Fallbacks used, exploration-rate auto-adjusted                          | Dashboard only         |

### INF-ALR-001 — Evolutionary Alerts
Unique to EvolutionOS — alerts on intelligence, not just infrastructure:

* Prediction error rising over rolling window (KPI-EVO-002 violation)
* Calibration error > threshold (KPI-BEL-002)
* Learning yield collapse (experiments completing without ACTIVE lessons)
* Belief instability spike (KPI-BEL-001)
* Fitness plateau beyond exploration escalation limits

These route to Governance review (Volume 5 §10).

---

# 21. Backup & Disaster Recovery

* INF-BCK-001: Event store: daily full backup + WAL archiving to S3. RPO ≤ 15 min for the event log.
* INF-BCK-002: Projections are NOT backed up — they rebuild from events (EC-CQRS-001). This drastically shrinks backup surface.
* INF-BCK-003: Monthly automated restore drill: restore into a scratch environment, replay, verify projection checksums (untested backups are not backups).
* INF-BCK-004: Knowledge integrity: verified snapshots enabling RSK-002 recovery (rollback + event replay).
* INF-BCK-005: Full-loss recovery runbook: fresh host + latest backup → operational in ≤ 4h (RTO target, v1).

---

# 22. High Availability

v1 accepts single-host risk (Free Tier), mitigated by: container auto-restart, checkpoint resume (FR-PX-102, FR-EC-502), aggressive backup. True HA (multi-AZ, replicated Postgres) is a documented scale-out path, unblocked by architecture.

### INF-HA-001
The system shall tolerate a full host reboot with zero knowledge loss and automatic workflow resumption — this is tested monthly (chaos drill).

---

# 23. Performance & Scalability

* INF-PRF-001: Load budget on reference hardware: sustain ≥ 1 full experiment pipeline/day + continuous measurement + daily consolidation, with p95 dashboard latency < 2s.
* INF-PRF-002: Every engine reports its own latency histograms; regressions caught in CI performance smoke tests.
* INF-PRF-003: Backpressure: when queues exceed thresholds, orchestrator stops accepting new directives before degrading in-flight work.

---

# 24. Cost Optimization

* INF-CST-001: Unified cost ledger (compute estimate + API spend + storage) surfaced per experiment.
* INF-CST-002: Monthly budget ceiling (configurable). Forecast breach → autonomously shift to cheaper providers/models → then pause new experiments → alert. Never silent overspend.
* INF-CST-003: Cost per validated lesson is a tracked efficiency metric (ties to KPI-EVO-003).

---

# 25. Security Architecture (Consolidated)

```text
Perimeter:   Gateway only public; TLS; rate limiting
Identity:    Human RBAC (Vol 3 §19) + service identities
Secrets:     SSM/SOPS; runtime-only; redacted logs
Data:        Encryption at rest (DB, S3) and in transit
Integrity:   Append-only events (INF-DB-001); audit trail
Supply chain: Pinned deps, image scanning in CI, minimal images
Isolation:   Container boundaries; plugin allow-lists (PX-SEC-003)
```

* INF-SEC-010: Quarterly dependency audit; critical CVEs patched within defined SLA.

---

# 26. Infrastructure Testing

| Test                                                                                                  | Frequency         |
| ----------------------------------------------------------------------------------------------------- | ----------------- |
| Restore drill (INF-BCK-003)                                                                           | Monthly           |
| Host reboot chaos drill (INF-HA-001)                                                                  | Monthly           |
| Projection rebuild verification                                                                       | Weekly, automated |
| INF-TST-004: Topology portability — full stack on laptop, EC2, and (future) K8s from identical images | Per release       |
| Free Tier envelope test — full cycle within resource limits                                           | Per release       |
| Secret redaction canary                                                                               | Every CI run      |

---
---

# 05_EvolutionOS_SRS_Evolution_Governance.md

# VOLUME 5 — AUTONOMOUS EVOLUTION, GOVERNANCE & ROADMAP

---

# 1. Evolution Philosophy

Volumes 2–4 define the machinery. This volume defines the **discipline**: how EvolutionOS is permitted to evolve, what it may never do, how humans retain meaningful control, and how we verify that evolution is real rather than illusory.

Guiding statement:

> **An autonomous system without governance is not intelligent — it is merely unsupervised.**

---

# 2. Scientific Method Framework

## 2.1 The Canonical Method

EvolutionOS shall implement the scientific method as an executable protocol:

```text
1. OBSERVE      Collect evidence about the environment
2. QUESTION     Identify gaps, contradictions, surprises
3. HYPOTHESIZE  Formulate a falsifiable prediction (FR-EC-410)
4. PREDICT      Quantify expected outcome + confidence
5. EXPERIMENT   Execute with controlled mutation (DP-011)
6. MEASURE      Collect per measurement plan
7. ANALYZE      Compare prediction vs reality (Reflection)
8. CONCLUDE     Extract lessons with statistical guardrails
9. INTEGRATE    Update knowledge and beliefs
10. REPEAT      Feed conclusions into the next cycle
```

## 2.2 Epistemic Rules

* GOV-SCI-001: A hypothesis that cannot fail is not a hypothesis. Validation rejects unfalsifiable statements.
* GOV-SCI-002: Negative results are first-class results. Falsified hypotheses produce lessons with the same rigor as confirmed ones.
* GOV-SCI-003: The system shall distinguish, in every record: **fact** (observed), **inference** (derived), **prediction** (forecast), **belief** (confidence-weighted conclusion), **speculation** (unsupported) — per CON-ETH-002. Speculation may never be used as decision evidence.
* GOV-SCI-004: Correlation claims require the statistical thresholds of FR-EC-111 before becoming causal claims. Causal claims additionally require controlled-mutation evidence (RSK-008).

---

# 3. Experimentation Framework (Governance View)

## 3.1 Experiment Classes

| Class         | Risk    | Approval (default)       | Mutation Distance                  |
| ------------- | ------- | ------------------------ | ---------------------------------- |
| `VALIDATION`  | Low     | Autonomous               | Near (re-testing known rules)      |
| `INCREMENTAL` | Low-Med | Autonomous               | Near                               |
| `EXPLORATORY` | Medium  | Autonomous within budget | Mid                                |
| `RADICAL`     | High    | Gated (human)            | Far                                |
| `META`        | High    | Gated (human)            | Changes to learning process itself |

* GOV-EXP-001: Class assignment is computed from risk score + mutation distance, not self-declared.
* GOV-EXP-002: Portfolio constraints (FR-EC-422 distribution) are governance-enforced; the Decision Engine cannot override them.
* GOV-EXP-003: Every experiment carries a pre-registered analysis plan. Post-hoc metric shopping ("we didn't move CTR but look at comments!") is recorded as exploratory observation, never as hypothesis confirmation.

---

# 4. Hypothesis Engine Governance

* GOV-HYP-001: Backlog prioritization formula is versioned config: `priority = f(information_value, strategic_alignment, cost, risk)` — where `information_value` favors hypotheses that discriminate between competing beliefs.
* GOV-HYP-002: Contradiction-resolution hypotheses receive automatic priority elevation (unresolved contradictions are epistemic debt).
* GOV-HYP-003: Maximum concurrent hypotheses touching the same variable: 1 (prevents confounded attribution across simultaneous experiments).

---

# 5. Mutation Engine Governance

* GOV-MUT-001: Mutation rate bounds: floor (exploration mandate, RSK-004) and ceiling (stability mandate). Auto-adjustment stays within bounds; changing the bounds themselves is a `META` experiment.
* GOV-MUT-002: Forbidden mutation registry: mutations that may never be attempted autonomously (e.g., violating platform ToS, misleading content framings, undisclosed sponsorship patterns). This registry is human-editable, versioned, and checked at directive issuance.
* GOV-MUT-003: `META` mutations (changing learning rates, fitness weights, consolidation thresholds) execute in **shadow mode** first: new parameters run in parallel evaluation against historical data before going live.

---

# 6. Fitness Evaluation Governance

* GOV-FIT-001: Fitness weight profiles (FR-EC-431) may only change via versioned governance events; the Fitness Engine cannot self-modify its own weights outside shadow-tested `META` experiments.
* GOV-FIT-002: **Goodhart Defense** — every fitness component has a paired counter-metric watched for divergence:

| Optimized            | Counter-Metric Watched                         |
| -------------------- | ---------------------------------------------- |
| selection_rate (CTR) | attention_rate (clickbait detector)            |
| learning_yield       | lesson deprecation rate (junk-lesson detector) |
| output volume        | cost per validated lesson                      |
| audience_growth      | returning-viewer rate                          |

Sustained divergence triggers `GoodhartAlert` → governance review.

* GOV-FIT-003: Fitness is never compared across weight-profile versions without normalization.

---

# 7. Reflection Framework Governance

* GOV-RFL-001: Reflection completeness audit: any experiment reaching `ARCHIVED` without a ReflectionReport is a `CRITICAL` defect (DP-012 enforcement).
* GOV-RFL-002: Reflection honesty check: reflections claiming confirmation are automatically cross-validated against raw observations by an independent validation pass (different prompt/model than the one that generated the reflection — reduces self-confirmation bias).
* GOV-RFL-003: Meta-reflection cadence (FR-EC-122) is governance-owned configuration.

---

# 8. Learning Framework Governance

* GOV-LRN-001: Evidence hierarchy — weight order: controlled experiment > natural experiment > observational correlation > external claim. External claims (e.g., "best practices" from research) enter as `CANDIDATE` knowledge with capped confidence until locally validated.
* GOV-LRN-002: Transfer learning rules — knowledge from one scope (niche/platform) applies to another only with a scope-transfer discount on confidence, and is flagged `TRANSFERRED` until validated in the new scope.
* GOV-LRN-003: Learning from failure quota — the system shall periodically verify that lessons are being extracted from failed experiments at a comparable rate to successes; a large asymmetry indicates success-bias in the Learning Engine.

---

# 9. Strategy Evolution Governance

* GOV-STR-001: Strategy changes require justification chains: `evidence → belief revision → strategy revision`, all linked by correlation IDs. Strategy drift without traceable cause is an architectural defect.
* GOV-STR-002: Niche/pivot decisions (highest-impact strategy class) are `RADICAL`-class: gated by default, with a full written case (evidence, alternatives, predicted outcomes) surfaced to the owner.
* GOV-STR-003: Strategy graveyard — retired strategies are archived with their full fitness history; the Hypothesis Engine may propose revival experiments when environmental conditions resembling their success period recur.

---

# 10. Self-Optimization (The System Improving Itself)

## 10.1 Levels of Self-Modification

```text
Level 0   Parameter tuning within bounds        → Autonomous
Level 1   Parameter bound changes                → META experiment, shadow-tested
Level 2   Algorithm/policy selection changes     → META experiment, gated
Level 3   Architecture changes                   → Human-only (out of scope for autonomy)
```

* GOV-SLF-001: The system shall never perform Level 3 changes autonomously. Its self-improvement authority is bounded and explicit.
* GOV-SLF-002: Self-evaluation (NFR-AUT-003) runs on the meta-reflection cadence and produces a **Learning Health Report**: prediction trend, calibration, yield, exploration effectiveness, cost efficiency — with recommended Level 0–2 adjustments.
* GOV-SLF-003: Every self-modification is recorded in the Evolution Timeline (FR-024) with before/after parameters and its own measurement plan. **Self-modifications are experiments too.**

---

# 11. Knowledge Governance

* GOV-KNW-001: Knowledge quality floor — records failing quality score thresholds (Vol 1 KPI-KNW-002) for `N` consecutive evaluations auto-transition to `DEPRECATED` with notification.
* GOV-KNW-002: Consolidation review — automated consolidations above a scope-impact threshold are sampled for human/audit review (guarding against meaning-destroying merges).
* GOV-KNW-003: Right of inspection — the owner can query "everything the system believes about X" and receive a complete, evidence-linked answer (Dashboard Knowledge Browser requirement).
* GOV-KNW-004: Poisoning defense — anomalous observation batches (statistical outliers, suspicious sources) are quarantined before influencing knowledge (extends FR-EC-302).

---

# 12. Memory Governance

* GOV-MEM-001: Archival policy owned by governance config, not the Memory Engine. Defaults: nothing deleted; archived items excluded from active retrieval; full history queryable for audit.
* GOV-MEM-002: Storage-pressure protocol: consolidation intensification → intermediate artifact cleanup → cold-tier archival — knowledge and event history are last-resort and require human approval to offload.

---

# 13. Belief Governance

* GOV-BEL-001: Calibration audits — scheduled comparison of stated confidence vs realized frequency (KPI-BEL-002); systematic miscalibration triggers global learning-rate review.
* GOV-BEL-002: Core belief protection — beliefs marked `LOAD_BEARING` (many decisions depend on them) require stronger contradiction evidence before revision, and their revisions notify the owner.
* GOV-BEL-003: No belief may cite itself in its own evidence chain (circular-support detection in the knowledge graph integrity job).

---

# 14. Decision Governance

* GOV-DEC-001: Decision audit sampling — a random sample of autonomous decisions per week is surfaced in the dashboard "Audit" queue for optional human review; reviewer disagreement is recorded as Level-4 feedback.
* GOV-DEC-002: Decision consistency monitor (KPI-DEC-003) — near-identical contexts producing divergent decisions without exploration-flag justification raise alerts.
* GOV-DEC-003: The four override verbs — `PAUSE`, `REJECT`, `ROLLBACK`, `REDIRECT` — are available to the owner at every decision point, always audited, and always fed back as learning signal (DP-014).

---

# 15. Ethical & Safety Framework

## 15.1 Hard Constraints (Never Violated, Never Learned Around)

* GOV-ETH-001: Platform ToS compliance is a hard constraint, checked pre-publication (CON-ETH-001).
* GOV-ETH-002: Factual integrity — no published claim without Fact Ledger support (FR-PX-203). The system shall not learn that fabrication improves metrics because fabrication is blocked upstream of measurement.
* GOV-ETH-003: No dark patterns registry — forbidden techniques (fabricated urgency, misleading thumbnails contradicting content, impersonation) live in the Forbidden Mutation Registry (GOV-MUT-002).
* GOV-ETH-004: Content policy filter — configurable topic/treatment exclusions, evaluated at directive issuance and again pre-publication.
* GOV-ETH-005: Transparency — AI-generated content disclosure per platform requirements and owner policy.

## 15.2 Safety Invariants

* GOV-SAF-001: Kill switch — a single owner action halts all publishing and external actions within one scheduler tick, while learning/reflection on already-collected data may continue.
* GOV-SAF-002: Blast-radius limits — max autonomous publications per day; max budget per experiment; max simultaneous `RADICAL` experiments (0 by default).
* GOV-SAF-003: Anomaly self-halt — if the system detects its own behavior deviating beyond bounds (publication rate spikes, cost spikes, decision-consistency collapse), it self-transitions to `GATED` mode and alerts.

---

# 16. Risk Management (Extended Register)

Extends Volume 1 §24:

| ID      | Risk                                               | Mitigation                                           |
| ------- | -------------------------------------------------- | ---------------------------------------------------- |
| RSK-009 | Goodhart's Law — optimizing proxy destroys goal    | GOV-FIT-002 counter-metrics                          |
| RSK-010 | Self-confirmation bias in reflection               | GOV-RFL-002 independent validation                   |
| RSK-011 | Reward hacking via junk lessons                    | FR-EC-432 anti-gaming rule                           |
| RSK-012 | Knowledge poisoning via anomalous data             | GOV-KNW-004 quarantine                               |
| RSK-013 | Runaway autonomous behavior                        | GOV-SAF-001/002/003                                  |
| RSK-014 | Circular belief support                            | GOV-BEL-003                                          |
| RSK-015 | Confounded attribution from concurrent experiments | GOV-HYP-003 variable locking                         |
| RSK-016 | Ethical drift via incremental mutations            | Hard constraints outside the learnable space (§15.1) |

**The central safety design principle:** ethical and safety constraints are enforced **outside** the learning loop. The system cannot learn its way around a rule it never gets to test.

---

# 17. Explainability Framework (Operationalized)

The "Five Whys" contract — for any published artifact, the system shall answer via dashboard, each with linked records:

1. **Why this experiment?** → Strategy + hypothesis backlog priority
2. **Why this hypothesis?** → Source (stale belief / contradiction / surprise / exploration)
3. **Why this candidate?** → DecisionRecord: candidates, scores, rejections
4. **Why this confidence?** → Evidence chain + calibration history
5. **What did we learn?** → ReflectionReport + resulting knowledge

* GOV-XPL-001: All five answers available within 3 dashboard clicks (extends FR-PX-1601).
* GOV-XPL-002: Explanation records are generated at decision time, never reconstructed post-hoc.

---

# 18. Audit & Compliance

* GOV-AUD-001: Immutable audit log (separate from event store, append-only) for: human actions, governance config changes, secret rotations, kill-switch activations, gated approvals.
* GOV-AUD-002: Quarterly self-audit report auto-generated: constraint compliance, calibration health, override statistics, cost summary, incident log.
* GOV-AUD-003: Full data-lineage export capability (supports future compliance regimes and research reproducibility).

---

# 19. Versioning Strategy

* GOV-VER-001: Independent semver for: Core engines, Execution Layer, event schemas, prompt registry, governance config, ontology. A deployment manifest pins the compatible set.
* GOV-VER-002: Event schema changes: additive preferred; breaking changes require upcasters (INF-EVT-005) and dual-read windows.
* GOV-VER-003: Knowledge is version-independent — it must survive every upgrade intact (FR-002, AC-001). Upgrade tests include knowledge-integrity checksums.

---

# 20. Migration Strategy

* GOV-MIG-001: All migrations forward-only with tested rollback via backup restore (never destructive down-migrations on the event store).
* GOV-MIG-002: Projection-affecting changes: rebuild projections from events rather than migrating projection tables where feasible.
* GOV-MIG-003: Platform migration playbook (adding e.g. Blog): implement adapter contract → pass conformance suite (Vol 3 §24) → register metric mapping → run `VALIDATION`-class experiments before scope expansion.

---

# 21. Quality Assurance Framework

Consolidated verification matrix:

| Property             | Verified By                                                      |
| -------------------- | ---------------------------------------------------------------- |
| Learns real rules    | Simulation harness planted-rule discovery (FR-EC-601)            |
| Doesn't forget       | Restart + upgrade knowledge checksums (AC-001, GOV-VER-003)      |
| Explains itself      | Five Whys dashboard audit (GOV-XPL-001)                          |
| Calibrated           | Scheduled calibration audits (GOV-BEL-001)                       |
| Doesn't game metrics | Counter-metric monitors (GOV-FIT-002), anti-gaming rule          |
| Safe                 | Kill-switch drills, blast-radius tests, forbidden-registry tests |
| Reproducible         | Event replay determinism tests (AC-013)                          |
| Portable             | Multi-topology deployment tests (INF-TST-004)                    |
| Resilient            | Chaos drills (INF-HA-001), provider-kill tests                   |

---

# 22. Acceptance Criteria (Release Gates)

A release of EvolutionOS is acceptable only when:

* AC-V5-001: All Volume 1 acceptance criteria (AC-001–013) pass.
* AC-V5-002: Simulation gate: ≥ 80% planted-rule discovery, calibration error within bounds.
* AC-V5-003: Kill switch verified end-to-end in staging.
* AC-V5-004: Restore drill passed within RTO on the release candidate.
* AC-V5-005: Zero secrets in logs (canary test).
* AC-V5-006: Five Whys demonstrably answerable for a real gated experiment.
* AC-V5-007: Full Free Tier envelope test passed.

---

# 23. KPIs & Success Metrics (Governance Additions)

Beyond Volume 1 §25:

* KPI-GOV-001: Override rate — % of gated items rejected by owner (should trend down as the system learns owner preferences)
* KPI-GOV-002: Constraint violation attempts caught pre-publication (should be near zero and never post-publication)
* KPI-GOV-003: Time-in-GATED vs AUTONOMOUS mode (autonomy earned, measured)
* KPI-GOV-004: Goodhart alerts per quarter
* KPI-GOV-005: Cost per validated lesson (system-level efficiency)

---

# 24. Product Roadmap

## v0.1 — Skeleton (Foundations)
Event store, event bus, config, deployment, dashboard shell, simulation harness scaffold. **Gate:** replayable events, rebuildable projections.

## v0.2 — Core Loop in Simulation
All Core engines operational against the simulation environment only. **Gate:** planted-rule discovery ≥ 80% (AC-V5-002). *No real-world publishing until this passes.*

## v0.3 — Pipeline (Dry Run)
Full content pipeline in dry-run mode: research → story → script → narration → visuals → composition → thumbnail. **Gate:** end-to-end artifacts from a directive, checkpoint-resume verified.

## v0.4 — First Contact (Gated)
YouTube adapter live, `GATED_STRICT` mode, analytics collection, observation normalization. **Gate:** first real experiments complete the full loop including reflection and lesson extraction.

## v0.5 — Learning Verified
Multiple experiment cycles; calibration audits; first knowledge consolidations. **Gate:** measurable prediction-error improvement across cycles (KPI-EVO-002) on real data.

## v1.0 — Supervised Autonomy
`NOTIFY` mode, self-evaluation active, weekly digests, full governance framework, all release gates green. **This is the Volume 1 vision, realized on YouTube.**

## v1.5 — Earned Autonomy
`AUTONOMOUS` mode for `VALIDATION`/`INCREMENTAL` classes based on KPI-GOV-001 trends. Meta-experiments (Level 1 self-optimization) enabled.

## v2.0 — Multi-Platform
Second adapter (Blog recommended: cheap, fast feedback). Cross-platform knowledge transfer with GOV-LRN-002 scope discounts. **Gate:** AC-009 proven — zero Core changes required.

## v3.0 — Multi-Domain
Non-content execution environments (SEO, marketing experiments). Generalized directive schema. Fitness profiles per domain.

## v4.0 — Research-Grade
Statistical rigor upgrades (causal inference tooling, power analysis), reproducibility exports, benchmarking suite for autonomous learners.

## v5.0 — General Evolution Platform
EvolutionOS as a framework: bring-your-own execution environment, ontology-driven configuration, the Core as a reusable autonomous experimentation kernel.

---

# 25. Future Research Directions

* Causal graph learning over the knowledge graph (beyond pairwise rules)
* Multi-armed bandit / Bayesian optimization formalisms for exploration policy
* Cross-domain analogy: transferring structural knowledge between unrelated environments
* Adversarial self-testing: a "red team" engine attacking the system's own beliefs
* Federated evolution: multiple EvolutionOS instances sharing validated (anonymized) knowledge
* Formal verification of safety-invariant enforcement

---

# Appendix A — ADR Index (Complete)

| ADR | Title                                        | Volume                                  |
| --- | -------------------------------------------- | --------------------------------------- |
| 001 | Capabilities Instead of Services             | 1                                       |
| 002 | Knowledge at the Center                      | 1                                       |
| 003 | YouTube as Execution Environment             | 1                                       |
| 004 | Immutable Knowledge                          | 1                                       |
| 005 | Every Decision Explainable                   | 1 (principle) / 5 §17 (operationalized) |
| 006 | Experiments as Unit of Progress              | 1 / 2 §8                                |
| 007 | Confidence Mandatory                         | 1 / 2 §6.1                              |
| 008 | Platform Independence Core Requirement       | 1 / 3 §12                               |
| 009 | Event-Driven Communication                   | 1 / 2 §9                                |
| 010 | Evolution Over Production                    | 1 / 5 §6                                |
| 011 | Event Sourcing for the Core                  | 2                                       |
| 012 | CQRS Separation                              | 2                                       |
| 013 | Modular Monolith First                       | 4                                       |
| 014 | PostgreSQL Universal Store (v1)              | 4                                       |
| 015 | Redis Streams Broker (v1)                    | 4                                       |
| 016 | Safety Constraints Outside the Learning Loop | 5 §16                                   |
| 017 | Progressive/Earned Autonomy                  | 5 §3, Roadmap                           |
| 018 | Simulation Before Reality                    | 5 Roadmap v0.2                          |
| 019 | Shadow-Mode Meta-Mutations                   | 5 §5                                    |
| 020 | Goodhart Counter-Metric Pairing              | 5 §6                                    |

---

# Appendix B — Glossary (Delta from Volume 1)

| Term                | Definition                                                                   |
| ------------------- | ---------------------------------------------------------------------------- |
| Directive           | Core→Execution instruction package for one experiment                        |
| Projection          | Rebuildable read model derived from the event log                            |
| Saga                | Long-running process manager coordinating the evolution cycle                |
| Shadow Mode         | Parallel evaluation of a change without live effect                          |
| Mutation Distance   | How far a variation departs from validated knowledge                         |
| Goodhart Alert      | Detected divergence between an optimized metric and its counter-metric       |
| Fact Ledger         | Source-verified claim registry gating script content                         |
| Scope Discount      | Confidence penalty applied to knowledge transferred between scopes           |
| Load-Bearing Belief | Belief with high decision-dependency, protected by stricter revision rules   |
| Earned Autonomy     | Autonomy expanded based on measured owner-alignment, not configuration alone |

---

# Appendix C — System Ontology (Canonical)

The formal vocabulary all schemas, APIs, prompts, and documentation must use:

```text
ENTITY          LIFECYCLE                          KEY RELATIONS
─────────────────────────────────────────────────────────────────────────
Observation     received → classified → routed     evidence-for → Knowledge
                (immutable)                        measured-by → Experiment

Knowledge       CANDIDATE → ACTIVE →               derived-from → Observation
Record          DEPRECATED → ARCHIVED              supersedes → KnowledgeRecord
                (append-only versions)             consolidated-into → KnowledgeRecord

Rule            (KnowledgeRecord subtype:          supports → Belief
                 conditional, scoped claim)

Belief          ACTIVE ⇄ SUSPENDED → RETIRED       derived-from → KnowledgeRecord
                (confidence time series)           used-by → Decision

Hypothesis      PROPOSED → ACTIVE →                generated-from → Belief|Surprise
                CONFIRMED|FALSIFIED                tested-by → Experiment
                (falsifiable form mandatory)

Experiment      DRAFT → … → ARCHIVED               tests → Hypothesis
                (state machine, Vol 2 §8.1)        contains → Mutation
                                                   produces → Observation, Reflection

Mutation        (declared pre-execution)           varies → Variable
                                                   distance: near|mid|far

Decision        (immutable record)                 selects → Candidate
                                                   cites → Belief, KnowledgeRecord
                                                   predicts → Prediction

Prediction      stated → evaluated                 compared-in → Reflection

Reflection      (exactly one per terminal          analyzes → Experiment
                 experiment)                       proposes → Lesson

Fitness         (vector, then scalar via           evaluates → Experiment
Record           versioned weight profile)         informs → Strategy

Strategy        DRAFT → ACTIVE →                   plans → Experiment
                UNDER_REVIEW → RETIRED             pursues → Objective
                (mandatory expiration)
```

**Ontology rule ONT-001:** Any new concept introduced anywhere in the system must first be added here, with lifecycle and relations, before implementation.

---

# Appendix D — Requirement Traceability (Cross-Volume Index)

| Range                                                         | Volume | Domain               |
| ------------------------------------------------------------- | ------ | -------------------- |
| FR-001 – FR-025, NFR-*, QA-*, DP-*, CON-*, ASM-*, RSK-001–008 | 1      | Foundation           |
| FR-EC-1xx – 6xx, EC-*, ADR-011/012                            | 2      | Evolution Core       |
| FR-PX-1xx – 21xx, PX-*                                        | 3      | Platform & Execution |
| INF-*, ADR-013/014/015                                        | 4      | Infrastructure       |
| GOV-*, RSK-009–016, KPI-GOV-*, AC-V5-*, ADR-016–020           | 5      | Governance           |

Every implementation artifact must trace to exactly one requirement ID. Every requirement must trace to at least one test. No orphans in either direction (NFR-MNT-005).

---

## Documentation Set Status: **COMPLETE**

```text
Volume 1  Foundation        ██████████ 100%   The Constitution
Volume 2  Evolution Core    ██████████ 100%   The Mind
Volume 3  Platform Layer    ██████████ 100%   The Hands
Volume 4  Infrastructure    ██████████ 100%   The Body
Volume 5  Governance        ██████████ 100%   The Conscience
```

---

A few closing architectural notes on decisions I made while writing these volumes:

1. **I moved "Create" and metric collection into the Execution Layer (Vol 3), keeping the Core purely abstract.** This is the strictest possible interpretation of platform independence — the Core literally cannot mention "video." This makes AC-009 structurally guaranteed rather than merely tested.

2. **The Simulation Harness (FR-EC-601) is the most important requirement in the entire set.** Without planted ground-truth rules, you can never prove the system actually learns versus merely appearing to. It's also the CI gate that prevents intelligence regressions (INF-CI-001) — treating "got dumber" with the same severity as "tests failed."

3. **Safety constraints live outside the learning loop (ADR-016).** The system can't learn to game rules it never gets to test. This is the single most important safety decision in the design.

4. **Autonomy is earned, not configured (ADR-017).** The progression GATED → NOTIFY → AUTONOMOUS driven by measured owner-alignment (KPI-GOV-001) makes the system trustworthy by demonstration.

5. **The Ontology (Appendix C) fulfills the recommendation from Volume 1** — it's now the canonical vocabulary binding all five volumes together.

The next logical step would be **Volume 0: Implementation Kickoff** — the concrete v0.1 sprint plan, repository structure, and first event schemas. Want me to draft it?



# 📚EvolutionOS — Supplementary Specifications

---

# 06_EvolutionOS_Ontology_Specification.md

# EVOLUTIONOS ONTOLOGY SPECIFICATION

**Version:** 1.0
**Status:** Canonical
**Authority:** This document supersedes any informal definition used elsewhere. If a concept exists in the system, it exists here first.

---

# 1. Purpose

The Ontology Specification defines the **complete vocabulary** of EvolutionOS.

Every entity, attribute, relationship, lifecycle state, event, and constraint that appears in code, database schemas, API contracts, prompts, dashboards, or documentation must trace to this document.

Without a shared ontology:

* Different modules develop divergent meanings for the same term
* Prompts and code disagree on what a "belief" is
* Knowledge extracted in one engine cannot be consumed by another
* Refactoring becomes archaeology

This document is **living**: new concepts require an entry here before implementation. Modifying an existing entry requires an ADR.

---

# 2. Ontology Organization

```text
Level 0SUBSTRATERaw material the system processes
Level 1   PERCEPTION     How the system receives reality
Level 2   KNOWLEDGE      What the system retains
Level 3   COGNITION      How the system thinks
Level 4   ACTION         How the system acts
Level 5   GOVERNANCE     How the system is controlled
Level 6   RELATIONS      How entities connect
Level 7   EVENTS         How state changes are announced
```

---

# 3. Level 0— Substrate

## 3.1 Variable

The smallest unit of experimental interest. A property of the world that the system can observe or manipulate.

```yaml
Variable:
  id: UUID
  name: string# canonical identifier, stable
  label: string                    # human-readable
  type: CONTINUOUS | ORDINAL | CATEGORICAL | BINARY
  domain: ValueDomain              # valid range / allowed values
  unit: string | null
  scope_applicability: [Scope]     # which scopes this variable is relevant to
  is_manipulable: bool             # can the system change it?
  is_observable: bool              # can the system measure it?
```

**Invariant:** A variable that is neither manipulable nor observable has no role in the system.

---

## 3.2 Metric

A measured expression of a Variable within a specific context.

```yaml
Metric:
  id: UUID
  canonical_name: string           # e.g., "selection_rate", "attention_rate"
  variable_ref: Variable.id
  aggregation: SUM | AVG | RATE | RATIO | PERCENTILE
  collection_window: Duration
  platform_mappings: map<Platform, string>  # e.g. youtube → "ctr"
  quality_floor: float# minimum reliability score to use
```

**Canonical Metric Registry** (additions require ONT-001 procedure):

| Canonical Name | Definition | Primary Variable |
|---|---|---|
| `selection_rate` | % of impressions resulting in engagement | CTR / play rate |
| `attention_rate` | % of content consumed on average | retention / completion |
| `audience_growth` | Net new persistent followers per cycle | subscribers / follows |
| `return_rate` | % returning audience | returning viewers |
| `engagement_depth` | Meaningful interactions per view | comments, saves |
| `conversion_rate` | Desired action completions | goal-dependent |

---

## 3.3 Scope

The contextual boundary within which a piece of knowledge applies.

```yaml
Scope:
  niche: string | null             # topic domain, e.g., "cybersecurity"
  platform: string | null          # execution env, e.g., "youtube"
  audience_segment: string | null  # e.g., "technical_beginner"
  format: string | null            # e.g., "documentary", "explainer"
  language: string | null
  region: string | null
```

**Scope matching rules:**

* `null` fields are wildcards — they match anything
* Two scopes are compatible if every non-null field matches
* Scope specificity score = count of non-null fields (more specific overrides less specific)

---

# 4. Level 1 — Perception

## 4.1 Observation

A single, immutable, timestamped measurement of a Metric produced by an Experiment.

```yaml
Observation:
  id: UUID
  experiment_id: UUID
  platform: string
  metric: Metric.canonical_name
  value: numeric | structured
  unit: string
  measured_at: timestamp
  collection_window: Duration
  collection_method: AUTOMATED | MANUAL | ESTIMATED
  quality: ObservationQuality
  raw_source_ref: string | null     # original API response reference
  status: RECEIVED | VALIDATED | QUARANTINED | INTEGRATED

ObservationQuality:
  completeness: float# 0.0–1.0
  reliability: CONFIRMED | ESTIMATED | DISPUTED
  freshness: CURRENT | DELAYED | STALE
```

**Immutability contract:** Once status = `INTEGRATED`, an Observation is sealed. Corrections create a new Observation with `supersedes_id` pointing to the original. The original is never edited or deleted.

---

## 4.2 Feedback Signal

A classified Observation or set of Observations, assigned to a feedback level (1–5) by the Signal Classifier.

```yaml
FeedbackSignal:
  id: UUID
  observation_refs: [UUID]
  feedback_level: 1 | 2 | 3 | 4 | 5
  routing_targets: [EngineID]
  summary: string
  detected_at: timestamp
```

---

## 4.3 Anomaly

A statistical outlier or pattern violation detected during Observation processing.

```yaml
Anomaly:
  id: UUID
  observation_refs: [UUID]
  anomaly_type: VALUE_OUTLIER | PATTERN_BREAK | MISSING_DATA | SOURCE_SUSPICIOUS
  severity: INFO | WARNING | CRITICAL
  quarantine_action: TAKEN | PENDING | CLEARED
  resolution: AnomalyResolution | null
```

---

# 5. Level 2 — Knowledge

## 5.1 KnowledgeRecord

The atomic persistent unit of learning. Immutable once created; all change creates new versions.

```yaml
KnowledgeRecord:
  id: UUID
  type: FACT | PATTERN | RULE | LESSON | EXTERNAL_CLAIM
  subtype: string# more specific classification
  statement: string                 # human-readable declarative sentence
  formal_statement: LogicalForm | null  # structured encoding if applicable
  scope: Scope
  confidence: float                 # 0.01–0.99, never0 or 1 (CON-ETH-003)
  confidence_basis: COMPUTED | INHERITED | TRANSFERRED | SEEDED
  evidence_refs: [Observation.id | KnowledgeRecord.id]
  contradiction_refs: [Observation.id | KnowledgeRecord.id]
  provenance: Provenance
  status: CANDIDATE | ACTIVE | DEPRECATED | ARCHIVED
  validation_count: int
  last_validated_at: timestamp
  embedding_vector: float[]# for semantic similarity
  tags: [string]
  supersedes_id: UUID | nullsuperseded_by_id: UUID | null

Provenance:
  source_type: EXPERIMENT | REFLECTION | CONSOLIDATION | TRANSFER | EXTERNAL | SEED
  source_id: UUID
  created_by_engine: EngineID
  created_at: timestamp
```

## 5.2 KnowledgeRecord Types

| Type | Definition | Example |
|---|---|---|
| `FACT` | Observed truth with direct evidence | "3-minute intros have 67% average retention in scope X" |
| `PATTERN` | Repeating correlation across multiple experiments | "Question hooks consistently outperform statistic hooks in this niche" |
| `RULE` | IF-THEN conditional claim with scoped applicability | "IF hook=question AND length<12m THEN selection_rate > 9% WITH85% confidence" |
| `LESSON` | Directional learning derived from experiment outcome | "Using specific numbers in titles improved selection_rate" |
| `EXTERNAL_CLAIM` | Imported from outside (research, competitor data) | "Industry average CTR is 4–5%" |

**Type hierarchy for evidence weighting:** `FACT` > `PATTERN` > `RULE` > `LESSON` > `EXTERNAL_CLAIM`

---

## 5.3 Rule

A KnowledgeRecord subtype with formal conditional structure.

```yaml
Rule:
  knowledge_record_id: UUID
  condition: Condition              # antecedent: IF part
  outcome: Outcome                  # consequent: THEN part
  scope: Scope
  confidence: float
  support_count: int                # experiments confirming
  contradiction_count: int          # experiments contradicting
  effect_size: float                # magnitude of the outcome
  p_value_equivalent: float | null  # statistical significance when available

Condition:
  variable_constraints: [VariableConstraint]  # variable=value or range
  scope_requirements: Scope

Outcome:
  metric: Metric.canonical_name
  direction: INCREASE | DECREASE | NO_CHANGE
  magnitude: Range# expected effect size bounds
  unit: string
```

---

## 5.4 Lesson

A directional learning claim derived from a single Experiment's Reflection.

```yaml
Lesson:
  knowledge_record_id: UUID
  experiment_id: UUID
  direction: POSITIVE | NEGATIVE | NEUTRAL | CONTRADICTORY
  dimension: string                 # what dimension this lesson concerns
  claim: string                     # human-readable takeaway
  supporting_observations: [UUID]
  confidence_at_creation: float
  promoted_to_rule: bool
  promotion_rule_id: UUID | null
```

---

## 5.5 KnowledgeEdge

A typed relationship between KnowledgeRecord nodes in the graph.

```yaml
KnowledgeEdge:
  id: UUID
  from_id: KnowledgeRecord.id
  to_id: KnowledgeRecord.id
  relation: KnowledgeRelation
  weight: float                # 0.0–1.0 strength
  created_at: timestamp
  provenance: Provenance

KnowledgeRelation:EVIDENCE_FOR        # from is evidence supporting to
  CONTRADICTS         # from is evidence against to
  DERIVED_FROM        # to was computed from from
  SUPERSEDES          # from replaces to
  CONSOLIDATED_INTO   # from merged into to
  TRANSFERRED_FROM    # scope transfer, confidence discounted
  RELATES_TO          # weaker semantic connection
  SPECIALIZES         # from is a specific case of to
```

---

# 6. Level 3 — Cognition

## 6.1 Belief

A confidence-weighted conclusion about the world, derived from KnowledgeRecords, continuously updated.

```yaml
Belief:
  id: UUID
  statement: string
  scope: Scope
  confidence: float
  stability_score: float            # low variance over recent updates = high stability
  is_load_bearing: bool             # many decisions depend on this
  derived_from: [KnowledgeRecord.id]
  confidence_history: [ConfidencePoint]
  last_challenged_at: timestamp | null
  last_validated_at: timestamp | null
  status: ACTIVE | SUSPENDED | RETIRED

ConfidencePoint:
  timestamp: timestamp
  confidence: float
  trigger: string# what caused this update
  causing_event_id: UUID
```

---

## 6.2 Hypothesis

A falsifiable prediction about the outcome of a future experiment.

```yaml
Hypothesis:
  id: UUID
  experiment_id: UUID | null        # null until assigned
  formal_form: FalsifiableForm      # strict structure required
  source: HypothesisSource
  priority_score: float
  status: PROPOSED | ACTIVE | CONFIRMED | FALSIFIED | ABANDONED

FalsifiableForm:
  if_variable: Variable.id
  changes_from: Value
  changes_to: Value
  in_scope: Scope
  then_metric: Metric.canonical_name
  change_direction: INCREASE | DECREASE
  change_magnitude: Range
  within_window: Duration
  expected_confidence: float

HypothesisSource:
  type: STALE_BELIEF | CONTRADICTION_RESOLUTION | STRATEGIC | SURPRISE | EXPLORATION
  source_ref: UUID                # the belief, reflection, or strategy that triggered it
```

**Validation rule:** Any Hypothesis where `formal_form` cannot produce a falsifiable experimental test is rejected at creation.

---

## 6.3 Prediction

A specific, quantified forecast attached to an Experiment before execution.

```yaml
Prediction:
  id: UUID
  experiment_id: UUID
  hypothesis_id: UUID
  metric_predictions: [MetricPrediction]
  stated_at: timestamp
  stated_confidence: float
  knowledge_used: [KnowledgeRecord.id]
  beliefs_used: [Belief.id]

MetricPrediction:
  metric: Metric.canonical_name
  expected_value: float
  expected_range: Range             # confidence interval
  measurement_window: Duration
```

---

## 6.4 Decision

An irrevocable record of a choice made by the system, with complete reasoning trace.

```yaml
Decision:
  id: UUID
  type: DecisionType
  context: DecisionContext
  candidates: [Candidate]
  scores: [CandidateScore]
  knowledge_used: [KnowledgeRecord.id]
  beliefs_used: [Belief.id]
  policy: EXPLOIT | EXPLORE | FORCED_EXPLORE | HUMAN_DIRECTED
  selected_candidate_id: UUID
  rejection_reasons: map<UUID, RejectionReason>
  risk_score: float
  prediction: Prediction
  made_at: timestamp
  made_by: EngineID

DecisionType:
  STRATEGY_SELECTION
  EXPERIMENT_DESIGN
  CANDIDATE_SELECTION     # topic, hook, title, thumbnail, etc.
  PROVIDER_SELECTION
  SCHEDULE_SELECTION
  META_PARAMETER_CHANGE

Candidate:
  id: UUID
  type: string
  value: any
  score: float
  score_breakdown: map<CriterionName, float>
  risk: float
  novelty: float

RejectionReason:
  primary: string
  evidence_refs: [UUID]
  confidence: float
```

---

## 6.5 Strategy

A multi-experiment plan pursing a long-horizon objective.

```yaml
Strategy:
  id: UUID
  objective: StrategicObjective
  horizon_count: int                # planned number of experiments
  active_experiments: [UUID]
  hypothesis_backlog: [UUID]
  fitness_trend: [FitnessPoint]
  weight_profile_id: UUID
  expiration: ExpirationPolicy
  review_triggers: [ReviewTrigger]
  status: DRAFT | ACTIVE | UNDER_REVIEW | RETIRED

StrategicObjective:
  statement: string
  target_metric: Metric.canonical_name
  target_scope: Scope
  target_horizon: Duration
  target_value: float | null        # null = directional improvement only

ExpirationPolicy:
  type: EXPERIMENT_COUNT | DURATION | FITNESS_PLATEAU | MANUAL
  value: int | Duration

ReviewTrigger:
  type: FITNESS_NEGATIVE | HYPOTHESES_FALSIFIED | ENVIRONMENT_SHIFT | EXPIRED
```

---

# 7. Level 4 — Action

## 7.1 Experiment

A controlled attempt to validate a Hypothesis by executing in a real or simulated environment.

```yaml
Experiment:
  id: UUID
  strategy_id: UUID
  hypothesis_id: UUID
  baseline_ref: UUID | null
  mutations: [Mutation]
  directive: ExperimentDirective
  prediction: Prediction
  measurement_plan: MeasurementPlan
  risk_score: float
  class: VALIDATION | INCREMENTAL | EXPLORATORY | RADICAL | META
  state: ExperimentState
  timeline: [StateTransitionEvent]

ExperimentState:
  DRAFT | HYPOTHESIZED | APPROVED | SCHEDULED | EXECUTING
  | MEASURING | COMPLETED | FAILED | REFLECTED | ARCHIVED

MeasurementPlan:
  metrics: [Metric.canonical_name]
  primary_metric: Metric.canonical_name
  windows: [Duration]
  minimum_data_quality: float
  early_stopping_rules: [StoppingRule]
```

---

## 7.2 Mutation

A single intentional change introduced into an Experiment relative to the baseline.

```yaml
Mutation:
  id: UUID
  experiment_id: UUID
  class: TOPIC | STRUCTURE | PRESENTATION | TIMING | SCOPE | META
  variable_id: Variable.id
  baseline_value: Value
  mutated_value: Value
  distance: NEAR | MID | FAR
  justification: string             # why this mutation was chosen
```

**Invariant:** An Experiment should have exactly1 Mutation unless a multi-mutation budget is explicitly justified in the Decision record (DP-011).

---

## 7.3 ReflectionReport

The mandatory output of every terminal Experiment. Exactly one per Experiment.

```yaml
ReflectionReport:
  id: UUID
  experiment_id: UUID
  prediction: Prediction
  actual: ActualOutcome
  delta: DeltaAnalysis
  surprise_score: float             # 0 = fully expected, 1 = fully surprising
  attribution: [AttributionClaim]
  confounds_identified: [string]
  lessons_proposed: [Lesson.id]
  calibration_impact: CalibrationDelta
  meta_notes: string# observations about the learning process
  generated_at: timestamp
  validated: bool                   # independent validation pass (GOV-RFL-002)

DeltaAnalysis:
  per_metric: map<Metric.canonical_name, MetricDelta>

MetricDelta:
  predicted: float
  actual: float
  absolute_delta: float
  relative_delta: float
  within_expected_range: bool

AttributionClaim:
  mutation_id: Mutation.id
  attributed_effect: MetricDelta
  confidence: float
  alternative_explanations: [string]
```

---

## 7.4 FitnessRecord

Multi-objective evaluation of an Experiment's value to the system.

```yaml
FitnessRecord:
  id: UUID
  experiment_id: UUID
  weight_profile_id: UUID
  vector: FitnessVector
  scalar: float# weighted_sum(vector, weights)
  computed_at: timestamp

FitnessVector:
  learning_yield: float             # validated lessons produced / experiment
  prediction_accuracy: float        # 1- normalized_prediction_error
  performance_delta: float          # primary metric delta vs baseline
  strategic_alignment: float        # contribution to active strategy
  cost_efficiency: float            # value / cost

WeightProfile:
  id: UUID
  version: semver
  weights: map<FitnessVector.field, float>
  rationale: string
  effective_from: timestamp
```

---

## 7.5 ExperimentDirective

The formal instruction package issued by the Core to the Execution Layer.

```yaml
ExperimentDirective:
  id: UUID
  experiment_id: UUID
  issued_at: timestamp
  content_spec: ContentSpec
  publishing_spec: PublishingSpec
  measurement_plan: MeasurementPlan
  constraints: ExecutionConstraints

ContentSpec:
  topic_candidates: [TopicSpec]
  narrative_structure: StructureSpec
  hook_strategy: HookSpec
  visual_strategy: VisualSpec
  length_target: Duration
  title_candidates: [TitleSpec]
  thumbnail_strategy: ThumbSpec

PublishingSpec:
  platform: string
  schedule: SchedulePolicy

ExecutionConstraints:
  resource_budget: ResourceBudget
  approval_required: bool
  approval_mode: AUTONOMOUS | NOTIFY | GATED | GATED_STRICT
  forbidden_mutations: [MutationPattern]  # from Forbidden Registry
```

---

## 7.6 EvolutionCycle

A complete iteration of the evolution loop.

```yaml
EvolutionCycle:
  id: UUID
  sequence: int                # monotonically increasing
  started_at: timestamp
  completed_at: timestamp | null
  step: CycleStep                # current position in the saga
  experiments_issued: [UUID]
  experiments_completed: [UUID]
  lessons_extracted: int
  beliefs_revised: int
  knowledge_created: int
  cycle_fitness: float              # aggregate fitness of completed experiments
  status: RUNNING | COMPLETED | FAILED | PAUSED

CycleStep:
  MEMORY_CONSOLIDATION | BELIEF_DECAY | HYPOTHESIS_REFRESH
  | STRATEGY_REVIEW | EXPERIMENT_SELECTION | DIRECTIVE_ISSUANCE
  | AWAITING_EXECUTION | OBSERVATION_INGESTION | REFLECTION
  | LESSON_EXTRACTION | FITNESS_COMPUTATION | META_EVALUATION
  | COMPLETED
```

---

# 8. Level 5 — Governance

## 8.1 GovernancePolicy

A versioned set of constraints and thresholds governing system behavior.

```yaml
GovernancePolicy:
  id: UUID
  version: semver
  effective_from: timestamp
  parameters: GovernancePolicyParameters

GovernancePolicyParameters:
  min_exploration_rate: float       # default 0.10
  max_exploration_rate: float       # default 0.40
  radical_experiment_budget: int    # max concurrent RADICAL (default 0)
  max_publications_per_day: int
  max_cost_per_experiment: Money
  monthly_budget_ceiling: Money
  approval_mode: ApprovalMode
  forbidden_mutations: [MutationPattern]
  decay_window_days: int
  consolidation_similarity_threshold: float
  min_evidence_count: int
  calibration_audit_interval_days: int
```

---

## 8.2 AuditEvent

An immutable record of a governance-significant action.

```yaml
AuditEvent:
  id: UUID
  timestamp: timestamp
  actor: ActorRef                # human user or service identity
  action: AuditActionType
  target_entity: EntityRef
  context: string
  outcome: SUCCESS | FAILURE | PARTIAL
  is_override: bool                # was this an owner override?

AuditActionType:
  APPROVE | REJECT | PAUSE | RESUME | ROLLBACK | REDIRECT
  | CONFIG_CHANGE | POLICY_CHANGE | SECRET_ROTATION
  | KILL_SWITCH_ACTIVATED | AUTONOMY_MODE_CHANGED
  | EXPERIMENT_CLASS_CHANGE | WEIGHT_PROFILE_CHANGE
```

---

## 8.3 LearningHealthReport

Periodic self-assessment of the learning process quality.

```yaml
LearningHealthReport:
  id: UUID
  cycle_window: [int, int]          # cycle sequence range
  generated_at: timestamp
  prediction_error_trend: TrendDirection
  calibration_error: float
  learning_yield: float
  exploration_effectiveness: float
  cost_per_validated_lesson: Money
  belief_stability_avg: float
  goodhart_alerts: int
  recommendations: [HealthRecommendation]

HealthRecommendation:
  level: int        # 0–2per Vol5§10.1
  parameter: string
  current_value: any
  recommended_value: any
  rationale: string
  confidence: float
```

---

# 9. Level 6 — Relations (Summary Graph)

```text
Observation──evidence-for──────────────► KnowledgeRecord
Observation ──contradicts────────────────► KnowledgeRecord
Observation ──measured-by────────────────► Experiment
KnowledgeRecord ──derives──► Belief──used-by──► Decision
KnowledgeRecord ──supersedes──► KnowledgeRecord
KnowledgeRecord ──consolidated-into──► KnowledgeRecord
KnowledgeRecord ──transferred-from──► KnowledgeRecord (scope change)
KnowledgeRecord ──specializes──► KnowledgeRecord
Belief ──generates──► Hypothesis (when stale or contradicted)
Hypothesis ──tested-by──► Experiment
Experiment ──contains──► Mutation
Experiment ──produces──► Observation
Experiment ──produces──► ReflectionReport
Experiment ──planned-by──► Strategy
ReflectionReport ──proposes──► Lesson (KnowledgeRecord)
Lesson ──promotes-to──► Rule (KnowledgeRecord)
Decision ──selects──► Candidate
Decision ──cites──► KnowledgeRecord
Decision ──cites──► Belief
Decision ──predicts──► Prediction
Prediction ──compared-in──► ReflectionReport
FitnessRecord ──evaluates──► Experiment
FitnessRecord ──uses──► WeightProfile
FitnessRecord ──informs──► Strategy
EvolutionCycle ──issues──► ExperimentDirective
ExperimentDirective ──drives──► Experiment
GovernancePolicy ──constrains──► Decision
GovernancePolicy ──constrains──► Mutation
AuditEvent ──records──► GovernanceAction
```

---

# 10. Level 7 — Events (Canonical Domain Event Catalog)

All events follow the EventEnvelope (Vol 2§9.2). Payload types are defined below.

| Event Type | Producer | Payload Key Fields |
|---|---|---|
| `ObservationReceived` | Observation Gateway | observation_id |
| `ObservationQuarantined` | Observation Gateway | observation_id, reason |
| `ObservationIntegrated` | Signal Classifier | observation_id, feedback_level |
| `AnomalyDetected` | Signal Classifier | anomaly_id, severity |
| `KnowledgeRecordCreated` | Knowledge Engine | record_id, type, confidence |
| `KnowledgeRecordActivated` | Knowledge Engine | record_id |
| `KnowledgeRecordDeprecated` | Knowledge Engine | record_id, reason |
| `KnowledgeConsolidated` | Memory Engine | merged_ids, consolidated_into_id |
| `BeliefCreated` | Belief Engine | belief_id, confidence |
| `BeliefRevised` | Belief Engine | belief_id, old_confidence, new_confidence, trigger |
| `BeliefStale` | Belief Engine | belief_id, last_validated_at |
| `BeliefRevisionRequired` | Learning Engine | belief_id, contradiction_ref |
| `HypothesisProposed` | Hypothesis Engine | hypothesis_id, source_type |
| `HypothesisActivated` | Experiment Engine | hypothesis_id, experiment_id |
| `HypothesisConfirmed` | Reflection Engine | hypothesis_id, effect_size |
| `HypothesisFalsified` | Reflection Engine | hypothesis_id, actual_outcome |
| `DecisionMade` | Decision Engine | decision_id, type, policy |
| `ExperimentCreated` | Experiment Engine | experiment_id, class |
| `ExperimentApproved` | Decision Engine / Human | experiment_id |
| `ExperimentScheduled` | Scheduler | experiment_id, scheduled_at |
| `ExperimentStarted` | Orchestrator | experiment_id |
| `ExperimentCompleted` | Orchestrator | experiment_id |
| `ExperimentFailed` | Orchestrator | experiment_id, reason |
| `ExperimentDirectiveIssued` | Experiment Engine | directive_id, experiment_id |
| `ReflectionProduced` | Reflection Engine | reflection_id, surprise_score |
| `LessonExtracted` | Learning Engine | lesson_id, experiment_id |
| `LessonActivated` | Knowledge Engine | lesson_id, rule_id (if promoted) |
| `FitnessComputed` | Fitness Engine | fitness_id, scalar |
| `StrategyCreated` | Strategy Engine | strategy_id |
| `StrategyRevised` | Strategy Engine | strategy_id, trigger |
| `StrategyRetired` | Strategy Engine | strategy_id, reason |
| `EvolutionCycleStarted` | Cycle Saga | cycle_id, sequence |
| `EvolutionCycleCompleted` | Cycle Saga | cycle_id, summary |
| `SelfEvaluationTriggered` | Meta-Reflection | cycle_range, trigger |
| `LearningHealthReportProduced` | Meta-Reflection | report_id |
| `GoodhartAlertRaised` | Fitness Engine | metric_pair, divergence_score |
| `KillSwitchActivated` | Governance | actor_id, scope |
| `AutonomyModeChanged` | Governance | old_mode, new_mode, actor_id |
| `ConfigChanged` | Config Service | parameter, old_value, new_value, actor_id |
| `PolicyVersionActivated` | Governance | policy_id, version |

---

# 11. Ontology Change Procedure (ONT-001)

Adding or modifying ontology entries follows this process:

```text
1. PROPOSEOpen a governance issue with: entity name, definition,lifecycle, key attributes, relations, rationale

2. REVIEW    Any two contributors review for: duplication with existing
             concepts, consistency with volumes1–5, implementation impact

3. ADRIf the addition changes an existing entity, an ADR is
             required documenting the breaking change

4. DOCUMENTThis file is updated first, before any code

5. PROPAGATE Database schemas, API contracts, prompt templates, and
             documentation updated in the same PR

6. VERIFY    Integration tests confirm the new entity flows through
             the full event chain from creation to storage to retrieval
```

**No entity may exist in implementation without a record here.**

---
---

# 07_EvolutionOS_ADR_Register.md

# ARCHITECTURE DECISION RECORDS

**Format:** Each ADR states Context, Decision, Rationale, Consequences, and Status.
**Status values:** ACCEPTED | SUPERSEDED | DEPRECATED | PROPOSED

---

# ADR-001— Capabilities Instead of Services

**Status:** ACCEPTED
**Date:** Baseline

### Context

Traditional software architectures are organized around services or modules (UserService, ContentService). Applied to an AI learning system, this creates a structural mismatch: the question "which service handles learning?" has no clean answer because learning is a cross-cutting concern involving storage, inference, and planning together.

### Decision

EvolutionOS introduces a Capabilities layer: five cognitive abilities (Learn, Reason, Create, Observe, Evolve) that define *what the system can do*, implemented by specialized Engines that define *how it does it*. The Capabilities layer is stable; the Engine layer evolves.

### Rationale

* Cognitive modeling matches the problem domain better than business-service modeling
* Stable capability names survive implementation changes
* New developers can navigate the system by asking "which capability does this serve?"
* Platform independence falls naturally out of this model: "Create" exists regardless of whether creating a video or a blog post

### Consequences

**Positive:** Conceptual clarity; extensibility; natural platform independence

**Trade-off:** One additional abstraction layer requiring discipline to maintain. Engineers must resist the temptation to map capabilities1:1 to services.

---

# ADR-002 — Knowledge at the Center, LLMs at the Periphery

**Status:** ACCEPTED
**Date:** Baseline

### Context

The dominant pattern in AI-powered applications places the LLM at the architectural center: the model receives context, reasons, and returns output. Memory, if it exists, is typically context stuffed into the prompt window. This creates hard limits: no persistent learning, no auditability, no provider independence, and reasoning that evaporates after each interaction.

### Decision

EvolutionOS inverts this. The **Knowledge Layer** is the center of the architecture. LLMs are stateless tools invoked by engines when inference is needed. Every significant reasoning output (a decision, a lesson, a reflection) is immediately externalized into the Knowledge Layer as a structured record — not left inside the model.

### Rationale

* Knowledge persists across model changes, provider switches, and software upgrades
* Decisions become reproducible: given the same knowledge state, reasoning can be replayed
* Explainability is structural: the evidence chain exists in the database, not in model weights
* Provider independence is guaranteed: swapping GPT-4 for Gemini changes nothing in the Knowledge Layer
* The system genuinely accumulates intelligence rather than simulating it per-prompt

### Consequences

**Positive:** Persistent learning; provider independence; full auditability; reproducible decisions; survives any single model's deprecation

**Trade-off:** Requires substantial engineering discipline. Engineers must resist returning to the simpler pattern of "just ask the LLM." Every significant inference must produce a persisted, structured artifact.

---

# ADR-003 — YouTube as an Execution Environment, Not a Core Concept

**Status:** ACCEPTED
**Date:** Baseline

### Context

The initial use case is YouTube content. The naive architecture would model the system around YouTube — channels, videos, thumbnails, CTR — making these first-class concepts in the core data model.

### Decision

YouTube is an execution plugin. The Core knows nothing about videos, thumbnails, channels, or YouTube-specific metrics. The Core knows only: Observations (with canonical metric names), Experiments, and Directives. The YouTube Adapter translates between these canonical concepts and YouTube's native API surface.

### Rationale

Treating YouTube as core would mean every future platform (blog, podcast, TikTok) requires Core changes. Treating it as a plugin means adding a platform = implementing one adapter contract + one metric mapping table, with zero changes to the learning, reasoning, or evolution engines.

### Consequences

**Positive:** True platform independence; future platforms at near-zero architectural cost; Core can be reused for non-content domains

**Trade-off:** The Directive schema must be abstract enough to express any experiment, which adds design complexity. The metric normalization layer requires careful maintenance to ensure cross-platform knowledge transfer is semantically valid.

---

# ADR-004 — Immutable Knowledge Records

**Status:** ACCEPTED
**Date:** Baseline

### Context

When new evidence contradicts an existing knowledge record, the tempting option is to edit or delete the old record. This is how most databases work.

### Decision

Knowledge records are append-only. A contradicted record transitions to `DEPRECATED` status. A corrected record is superseded by a new record with `supersedes_id` pointing to the original. Neither is ever edited or deleted.

### Rationale

* The history of what the system believed, and when, is itself valuable data
* Debugging why a strategy failed requires knowing what beliefs were active at the time
* Reproducing historical decisions requires access to the exact knowledge state at that moment
* Contradiction evidence is scientifically valuable — discarding it loses information
* Auditability: "why did the system do X in week12?" becomes answerable

### Consequences

**Positive:** Complete learning history; time-travel debugging; reproducible decisions; full auditability; genuine evidence-based contradictions rather than silent overwrites

**Trade-off:** Storage grows monotonically. Requires active consolidation and archival policies (Memory Engine) to remain manageable. The knowledge graph can become complex. Mitigated by: content-addressed storage, hierarchical indexing, confidence-weighted retrieval (high-confidence active records retrieved first), and archival removing deprecated records from active indexes while preserving them for audit.

---

# ADR-005 — Mandatory Explainability for Every Strategic Decision

**Status:** ACCEPTED
**Date:** Baseline

### Context

Most AI systems produce outputs without preserving reasoning. When asked "why did you choose this topic?", they cannot answer. This is acceptable for disposable outputs; it is unacceptable for a system meant to improve through accumulated experience.

### Decision

Every strategic decision must be recorded as a `DecisionRecord` before it takes effect. The record is immutable, contains all candidates considered (not just the winner), all scores, all evidence and beliefs cited, the selection policy, and a `Prediction` of expected outcome. Decisions that cannot produce this record are not permitted to execute.

### Rationale

* Explainability is not a feature added later — it is a structural invariant
* The owner must always be able to ask "why?" and receive a complete answer
* Decision records are the primary input to reflection: prediction vs. reality comparison requires knowing the original prediction
* Regulatory and ethical compliance becomes easier when every decision is auditable by design

### Consequences

**Positive:** Full explainability; reflection becomes structurally possible; owner trust; debugging capability; the "Five Whys" dashboard contract is satisfiable

**Trade-off:** Decision recording adds latency and storage overhead to every strategic choice. Mitigated by: async write path for non-critical decisions, batched storage, and the observation that strategic decisions are infrequent relative to operational events.

---

# ADR-006 — Experiments as the Atomic Unit of Progress

**Status:** ACCEPTED
**Date:** Baseline

### Context

Alternative framings of progress: publish count (number of videos), engagement metrics (views, subscribers), or time elapsed. Each creates perverse incentives: maximizing publish count rewards speed over learning; maximizing engagement rewards popularity over strategy quality.

### Decision

An `Experiment` — a controlled attempt to validate a `Hypothesis` with a pre-registered `Prediction` and structured `Reflection` — is the atomic unit by which EvolutionOS measures its own progress. Fitness is computed per experiment. The system's intelligence is measured by the quality and quantity of validated knowledge produced by experiments, not by publication volume or engagement numbers.

### Rationale

* Aligns measurement with the actual objective (learning, not content)
* Forces hypothesis-driven thinking before every execution
* Makes negative results first-class: a falsified hypothesis is a completed experiment with positive learning value
* Decouples intelligence growth from platform algorithm volatility

### Consequences

**Positive:** Correct incentive alignment; learning-first culture enforced structurally; negative results valued

**Trade-off:** Slower initial output than a pure content-generation system. Accepted by design (NG-003, PG-001).

---

# ADR-007 — Confidence Is Mandatory on Every Belief and Rule

**Status:** ACCEPTED
**Date:** Baseline

### Context

Binary knowledge representation — a thing is either known or unknown — is inappropriate for a system that learns from noisy, incomplete real-world data. A system that treats a single-experiment correlation with the same certainty as a finding replicated across 50 experiments will make poor decisions.

### Decision

Every `Belief`, `Rule`, and `KnowledgeRecord` carries a `confidence` score in the range (0.01, 0.99). The bounds are exclusive: 0 would mean certain falsehood (we would not store it); 1 would claim certainty (CON-ETH-003forbids it). Confidence is always computed from evidence, never manually assigned except for seed knowledge (which is marked `confidence_basis: SEEDED` and deprioritized).

### Rationale

* Real-world patterns are probabilistic; the knowledge model must reflect this
* Confidence-weighted retrieval allows the Decision Engine to rank evidence appropriately
* Confidence decay for unvalidated beliefs prevents stale certainty
* Calibration measurement (KPI-BEL-002) becomes possible only when confidence is explicit

### Consequences

**Positive:** Nuanced reasoning; calibration measurement; appropriate epistemic humility; decay mechanics; better decision quality under uncertainty

**Trade-off:** Confidence math must be well-defined and consistently applied. The Bayesian-inspired update function (FR-EC-202) must be validated against the calibration KPI continuously; systematic miscalibration is a detectable and correctable defect.

---

# ADR-008 — Platform Independence as a Structural Invariant

**Status:** ACCEPTED
**Date:** Baseline

### Context

Many systems claim platform independence but implement it as "we could refactor this later." EvolutionOS makes platform independence structurally impossible to violate through the Core boundary rule (EC-BND-001).

### Decision

The Evolution Core module is prohibited at the code level from importing or referencing any execution-layer concept. This is enforced by: module boundary tests in CI (any import of execution-layer packages from Core packages fails the build), the event-only communication contract (EC-BND-002), and the abstract Directive/Observation schema which contains no platform-specific fields.

### Rationale

* "We could refactor it later" never happens; structural enforcement is the only reliable approach
* The Core's long-term value is precisely its reusability; compromising this for convenience destroys the fundamental architecture
* Future domain expansion (ADR-003extended) to non-content environments requires this invariant to hold

### Consequences

**Positive:** Guaranteed platform independence; Core reusability; clean architecture

**Trade-off:** Requires module boundary enforcement tooling in CI. The abstract Directive schema must be expressive enough for all current and future execution environments without becoming a leaky abstraction.

---

# ADR-009 — Event-Driven Communication Between Bounded Contexts

**Status:** ACCEPTED
**Date:** Baseline

### Context

Direct method calls between engines create tight coupling: changing one engine's interface breaks its callers; adding a new consumer of an event requires modifying the producer. For a system expected to evolve indefinitely, tight coupling is architectural debt that compounds.

### Decision

All communication between bounded contexts (per Vol 2 §4.1) occurs exclusively through domain events on the event bus. An engine publishes events describing what happened; it does not call other engines directly. Any engine may subscribe to any event without the producer's knowledge.

### Rationale

* Producers and consumers evolve independently
* New engines can be added by subscribing to existing events, zero changes to existing code
* The event log is a complete history of system activity (enabling event sourcing, ADR-011)
* Testing becomes easier: inject events to test consumers; assert events to test producers

### Consequences

**Positive:** Loose coupling; independent evolution; complete audit trail; natural fit with event sourcing; easy consumer addition

**Trade-off:** Eventual consistency between contexts. Cross-context workflows require sagas rather than transactions (EvolutionCycleSaga, Vol 2 §13). Debugging requires correlation ID tracing across events. These complexities are accepted because the coupling cost of the alternative compounds indefinitely.

---

# ADR-010 — Evolution Optimized Over Content Production

**Status:** ACCEPTED
**Date:** Baseline

### Context

The most common success metric for content automation systems is output volume (videos per week) or engagement metrics (views, subscribers). Optimizing for these creates systems that produce high volumes of low-learning content.

### Decision

EvolutionOS optimizes for `learning_yield` (validated lessons per experiment) as its primary fitness dimension, weighted above `performance_delta` (engagement metrics) in the default FitnessVector weight profile. Content production is a means to generate learning opportunities, not an end in itself.

### Rationale

* Long-term: a system that learns faster will eventually outperform one that publishes faster
* Correct incentive alignment: the system should want to learn, not to publish
* Protects against the trap of high-volume mediocrity
* Consistent with the mission statement: "transform AI from a passive responder into an active learner"

### Consequences

**Positive:** Correct long-term incentives; learning-first behavior; prevents publish-volume gaming

**Trade-off:** Initial growth slower than a pure content-generation system. Accepted explicitly inNG-003 and PG-001. The owner must understand this trade-off during deployment configuration.

---

# ADR-011 — Event Sourcing for the Evolution Core

**Status:** ACCEPTED
**Date:** Volume 2

### Context

The Core requires: immutable history (ADR-004), decision reproducibility (AC-013), experiment replay for regression testing (NFR-TST-003), and complete audit trails (GOV-AUD-001). Traditional CRUD storage satisfies none of these without additional complexity.

### Decision

The Evolution Core uses event sourcing as its persistence model. Aggregate state is a pure function of its event history. The current state of any aggregate can be reconstructed by replaying its events from the beginning (or from a snapshot). Projections (read models) are built from the event stream.

### Rationale

* Immutability falls naturally from the append-only event log
* Time-travel debugging: replay to any point in history
* Regression testing: replay historical events against new code
* Complete audit trail: every state change has a corresponding event with full context
* Natural fit with the domain: the evolution loop *is* a sequence of events

### Consequences

**Positive:** All of the above

**Trade-off:** Projection maintenance complexity; eventual consistency between write and read models; snapshots needed for large aggregates; upcasters needed for schema evolution. All are well-understood patterns with established solutions.

---

# ADR-012 — CQRS Separation for the Core

**Status:** ACCEPTED
**Date:** Volume 2

### Context

With event sourcing (ADR-011), the write model (aggregates validating commands, emitting events) and read models (projections answering queries) have different optimization requirements. Forcing a single model to serve both degrades both.

### Decision

The Core applies CQRS: commands flow to aggregates through the command bus; queries are served by dedicated projections rebuilt from the event stream. Projections are disposable — any projection can be dropped and rebuilt from the event log without data loss.

### Rationale

* Read models optimized for their query patterns (graph for knowledge browsing, flat for decision tracing, time-series for fitness trends)
* Write model optimized for invariant enforcement
* Projection rebuilds are a powerful tool: schema changes often become "drop + rebuild" rather than migrations
* Dashboard queries never contend with write-path aggregates

### Consequences

**Positive:** Independent optimization; disposable read models; schema flexibility; dashboard performance

**Trade-off:** Two models to maintain; eventual consistency (reads may lag writes by milliseconds on the same host). The lag is acceptable for all known use cases; the dashboard is not a real-time trading system.

---

# ADR-013 — Modular Monolith Deployment First

**Status:** ACCEPTED
**Date:** Volume 4

### Context

Microservice deployments on Free Tier infrastructure are operationally complex and resource-inefficient. True microservices require service mesh, distributed tracing, network partitions, and operational overhead that is inappropriate at v1 scale. However, building a true monolith risks creating coupling that prevents future distribution.

### Decision

v1 deploys as a **modular monolith**: all services run as separate Docker containers on one host, communicating through the same event bus abstraction they would use if distributed. The key constraint: service boundaries are enforced *logically* (separate containers, separate DB schemas, event-only cross-context communication) even though the physical deployment is one host.

### Rationale

* Free Tier viable without compromise
* The architectural discipline of microservices (boundaries, events, data ownership) is enforced without the operational overhead
* Migration path to true distribution is guaranteed because services already communicate correctly: moving a container to another host requires only configuration changes
* "Modular monolith with a microservices escape hatch" is a proven pattern for systems that need to start small and grow

### Consequences

**Positive:** Free Tier viable; operational simplicity; no network partition risk in v1; clean migration path to scale-out

**Trade-off:** Cannot scale individual components independently until distribution occurs. Accepted at v1 scale; monitored by the Free Tier envelope test (per-release gate).

---

# ADR-014 — PostgreSQL as the Universal Store (v1)

**Status:** ACCEPTED
**Date:** Volume 4

### Context

The system needs: an event store, a knowledge graph, relational projections, vector similarity search (for knowledge consolidation), job persistence, and audit logs. The purpose-built alternatives (Neo4j for graph, EventStoreDB for events, Pinecone for vectors, Redis for jobs) each require separate infrastructure, operations, and Free Tier budget.

### Decision

v1 uses PostgreSQL for all persistence needs: event store (append-only table with optimistic concurrency), knowledge graph (relational + recursive CTEs + `ltree`), vector similarity (pgvector extension for semantic consolidation), projections (standard tables), and job state. Each logical concern has its own schema, enforcing ownership boundaries.

### Rationale

* One battle-tested database fits Free Tier memory limits
* PostgreSQL with pgvector handles vector similarity without a separate vector database
* Recursive CTEs handle knowledge graph traversal adequately at v1 scale
* All concerns are hidden behind repository interfaces — the migration path to purpose-built stores is clear when measured thresholds are crossed (e.g., knowledge graph > 1M nodes → evaluate Neo4j)
* Operational simplicity: one backup strategy, one monitoring target, one connection pool

### Consequences

**Positive:** Free Tier viable; operational simplicity; one backup/restore surface; graph queries possible without Neo4j

**Trade-off:** Graph queries less elegant than a native graph DB; vector search performance limited compared to purpose-built stores at large scale. Both are explicitly deferred: scale triggers for evaluation are defined (RSK-006), and repository interfaces ensure migration is a swap, not a rewrite.

---

# ADR-015 — Redis Streams as the Event Bus (v1)

**Status:** ACCEPTED
**Date:** Volume 4

### Context

The event-driven architecture (ADR-009) requires a message broker. Options: RabbitMQ (full-featured, heavier), Kafka (high-throughput, complex), managed queues (SQS, costly), or Redis Streams (lightweight, persistent, consumer groups, single-host friendly).

### Decision

v1 uses Redis Streams behind a `MessageBroker` interface. The interface is the only coupling point; the implementation is swappable. Redis Streams provides: consumer groups (competing consumers), stream persistence (survive broker restart), replay from offset, and dead-letter stream support — all required features at negligible memory overhead.

### Rationale

* Redis is already justified as the caching layer (Vol 4 §8) — one less service
* Redis Streams has all required semantics for v1 throughput
* The `MessageBroker` interface means graduating to RabbitMQ, Kafka, or SQS requires implementing one interface, zero changes elsewhere
* At single-host scale, network partition between Redis and consumers is not a meaningful risk

### Consequences

**Positive:** Lightweight; Free Tier viable; persistent; replayable; swappable

**Trade-off:** Redis Streams lacks some Kafka features (log compaction, exactly-once semantics, multi-datacenter replication). All are irrelevant at v1 scale and deferred with a clear upgrade path.

---

# ADR-016 — Safety Constraints Live Outside the Learning Loop

**Status:** ACCEPTED
**Date:** Volume 5

### Context

A learning system optimizes toward its fitness function. If ethical and safety constraints are implemented as soft penalties within the fitness function, the system will learn to minimize those penalties while maximizing fitness — effectively learning to game its own safety rules. This is a well-documented failure mode in reinforcement learning systems.

### Decision

Ethical and safety constraints (GOV-ETH-001 through GOV-ETH-005, GOV-SAF-001 through GOV-SAF-003) are implemented as **hard gates upstream of the learning loop**, not as fitness penalties. The Forbidden Mutation Registry is checked before a Directive is issued. The content policy filter is applied before publishing. The system never receives a reward signal from an action that violates a hard constraint, because the action never executes.

### Rationale

* You cannot learn to circumvent a rule you never get to test
* Fitness function penalties create an adversarial optimization dynamic — the system will find edge cases
* Hard gates are verifiable: CI tests can confirm that no violating action ever reaches execution
* Conceptually clean: the learning loop is about "how to achieve objectives well" — the constraints define "within these non-negotiable boundaries"

### Consequences

**Positive:** Robust safety; no adversarial optimization of constraints; verifiable in CI; conceptually clean separation

**Trade-off:** Hard gates require comprehensive constraint specification upfront. Gaps in the Forbidden Registry can create blind spots. Mitigated by: human-editable registry (GOV-MUT-002), pre-publication content policy filter as a second gate, and anomaly self-halt (GOV-SAF-003) as a final backstop.

---

# ADR-017 — Progressive / Earned Autonomy

**Status:** ACCEPTED
**Date:** Volume 5

### Context

Deploying a fully autonomous system from day one requires trusting that the system's judgment aligns with the owner's values before any evidence of alignment exists. This is how autonomous systems earn distrust and get shut down.

### Decision

Autonomy is earned through demonstrated alignment. The system starts in `GATED_STRICT` mode. Transitions to `GATED` → `NOTIFY` → `AUTONOMOUS` (for specific experiment classes) are driven by KPI-GOV-001 (override rate trending toward zero), not by configuration or time. The system itself learns to predict what the owner would approve and surfaces that reasoning; as prediction accuracy increases, autonomy expands.

### Rationale

* Trust is built by evidence, consistent with the system's own epistemology
* Owner rejections are Level-4 feedback — valuable learning signal, not failures
* Progressive autonomy makes the system more trustworthy in practice, not just in specification
* Aligns with the broader principle: evidence before belief, demonstration before trust

### Consequences

**Positive:** Owner trust earned empirically; autonomy expansion is justified and measurable; owner rejections contribute to learning; safer deployment

**Trade-off:** Initial deployment requires more owner attention. This is correct — the system has not yet earned trust.

---

# ADR-018 — Simulation Before Reality

**Status:** ACCEPTED
**Date:** Volume 5 Roadmap

### Context

Deploying an untested learning system against a real platform risks: publishing low-quality content, wasting API budget, and generating misleading data that corrupts the knowledge base before the system has any valid knowledge.

### Decision

The v0.2 milestone gates ALL real-world activity behind the Simulation Harness (FR-EC-601). The Core engines must demonstrate planted-rule discovery (≥ 80%) and calibrated confidence in a synthetic environment before any real experiment is issued. This gate is mandatory and cannot be bypassed by configuration.

### Rationale

* Intelligence verification before real-world consequences
* A system that cannot find rules planted in a controlled environment will not find them in the noisy real world
* Protects the knowledge base from early corruption by garbage data
* The simulation environment is cheaper and faster to iterate against than real-world experiments

### Consequences

**Positive:** Intelligence verified before deployment; knowledge base protected; faster iteration during development; CI-integrated intelligence regression testing

**Trade-off:** Simulation environment must be carefully designed so that planted rules resemble real-world patterns without being trivially easy. Overfitting to the simulation environment is a risk; mitigated by keeping simulation rules realistic and varied.

---

# ADR-019 — Shadow Mode for Meta-Mutations

**Status:** ACCEPTED
**Date:** Volume 5

### Context

Meta-mutations (Level1–2self-modifications: changing learning rates, fitness weights, consolidation thresholds) affect the entire learning process. Deploying them directly risks degrading system-wide performance before the problem is detected.

### Decision

All Level 1–2 self-modifications execute in shadow mode first: the new parameters run in parallel against historical data (replay-based evaluation) and synthetic scenarios for a defined evaluation window before taking effect. Live deployment occurs only after shadow results confirm no degradation on reference benchmarks.

### Rationale

* Self-modifications are experiments; experiments require predictions and measurements before commitment
* The system cannot be allowed to degrade its own learning process without a safety net
* Shadow mode leverages the event log (ADR-011) — historical replay is free
* Consistent with the broader principle: evidence before belief, measurement before commitment

### Consequences

**Positive:** Safe self-modification; degradation caught before live impact; leverages existing event replay infrastructure

**Trade-off:** Self-modification latency increased by the shadow evaluation window (default: 7 days or N cycles). Accepted as appropriate caution for changes affecting system-wide behavior.

---

# ADR-020 — Goodhart Counter-Metric Pairing

**Status:** ACCEPTED
**Date:** Volume 5

### Context

Goodhart's Law: "When a measure becomes a target, it ceases to be a good measure." Any metric the system optimizes will eventually be gamed — even by an unconscious optimization process. A system optimizing `selection_rate` (CTR) will drift toward clickbait if CTR is the only signal.

### Decision

Every fitness metric the system optimizes has a mandatory paired counter-metric that watches for divergence. The pairs are defined in GOV-FIT-002 and are non-negotiable: removing a counter-metric pairing requires an ADR. Sustained divergence between an optimized metric and its counter-metric raises a `GoodhartAlert` routing to governance review.

### Rationale

* Structural defense against the most dangerous known failure mode in optimization systems
* Counter-metrics are cheap to monitor and early warning is high value
* The specific pairings chosen reflect domain knowledge: CTR↑ + retention↓ = clickbait; yield↑ + deprecation↑ = junk lessons
* Governance review gives the owner visibility into optimization drift before it causes damage

### Consequences

**Positive:** Structural Goodhart defense; early warning; governance visibility; domain knowledge encoded in the pairing design

**Trade-off:** Requires careful selection of counter-metrics — a poorly chosen counter-metric could itself become a target. Counter-metric pairs are themselves reviewed in the quarterly self-audit (GOV-AUD-002).

---
---

# 08_EvolutionOS_Implementation_Roadmap.md

# IMPLEMENTATION ROADMAP

**Version:** 1.0
**Scope:** v0.1 through v1.0 in detail; v1.5 through v5.0 in outline

---

# Guiding Principle

Every milestone produces a **system that works end-to-end at its current scope**, not a collection of unintegrated components. A milestone is complete only when its gate criteria are met — not when its stories are closed.

> **Simulation gate before reality. Working loop before features. Intelligence verified before autonomy.**

---

# Milestone Overview

```text
v0.1   SkeletonInfrastructure, event bus, config, CI
v0.2   Core Loop (Sim)       All Core engines in simulation — intelligence gate
v0.3   Pipeline (Dry Run)    Full content pipeline, no publishing
v0.4   First ContactYouTube live, GATED_STRICT, first real experiments
v0.5   Learning Verified     Multi-cycle learning, calibration, measurable improvement
v1.0   Supervised Autonomy   Full governance, weekly digests, NOTIFY mode
```

---

# v0.1 — Skeleton

**Goal:** A runnable system with no intelligence yet, but with all the infrastructure required to build intelligence on top of.

**Duration estimate:** 3–4 weeks

## Deliverables

### Infrastructure
- [ ] Repository structure (see Developer Handbook §3for canonical layout)
- [ ] Docker Compose: postgres, redis, all service containers (stubbed), dashboard shell
- [ ] `make bootstrap` — one-command local setup
- [ ] `make test` — full test suite runs cleanly on a fresh checkout
- [ ] Environment config system with validation (INF-CFG-004)
- [ ] Secrets loading (INF-SEC-001) — SOPS for local dev

### Event Infrastructure
- [ ] EventEnvelope schema + serialization
- [ ] MessageBroker interface + Redis Streams implementation
- [ ] Consumer group setup with dead-letter streams
- [ ] Correlation ID propagation middleware
- [ ] Event schema registry (version 0.1.0 of all Vol 2 §9.2events)

### Database
- [ ] PostgreSQL schemas: `core_events`, `core_read`, `knowledge`, `workflow`, `operations`
- [ ] Migration tooling (`alembic` / `flyway` / equivalent — team choice)
- [ ] `core_events` table with append-only DB-level enforcement (INF-DB-001)
- [ ] pgvector extension installed and tested

### Observability
- [ ] Structured JSON logging with mandatory fields (INF-LOG-001)
- [ ] Secret-redaction filter on all log sinks (INF-LOG-003) — canary test in CI
- [ ] Basic Prometheus metrics export per container
- [ ] Correlation ID search in logs demonstrated

### CI/CD
- [ ] Lint → Unit Test → Build → Integration smoke pipeline
- [ ] Secret canary test (INF-CI-002prerequisite)
- [ ] Image tagging with git SHA

### Dashboard Shell
- [ ] Auth-gated login (placeholder credentials)
- [ ] Empty views for all 9 dashboard sections (Vol 3 §18.1) — no data yet
- [ ] Health status panel showing container states

## Gate Criteria

```
✓ make bootstrap completes on a fresh checkout
✓ All containers healthy in docker compose ps
✓ An event written to core_events cannot be updated or deleted (test this explicitly)
✓ Correlation ID appears in every log line when set
✓ CI pipeline green
✓ No secrets in any log output (canary test passes)
```

---

# v0.2 — Core Loop in Simulation

**Goal:** All five Core capabilities (Learn, Reason, Observe, Evolve, and the core-side of Create decisions) running end-to-end in a simulation environment with planted ground-truth rules.

**Duration estimate:** 6–8 weeks

**This is the most important milestone. Do not proceed to v0.3 until the intelligence gate passes.**

## The Simulation Environment

The simulation environment is a synthetic world that:

1. Has a fixed set of **planted rules** — e.g.:
   - "In scope `{niche: test_a}`, question hooks increase `selection_rate` by 12–18%"
   - "In scope `{niche: test_a}`, content length > 15 minutes decreases `attention_rate` by 20–30%"
   - "In scope `{niche: test_b}`, statistic hooks outperform question hooks"
   - 8–12 planted rules total, varied by scope, metric, and direction
2. Returns synthetic observations with realistic noise (±15% variance) when experiments are executed against it
3. Is deterministic given a seed — enabling reproducible CI runs
4. Has a "ground truth oracle" that can verify at test time whether the Core discovered the planted rules

## Deliverables

### Ontology Implementation
- [ ] All Level 0–4 ontology entities (Vol 6 §3–7) as code data classes / schemas
- [ ] Ontology validation: any entity construction with missing required fields fails at creation time

### Event Store
- [ ] Aggregate base class: command handling, event emission, optimistic concurrency
- [ ] Snapshot mechanism (every 100 events per aggregate)
- [ ] Projection consumer base class: offset persistence, idempotent processing
- [ ] Event replay utility (for testing and debugging)

### Core Engines — Phase 1: Perception + Learning
- [ ] **Observation Gateway:** schema validation, quarantine, integration, `ObservationIntegrated` events
- [ ] **Signal Classifier:** feedback level assignment (1–5), routing
- [ ] **Knowledge Engine:** CRUD + graph edges + vector similarity (pgvector), consolidation, status transitions
- [ ] **Learning Engine:** lesson extraction pipeline, statistical guardrails (FR-EC-111), contradiction handling
- [ ] **Reflection Engine:** `ReflectionReport` generation, surprise scoring, meta-reflection scaffolding

### Core Engines — Phase 2: Reasoning
- [ ] **Belief Engine:** confidence update function, decay, `BeliefRevised` events, stability tracking
- [ ] **Hypothesis Engine:** falsifiable form validation, backlog management, prioritization
- [ ] **Decision Engine:** 8-step protocol (FR-EC-210), candidate generation, exploration policy
- [ ] **Strategy Engine:** strategy lifecycle, review triggers, expiration

### Core Engines — Phase 3: Evolution
- [ ] **Experiment Engine:** full state machine, directive issuance
- [ ] **Mutation Engine:** taxonomy, distance scoring, budget enforcement
- [ ] **Fitness Engine:** vector computation, weight profiles, anti-gaming rule (FR-EC-432)
- [ ] **Memory Engine:** consolidation cycle, decay application, MemoryHealthReport

### EvolutionCycleSaga
- [ ] Full12-step saga with checkpoint persistence (FR-EC-
###EvolutionCycleSaga (continued)
- [ ] Full12-step saga with checkpoint persistence (FR-EC-502)
- [ ] Portfolio management: multiple concurrent experiments
- [ ] Cycle resumability after crash/restart
- [ ] `EvolutionCycleStarted` / `EvolutionCycleCompleted` events

### Simulation Harness
- [ ] Synthetic world engine with configurable planted rules
- [ ] Noise injection (configurable variance per metric)
- [ ] Deterministic seed-based execution
- [ ] Ground truth oracle: given a rule ID, return whether the Core has discovered it with acceptable confidence
- [ ] Simulation runner: execute N cycles against the synthetic world, return discovery report

### Projections (Read Models)
- [ ] Knowledge Graph projection (browsable, depth-limited graph queries)
- [ ] Decision Trace projection (full reasoning chain per decision)
- [ ] Fitness Timeline projection (trend data per strategy)
- [ ] Belief Snapshot projection (fast retrieval for decision hot path)

### Dashboard — Core Views
- [ ] Knowledge Browser: list, filter by scope/confidence/status, graph view
- [ ] Belief Inspector: active beliefs with confidence histories
- [ ] Decision Explorer: drill-down to candidates, evidence, rejections
- [ ] Experiment Board: kanban by state

## Gate Criteria

```
✓ Simulation gate:≥ 80% of planted rules discovered (ACTIVE status)
   within≤ 50simulated cycles
✓ Calibration gate: stated confidence within±15% of realized frequency
   across all planted rules
✓ Immutability gate: zero knowledge records modified after creation
   (verified by event log integrity check)
✓ Reproducibility gate: identical seed → identical discovery sequence
   (deterministic replay test)
✓ Explainability gate: every decision in the simulation has a complete
   DecisionRecord with≥ 3 candidates, evidence refs, and a prediction
✓ Cycle resume gate: kill the process at every saga step boundary;
   assert it resumes correctly from checkpoint (12separate kill tests)
✓ Contradiction gate: inject contradictory observations for one planted
   rule; assert confidence decreases and BeliefRevisionRequired fires
```

**If any gate criterion fails, fix it before proceeding. No exceptions.**

---

# v0.3 — Pipeline (Dry Run)

**Goal:** A complete content production pipeline that generates all artifacts from an `ExperimentDirective` without publishing anything. The Core issues directives; the pipeline executes them; artifacts are stored; the loop is verified end-to-end without touching any external platform.

**Duration estimate:** 5–7 weeks

## Deliverables

### Workflow Orchestrator
- [ ] Pipeline state machine: all stages RECEIVED → … → THUMBNAIL_READY
- [ ] Checkpoint persistence: every stage writes output artifact ref before advancing
- [ ] Stage timeout + retry per configurable policy
- [ ] Budget enforcement: token + API cost tracking, halt on budget exceeded
- [ ] Parallel stage execution (narration + thumbnail concurrently)
- [ ] Dry-run mode flag: full pipeline, `publish` stubbed (FR-PX-2101)

### Research Pipeline
- [ ] Pluggable search provider interface + first implementation (e.g., SerpAPI, DuckDuckGo)
- [ ] Fact Ledger: claim storage, source tier tracking
- [ ] Hallucination defense: LLM claims rejected without Fact Ledger backing (FR-PX-203)
- [ ] ResearchDossier output schema

### Story Generation Pipeline
- [ ] Structure compliance: Hook/Context/Conflict/Development/Resolution/Reflection
- [ ] Multi-candidate (≥ 3) generation and scoring
- [ ] Retention-aware pacing map annotation

### Script Engine
- [ ] Scene decomposition with `fact_refs` traceability
- [ ] Readability constraint validation
- [ ] Scene-level duration estimation

### Narration Engine
- [ ] TTS provider interface + first implementation (e.g., ElevenLabs, OpenAI TTS)
- [ ] Provider fallback chain
- [ ] Quality gates: duration, silence, clipping, loudness normalization
- [ ] Per-scene regeneration (not full-script)

### Visual Planning Engine
- [ ] Visual strategy execution from directive spec
- [ ] ShotList generation: asset type, query/spec, duration, transition
- [ ] License metadata requirement enforcement (FR-PX-603)

### Video Composition Engine
- [ ] Declarative composition: ShotList + audio → rendered video
- [ ] Render profile system (resolution, bitrate, codec)
- [ ] Resource-aware: respects memory/CPU limits
- [ ] Post-render validation: duration, sync, black-frame, corrupt-file

### Thumbnail Engine
- [ ] N-candidate thumbnail generation
- [ ] Candidates submitted to Decision Engine for ranking (Core-side decision)
- [ ] Storage with experiment_id linkage

### AI Provider Management
- [ ] Provider abstraction layer + router
- [ ] Task class → provider tier mapping
- [ ] Response caching (deterministic requests)
- [ ] Cost ledger: every request logged with tokens, cost, task class, experiment_id
- [ ] Fallback chain with circuit breaker

### Prompt Management
- [ ] Prompt registry with semver versioning
- [ ] Output schema validation per prompt
- [ ] Structured-repair retry on schema violation
- [ ] Prompt evaluation harness (for promotion testing)

### Asset Management
- [ ] Content-addressed storage (SHA256 keys)
- [ ] S3/MinIO backend (unified interface)
- [ ] Retention policies: intermediate TTL, final artifact persistent
- [ ] experiment_id linkage on all assets

## Gate Criteria

```
✓ Dry-run gate: full pipeline executes from directive to all artifacts
   (video file, thumbnail candidates, metadata) without publishing
✓ Fact gate: every script claim traces to a Fact Ledger entry
   (no unsourced claims in any generated script)
✓ Checkpoint gate: kill orchestrator at every stage boundary (9 stages);
   assert artifact-based resume — never restarts from beginning
✓ Fallback gate: kill primary LLM provider mid-pipeline;
   assert fallback provider completes the pipeline
✓ Budget gate: set budget below pipeline cost; assert halt with
   BudgetExceeded event, no silent overspend
✓ Cost gate: every pipeline execution produces a per-experiment
   cost breakdown (tokens, API calls, compute estimate)
✓ Parallel gate: narration and thumbnail run concurrently,
   verified by wall-clock timing (not sequential)
```

---

# v0.4 — First Contact

**Goal:** The first real experiment executes on YouTube in `GATED_STRICT` mode. The owner approves every step. The full loop — directive → pipeline → publish → measure → observe → reflect → learn — completes on real data.

**Duration estimate:** 4–5 weeks

## Deliverables

### YouTube Adapter
- [ ] Platform adapter interface implementation for YouTube
- [ ] OAuth2 authentication with encrypted credential storage and auto-refresh
- [ ] `publish()`: upload video, set metadata, schedule
- [ ] `collect_metrics()`: YouTube Analytics API → canonical metrics mapping
- [ ] Metric windows: 24h, 72h, 7d, 28d collection jobs
- [ ] `rollback()`: unlist/delete capability (DP-014)
- [ ] Native A/B thumbnail support (YouTube experiment thumbnails)
- [ ] Adapter conformance test suite (Vol 3 §24)
- [ ] Health status reporting

### Scheduling Engine
- [ ] Cron + one-shot job persistence
- [ ] Missed-fire detection on startup with catch-up policy
- [ ] Priority classes: EVOLUTION_CYCLE > MEASUREMENT > MAINTENANCE > CLEANUP
- [ ] Measurement jobs: triggered post-publish per MeasurementPlan windows

### Human Approval Framework
- [ ] `GATED_STRICT` mode implementation
- [ ] Approval Inbox dashboard view: full artifact preview + reasoning context
- [ ] Approve / Reject / Request revision actions
- [ ] Rejection recorded as Level-4 feedback → Core learning signal
- [ ] Audit event for every approval decision

### Notification System
- [ ] Email + webhook channels
- [ ] `CRITICAL`, `APPROVAL`, `DIGEST` classes
- [ ] Approval inbox notification on new gated items

### API Gateway
- [ ] Auth (token-based), rate limiting, request logging
- [ ] Versioned API v1 with Core and pipeline endpoints
- [ ] YouTube webhook endpoint with signature verification

### Observation Integration (Real Data)
- [ ] Observation Gateway receiving real YouTube analytics
- [ ] Quarantine logic tested against real edge cases
- [ ] Signal classification on real metric data
- [ ] Full loop: observation → reflection → lesson for first real experiment

### Dashboard Completion
- [ ] Pipeline Monitor: live stage states, timings, cost
- [ ] Approval Inbox with video preview
- [ ] Cost Center: per-experiment cost breakdown
- [ ] Evolution Overview: first real fitness data

## Gate Criteria

```
✓ Publish gate: at least one video successfully published on YouTube
   via the adapter with owner approval
✓ Measurement gate: analytics collected at24h, 72h, 7d windows
   for the first published experiment
✓ Loop gate: the full evolution loop completes —
   observation → reflection → lesson extracted → knowledge record ACTIVE
✓ Rejection gate: owner rejects one experiment;
   rejection appears as Level-4 feedback in Core knowledge
✓ Rollback gate: rollback capability demonstrated (unlist a test video)
✓ OAuth gate: OAuth token expires and auto-refreshes without human action
✓ Real lesson gate: at least one ACTIVE knowledge record derived from
   real (not simulated) experimental evidence
```

---

# v0.5 — Learning Verified

**Goal:** Multiple experiment cycles complete. The system demonstrably learns from real data. Prediction accuracy improves. Calibration is measured. Knowledge consolidates. The owner has evidence that the system is genuinely becoming more intelligent.

**Duration estimate:** 8–12 weeks (milestone is time-gated by real-world experiment cycle duration)

## Deliverables

### Multi-Cycle Operations
- [ ] EvolutionCycleSaga running recurring cycles autonomously
- [ ] Hypothesis backlog growing from real beliefs + real contradictions
- [ ] Strategy lifecycle: first strategy review and revision on real data
- [ ] Memory Engine: first real knowledge consolidations
- [ ] Belief decay: first beliefs transitioning to SUSPENDED for lack of validation

### Calibration System
- [ ] Calibration audit job: stated confidence vs realized frequency (KPI-BEL-002)
- [ ] Calibration history dashboard chart
- [ ] Calibration alert on systematic drift

### Meta-Reflection
- [ ] Meta-reflection trigger at every 20th experiment
- [ ] LearningHealthReport generation and storage
- [ ] Learning Health dashboard panel
- [ ] Recommendations surfaced to owner (Level0only — no autonomous changes yet)

### Prediction Tracking
- [ ] Prediction error trend computation (KPI-EVO-002)
- [ ] Prediction accuracy dashboard chart (rolling window)
- [ ] Alert: prediction error increasing over window

### Goodhart Defense
- [ ] Counter-metric pairs monitoring (GOV-FIT-002)
- [ ] GoodhartAlert generation and routing
- [ ] Alert surfaced in dashboard

### Intelligence Dashboard
- [ ] Intelligence Health panel (separate from Machine Health):
  - Prediction error trend
  - Calibration error trend
  - Knowledge growth rate
  - Learning yield per experiment
  - Belief stability distribution- Exploration ratio

## Gate Criteria

```
✓ Improvement gate: prediction error (KPI-EVO-002) is measurably lower
   in cycles 8–10 than in cycles 1–3(real data, not simulation)
✓ Calibration gate: calibration audit completes without errors;
   confidence estimates within ±20% of realized frequency on real data
✓ Consolidation gate: at least one real knowledge consolidation event;
   merged records archived, consolidated record ACTIVE
✓ Meta-reflection gate: LearningHealthReport generated from real data,
   containing≥ 1 actionable recommendation
✓ Belief evolution gate: at least one belief has a meaningful confidence
   history (≥ 3 updates from evidence, not decay)
✓ Knowledge reuse gate: at least one decision cites a knowledge record
   from a previous cycle (KPI-KNW-003)
```

---

# v1.0 — Supervised Autonomy

**Goal:** Full governance framework operational. System runs in `NOTIFY` mode. Weekly digests generated from real knowledge. All release gates from Volume 5 §22 pass. This is the realization of the Volume 1 vision.

**Duration estimate:** 4–6 weeks of development + 4weeks of supervised operation

## Deliverables

### Governance Framework
- [ ] GovernancePolicy v1.0 with all parameters from Vol 5 §8.1
- [ ] Forbidden Mutation Registry: initial entries + human-edit interface
- [ ] Content policy filter: pre-publication check
- [ ] Blast-radius limits enforced (GOV-SAF-002)
- [ ] Anomaly self-halt: statistical anomaly detection → automatic GATED transition (GOV-SAF-003)
- [ ] Kill switch: single owner action halts all external actions within one scheduler tick (GOV-SAF-001)

### Autonomy Mode Transition
- [ ] `NOTIFY` mode: publish + notify, no gate for VALIDATION + INCREMENTAL class experiments
- [ ] KPI-GOV-001 dashboard: override rate trend visible
- [ ] Autonomy mode change requires audit event + owner confirmation

### Weekly Intelligence Digest
- [ ] Auto-generated from real Core records (not free-form LLM narrative)
  - What the system learned this week (new ACTIVE knowledge records)
  - Predictions made and their outcomes
  - Next experiments planned and why
  - Fitness trend
  - Cost summary
- [ ] Every claim in digest links to a knowledge record
- [ ] Delivered via notification system (email + dashboard)

### Explainability — Five Whys Contract
- [ ] All five answers accessible within 3 dashboard clicks for any published experiment (GOV-XPL-001)
- [ ] Explanation records generated at decision time (GOV-XPL-002)
- [ ] Explanation audit: random weekly sample surfaced in dashboard

### Audit System
- [ ] Immutable audit log separate from event store
- [ ] All governance-significant actions recorded (GOV-AUD-001)
- [ ] Quarterly self-audit report generation scaffold (GOV-AUD-002)

### Self-Evaluation
- [ ] NFR-AUT-003trigger: learning process self-evaluation when health metrics fall below thresholds
- [ ] Level0 parameter recommendations surfaced to owner
- [ ] Shadow-mode scaffold ready for Level 1 meta-mutations (not yet active)

### Final Testing
- [ ] All v1.0 release gate criteria (AC-V5-001through AC-V5-007) verified
- [ ] Monthly chaos drill documented (INF-HA-001)
- [ ] Restore drill completed (INF-BCK-003)
- [ ] Free Tier envelope test: full cycle within resource limits

## Gate Criteria (Full v1.0 Release Gates)

```
✓ AC-V5-001: All Volume 1 acceptance criteria pass (AC-001–013)
✓ AC-V5-002: Simulation gate: ≥ 80% planted-rule discovery,
   calibration within bounds (re-verified with final codebase)
✓ AC-V5-003: Kill switch verified end-to-end in staging:
   activates within one scheduler tick, all external actions halt
✓ AC-V5-004: Restore drill passed within 4h RTO on the release candidate
✓ AC-V5-005: Zero secrets in logs (canary test on release candidate)
✓ AC-V5-006: Five Whys answerable for a real gated experiment
   (demonstrated live to owner)
✓ AC-V5-007: Full Free Tier envelope test passed
✓ NOTIFY mode operating for≥ 4 weeks with no critical incidents
✓ Weekly digest generated and verified for≥ 3 consecutive weeks
```

---

# v1.5 — Earned Autonomy (Outline)

**Trigger:** KPI-GOV-001 (override rate)< 5% sustained for 8 weeks

- `AUTONOMOUS` mode for VALIDATION + INCREMENTAL experiment classes
- Level 1 meta-mutations active (shadow-tested before live)
- Self-optimization loop: parameter tuning within bounds, fully autonomous
- Exploration rate auto-adjustment within governance bounds
- Owner interaction reduced to: digest review, occasional RADICAL experiment approvals, governance config updates

---

# v2.0 — Multi-Platform (Outline)

**Trigger:** v1.0 stable, owner wants second platform

- Second platform adapter (recommended: Blog for fast, cheap feedback loops)
- Cross-platform knowledge transfer with scope discount (GOV-LRN-002)
- Metric normalization verified: same canonical metrics from both platforms
- Zero Core changes required (AC-009verification test)
- Comparative fitness across platforms
- Platform-agnostic strategy planning

---

# v3.0 — Multi-Domain (Outline)

- Non-content execution environments (SEO experiments, ad copy testing, email subject lines)
- Generalized directive schema covering non-media experiments
- Domain-specific fitness profiles
- Knowledge transfer across domains with scope discount

---

# v4.0 — Research Grade (Outline)

- Formal causal inference tooling integrated with the knowledge graph
- Statistical power analysis before experiment approval
- Reproducibility export: full experiment package for external replication
- Benchmarking suite: compareEvolutionOS against known learning baselines
- Open dataset of anonymized knowledge (opted-in deployments)

---

# v5.0 — General Evolution Platform (Outline)

- EvolutionOS as a framework: bring-your-own execution environment
- Ontology-driven configuration: execution environments specified as config, not code
- The Core published as a reusable autonomous learning kernel (library/service)
- Plugin marketplace for adapters and providers
- Multi-instance federated knowledge sharing (opt-in, anonymized)

---
---

# 09_EvolutionOS_Developer_Handbook.md

# DEVELOPER HANDBOOK

**Audience:** Engineers contributing to EvolutionOS
**Purpose:** Everything a new contributor needs to be productive, make correct decisions, and not accidentally break the architecture

---

# 1. Before You Write Any Code

Read in this order:

1. Volume 1 §4–6(Vision, Mission, Philosophy) — 15 minutes
2. Volume 1 §14 (Cognitive Architecture) — 5 minutes
3. ADR-001 through ADR-010 — 30 minutes
4. The Ontology Specification §3–7 (entity definitions) — 45 minutes
5. This handbook — 30 minutes

If you skip these, you will build the wrong thing correctly, which is worse than building the wrong thing incorrectly (at least the latter is obvious).

**The single most important thing to internalize:**

> The Evolution Core knows nothing about content, videos, or platforms. If you find yourself writing `video` or `youtube` inside a Core engine, stop.

---

# 2. Core Development Philosophy

## 2.1 The Three Questions

Before implementing anything, answer these:

**1. Which Capability does this serve?**
(Learn / Reason / Create / Observe / Evolve)

If you cannot answer this, the feature may not belong in EvolutionOS, or you may be building at the wrong layer.

**2. Which Requirement does this implement?**

Every implementation must trace to a requirement ID (FR-*, NFR-*, FR-EC-*, FR-PX-*, INF-*, GOV-*). If no requirement covers what you are building, either the feature is out of scope or the SRS needs an addition — file an issue before building.

**3. Does this cross a bounded context boundary?**

If yes, use an event. Direct calls across context boundaries are not permitted (ADR-009). If you are unsure where a boundary lies, consult Volume 2 §4.1.

## 2.2 The Ratchet Principle

The architecture gets stricter over time, never looser.

Shortcuts that violate:
- Knowledge immutability (ADR-004)
- Core boundary rule (EC-BND-001)
- Explainability requirements (ADR-005)
- Safety constraints (ADR-016)

...are not acceptable at any milestone, even v0.1. These invariants are non-negotiable.

## 2.3 Tests Are First-Class Architecture

The simulation harness (FR-EC-601) is not a test utility — it is the primary intelligence verification mechanism. Degrading the simulation gate to make a milestone pass is equivalent to deleting the product's reason for existing.

---

# 3. Repository Structure

```
evolutionos/
│
├── core/                # Evolution Core (Vol 2) — NO execution concepts
│   ├── perception/
│   │   ├── observation_gateway.py
│   │   └── signal_classifier.py
│   ├── learning/
│   │   ├── knowledge_engine.py
│   │   ├── learning_engine.py
│   │   └── reflection_engine.py
│   ├── reasoning/
│   │   ├── belief_engine.py
│   │   ├── decision_engine.py
│   │   └── strategy_engine.py
│   ├── evolution/
│   │   ├── experiment_engine.py
│   │   ├── hypothesis_engine.py
│   │├── mutation_engine.py
│   │   ├── fitness_engine.py
│   │   └── memory_engine.py
│   ├── saga/
│   │   └── evolution_cycle_saga.py
│   ├── domain/                    # Aggregates, entities, value objects
│   │   ├── experiment.py
│   │   ├── belief.py
│   │   ├── knowledge_record.py
│   │   ├── hypothesis.py
│   │   ├── decision.py
│   │   └── strategy.py
│   ├── events/                    # Domain event definitions
│   │   └── catalog.py
│   └── ports/                     # Interfaces the Core exposes/requires
│       ├── knowledge_repository.py
│       ├── event_bus.py
│       └── directive_issuer.py
│
├── execution/                     # Execution Layer (Vol 3) — platform-aware
│   ├── orchestrator/
│   │   ├── workflow_engine.py
│   │   └── pipeline_stages/
│   │       ├── research.py
│   │       ├── story.py
│   │       ├── script.py
│   │       ├── narration.py
│   │       ├── visual_planning.py
│   │├── composition.py
│   │       ├── thumbnail.py
│   │       └── publishing.py
│   ├── adapters/
│   │   ├── base.py                # PlatformAdapter interface
│   │   └── youtube/
│   │       ├── adapter.py
│   │       └── metric_mapping.py
│   ├── providers/
│   │   ├── llm/
│   │   │   ├── router.py
│   │   │├── openai.py
│   │   │   ├── gemini.py
│   │   │   └── groq.py
│   │   ├── tts/
│   │   ├── search/
│   │   └── media/
│   └── prompts/
│       └── registry/
│
├── infrastructure/                # Vol 4 implementations
│   ├── persistence/
│   │   ├── event_store.py
│   │   ├── projections/
│   │   │   ├── knowledge_graph.py
│   │   │   ├── decision_trace.py
│   │   │   ├── fitness_timeline.py
│   │   │   └── belief_snapshot.py
│   │   └── repositories/
│   ├── messaging/
│   │   ├── broker.py              # MessageBroker interface
│   │   └── redis_streams.py
│   ├── storage/
│   │   └── object_store.py
│   └── scheduler/
│       └── job_engine.py
│
├── governance/                    # Vol 5 implementations
│   ├── policy_engine.py
│   ├── audit_log.py
│   ├── forbidden_registry.py
│   ├── content_policy.py
│   └── kill_switch.py
│
├── dashboard/                     # Web UI
│   ├── api/# FastAPI / equivalent
│   └── ui/                        # React / equivalent
│
├── simulation/                    # Simulation harness (FR-EC-601)
│   ├── world.py                # Synthetic world with planted rules
│   ├── oracle.py                  # Ground truth verification
│   └── runner.py                  # Simulation execution
│
├── tests/
│   ├── unit/
│   ├── integration/
│   ├── contract/                # Adapter conformance tests
│   ├── simulation/                # Intelligence gate tests
│   ├── chaos/                     # Provider kill tests, checkpoint resume
│   └── e2e/                       # Full dry-run pipeline tests
│
├── migrations/                    # Database migrations (numbered)
│
├── config/
│   ├── defaults.yaml              # All configurable parameters with defaults
│   ├── schema.yaml                # Config schema for validation
│   └── environments/
│       ├── local.yaml
│       └── prod.yaml
│
├── docs/                          # The5+4specification volumes
│
├── docker-compose.yml
├── docker-compose.dev.yml
├── Makefile
└── README.md
```

## 3.1 Module Boundary Enforcement

A CI test verifies no Core module imports from `execution/`, `adapters/`, or any platform-specific package:

```python
# tests/architecture/test_core_boundary.py
def test_core_has_no_execution_imports():
    """EC-BND-001: Core must never import execution layer concepts."""
    core_files = glob("core/**/*.py", recursive=True)
    forbidden = ["execution", "youtube", "video", "thumbnail",
                 "render", "publish", "narration", "pipeline"]
    for file in core_files:
        source = open(file).read()
        for term in forbidden:
            assert term not in source.lower(), (
                f"EC-BND-001 violation: '{term}' found in Core file {file}"
            )
```

This test runs on every commit. A failing boundary test blocks merge.

---

# 4. Adding a New Feature — Decision Tree

```text
START│▼
Does an existing requirement cover this?
  ├── YES → proceed to "Which layer?"
  └── NO  → file a requirements issue first; do not build unrequired features

Which layer?
  ├── Core intelligence (learning, reasoning, evolving)
  │└── Goes in core/ with no platform imports
  ├── Content production / publishing
  │     └── Goes in execution/orchestrator/ or execution/adapters/
  ├── Infrastructure / persistence
  │     └── Goes in infrastructure/
  ├── Governance / safety
  │     └── Goes in governance/
  └── UI / API└── Goes in dashboard/

Does it introduce a new entity?
  └── YES → update Ontology Specification first (ONT-001 procedure)

Does it cross a bounded context boundary?
  └── YES → communicate via event on the event bus, never direct call

Does it change an existing API/schema?
  ├── Additive change → proceed with migration
  └── Breaking change → write an ADR first

Write tests FIRST for:├── All aggregate invariants
  ├── State machine transitions (valid and invalid)
  ├── Event emission (correct event for every state change)
  └── Gate criteria for the relevant milestone

IMPLEMENT → verify tests pass → submit PR
```

---

# 5. Writing a Core Engine

Every Core engine follows this structure:

```python
# core/learning/knowledge_engine.py

from core.ports.event_bus import EventBus
from core.ports.knowledge_repository import KnowledgeRepository
from core.domain.knowledge_record import KnowledgeRecord
from core.events.catalog import KnowledgeRecordActivated, KnowledgeRecordDeprecated

class KnowledgeEngine:
    """Capability: Learn
    Requirement: FR-EC-101through FR-EC-104Responsibility: Store, index, retrieve, consolidate KnowledgeRecords.Single responsibility: knowledge persistence and retrieval.
                    Does NOT extract lessons (Learning Engine) or use knowledge
                    for decisions (Decision Engine).
    """

    def __init__(self, repository: KnowledgeRepository, event_bus: EventBus):
        # Depend on interfaces, not implementations (DP-005)
        self._repo = repository
        self._bus = event_bus

    def activate(self, record_id: str) -> None:
        """
        Transition a CANDIDATE record to ACTIVE.
        Requirement: FR-EC-101 (status transitions)
        Emits: KnowledgeRecordActivated
        """
        record = self._repo.get(record_id)
        record.activate()          # aggregate enforces invariants
        self._repo.save(record)    # append-only: saves the new version
        self._bus.publish(
            KnowledgeRecordActivated(
                record_id=record_id,
                confidence=record.confidence,
            )
        )
```

Rules:
- Constructor takes **interfaces only** — never concrete implementations
- Method docstrings reference the requirement they implement
- Every state change emits an event
- No method calls across bounded contexts — publish an event instead
- No platform-specific imports anywhere in `core/`

---

# 6. Writing a Domain Event

```python
# core/events/catalog.py

from dataclasses import dataclass
from datetime import datetime
from uuid import UUID, uuid4

@dataclass(frozen=True)           # Events are immutable value objects
class KnowledgeRecordActivated:
    """
    Produced by: Knowledge Engine
    Consumed by: Belief Engine, Decision Engine
    Schema version: 1.0.0
    Requirement: FR-EC-102(immutability), EC-EVT-002 (envelope)
    """
    record_id: UUID
    confidence: float
    # --- Envelope fields (populated by EventBus before publishing) ---
    event_id: UUID = None
    event_type: str = "KnowledgeRecordActivated"
    schema_version: str = "1.0.0"
    occurred_at: datetime = None
    correlation_id: UUID = None
    causation_id: UUID = None
    producer: str = "knowledge_engine"
```

Rules:
- Events are **frozen dataclasses** — immutable by construction
- Event names are **past tense** (something happened, not a command)
- Schema version is explicit — changing payload fields requires a version bump
- Docstring identifies producer, consumers, and requirement

---

# 7. Writing a Database Migration

```
migrations/
  0001_initial_schemas.sql
  0002_core_events_table.sql
  0003_knowledge_nodes_and_edges.sql
  0004_pgvector_extension.sql
  ...
```

Rules:
- Numbered sequentially — never re-number
- **Forward only** — no destructive down-migrations on `core_events`
- Every migration includes a comment block:

```sql
-- Migration: 0003_knowledge_nodes_and_edges.sql
-- Requirement: FR-EC-101 (KnowledgeRecord schema)
-- ADR: ADR-014 (PostgreSQL as universal store)
-- Breaking change: NO
-- Rollback: Remove tables (safe: no data yet at v0.1)
```

- After writing
```sql
-- After writing a migration, run against a snapshot of production-shaped
-- data in CI to verify it completes cleanly (INF-CI-002).
```

---

# 8. Writing an Aggregate

Aggregates are the write-side of the CQRS model. They enforce invariants and emit events. They never query across boundaries.

```python
# core/domain/experiment.py

from dataclasses import dataclass, field
from typing import List
from uuid import UUID
from core.domain.events import DomainEvent
from core.domain.exceptions import InvalidStateTransition, MutationBudgetExceeded

# Valid state machine transitions (FR-EC-401)
VALID_TRANSITIONS = {
    "DRAFT":{"HYPOTHESIZED"},
    "HYPOTHESIZED": {"APPROVED", "DRAFT"},
    "APPROVED":     {"SCHEDULED"},
    "SCHEDULED":    {"EXECUTING"},
    "EXECUTING":    {"MEASURING", "FAILED"},
    "MEASURING":    {"COMPLETED", "FAILED"},
    "COMPLETED":    {"REFLECTED"},
    "FAILED":       {"REFLECTED"},    # Failed experiments still reflect (DP-012)
    "REFLECTED":    {"ARCHIVED"},
    "ARCHIVED":     set(),            # Terminal — no further transitions
}

@dataclass
class Experiment:
    """
    Aggregate root for the Experiment bounded context.
    Requirement: FR-EC-401, FR-EC-402Invariants enforced:- State machine legality
      - Hypothesis must be attached before APPROVED
      - Mutation budget must not be exceeded (DP-011)
      - ARCHIVED is terminal and permanent
    """
    id: UUID
    state: str = "DRAFT"
    hypothesis_id: UUID = None
    mutations: List = field(default_factory=list)
    mutation_budget: int = 1# default: single mutation (DP-011)
    _events: List[DomainEvent] = field(default_factory=list, repr=False)

    def transition_to(self, new_state: str) -> None:
        """Enforce state machine legality."""
        allowed = VALID_TRANSITIONS.get(self.state, set())
        if new_state not in allowed:
            raise InvalidStateTransition(
                f"Cannot transition Experiment {self.id} "
                f"from {self.state} to {new_state}. "
                f"Allowed: {allowed}"
            )
        self.state = new_state
        self._record(ExperimentStateChanged(
            experiment_id=self.id,
            new_state=new_state
        ))

    def attach_hypothesis(self, hypothesis_id: UUID) -> None:
        if self.state != "DRAFT":
            raise InvalidStateTransition(
                "Hypothesis can only be attached in DRAFT state."
            )
        self.hypothesis_id = hypothesis_id
        self.transition_to("HYPOTHESIZED")

    def approve(self) -> None:
        if self.hypothesis_id is None:
            raise ValueError(
                "FR-EC-401: Experiment cannot be APPROVED without an attached Hypothesis."
            )
        self.transition_to("APPROVED")

    def add_mutation(self, mutation) -> None:
        """FR-EC-421: Enforce mutation budget."""
        if len(self.mutations) >= self.mutation_budget:
            raise MutationBudgetExceeded(
                f"Experiment {self.id} has mutation_budget={self.mutation_budget}. "
                f"Exceeding budget requires explicit justification in DecisionRecord."
            )
        self.mutations.append(mutation)

    def archive(self) -> None:
        """FR-EC-401: ARCHIVED is terminal."""
        if self.state != "REFLECTED":
            raise InvalidStateTransition(
                "Experiment must be REFLECTED before ARCHIVED."
            )
        self.transition_to("ARCHIVED")
        # Cannot be called again — ARCHIVED has no valid outgoing transitions

    def pop_events(self) -> List[DomainEvent]:
        """Drain pending events for the event bus to publish."""
        events = list(self._events)
        self._events.clear()
        return events

    def _record(self, event: DomainEvent) -> None:
        self._events.append(event)
```

Rules:
- Aggregates **never** call repositories or the event bus directly
- They accumulate events via `_record()` — the application service drains and publishes them
- Every invariant violation raises a typed exception, never silently continues
- State transitions are always logged as events

---

# 9. Writing an Application Service

Application services orchestrate: they load aggregates, call methods, save, and publish events. They are the thin layer between the HTTP/event handler and the domain.

```python
# core/learning/services/activate_knowledge_record_service.py

class ActivateKnowledgeRecordService:
    """
    Application service: coordinate activating a KnowledgeRecord.
    This is NOT domain logic — it is orchestration.
    Requirement: FR-EC-101
    """

    def __init__(
        self,
        repository: KnowledgeRepository,
        event_bus: EventBus,
        policy: GovernancePolicy,
    ):
        self._repo = repository
        self._bus = event_bus
        self._policy = policy

    def execute(self, command: ActivateKnowledgeRecordCommand) -> None:
        #1. Load aggregate
        record = self._repo.get(command.record_id)
        if record is None:
            raise RecordNotFound(command.record_id)

        # 2. Check governance policy
        if not self._policy.allows_activation(record):
            raise PolicyViolation(f"Record {command.record_id} blocked by governance policy.")

        # 3. Execute domain logic (aggregate enforces invariants)
        record.activate()  # raises if invalid

        # 4. Persist (optimistic concurrency via version check)
        self._repo.save(record)

        # 5. Publish events (drain from aggregate, publish to bus)
        for event in record.pop_events():
            self._bus.publish(event)
```

---

# 10. Writing a Projection

Projections consume events and build read-optimized views. They must be:
- **Idempotent:** processing the same event twice produces the same state
- **Rebuildable:** drop the projection table and replay from offset0

```python
# infrastructure/persistence/projections/knowledge_graph.py

class KnowledgeGraphProjection:
    """
    Read model: browsable knowledge graph.
    Rebuilt from events — never treated as source of truth.
    Requirement: FR-EC-103, ADR-012Consumes: KnowledgeRecordCreated, KnowledgeRecordActivated,KnowledgeRecordDeprecated, KnowledgeConsolidated
    """

    def __init__(self, db: DatabaseConnection):
        self._db = db

    def handle(self, event: DomainEvent) -> None:
        """Dispatch to per-event handler. Idempotent via ON CONFLICT DO NOTHING."""
        handlers = {
            "KnowledgeRecordCreated":self._on_created,
            "KnowledgeRecordActivated":  self._on_activated,
            "KnowledgeRecordDeprecated": self._on_deprecated,
            "KnowledgeConsolidated":     self._on_consolidated,
        }
        handler = handlers.get(event.event_type)
        if handler:
            handler(event)
        # Unknown events are silently skipped — projections only care
        # about the events they need

    def _on_created(self, event) -> None:
        self._db.execute("""
            INSERT INTO core_read.knowledge_nodes
                (id, statement, scope, confidence, status, created_at)
            VALUES (%s, %s, %s, %s, 'CANDIDATE', %s)
            ON CONFLICT (id) DO NOTHING    -- idempotency
        """, (event.record_id, event.statement,
              event.scope, event.confidence, event.occurred_at))

    def rebuild(self) -> None:
        """
        Drop and rebuild this projection from the event log.
        Called by: weekly rebuild verification job (INF-CI-001),
                   post-migration rebuild.
        """
        self._db.execute("TRUNCATE core_read.knowledge_nodes CASCADE")
        # Infrastructure layer replays all relevant events from offset 0
        # and calls self.handle() for each
```

---

# 11. Writing a Platform Adapter

Every new execution environment implements the same contract (FR-PX-1001).

```python
# execution/adapters/base.py

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List

@dataclass
class CapabilityManifest:
    supports_native_ab: bool
    supports_rollback: bool
    supports_scheduling: bool
    max_title_length: int
    max_description_length: int
    supported_metrics: List[str]  # canonical metric names

class PlatformAdapter(ABC):
    """
    Contract every execution environment must implement.
    Requirement: FR-PX-1001, ADR-003
    Adding a new platform = implement this + metric_mapping.py.
    Zero Core changes required.
    """

    @abstractmethod
    def capabilities(self) -> CapabilityManifest:
        """Declare what this platform supports."""

    @abstractmethod
    def publish(
        self,
        artifact_ref: str,
        metadata: PublicationMetadata,
        schedule: SchedulePolicy,
    ) -> PublicationRef:
        """Publish artifact. Idempotent: retries never create duplicates."""

    @abstractmethod
    def collect_metrics(
        self,
        ref: PublicationRef,
        window: MeasurementWindow,
    ) -> List[RawMetric]:
        """Return platform-native metrics for normalization."""

    @abstractmethod
    def rollback(self, ref: PublicationRef) -> RollbackResult:
        """Unlist or delete the publication. Required for DP-014."""

    @abstractmethod
    def health(self) -> HealthStatus:
        """Return current adapter health (HEALTHY/DEGRADED/FAILED)."""
```

```python
# execution/adapters/youtube/metric_mapping.py

# The entire cross-platform knowledge transfer capability rests on
# this mapping being semantically correct. Review carefully.
YOUTUBE_TO_CANONICAL = {
    "clickThroughRate":"selection_rate",
    "averageViewDuration":           "attention_rate",   # needs normalization
    "averageViewDurationPercentage": "attention_rate",
    "subscribersGained":             "audience_growth",
    "views":                         "reach",
    "comments":                      "engagement_depth",
    "likes":                         "engagement_depth",  # combined with comments
    "returningViewers":              "return_rate",
}

def normalize(metric_name: str, value: float, context: NormalizationContext) -> float:
    """
    Convert platform-native value to canonical unit.
    Example: YouTube averageViewDuration (seconds) →attention_rate (percentage of content length)
    """
    if metric_name == "averageViewDuration" and context.content_duration:
        return (value / context.content_duration) * 100.0
    return value
```

**Adapter conformance test suite** (every adapter must pass):

```python
# tests/contract/test_platform_adapter_conformance.py

class PlatformAdapterConformanceSuite:
    """
    Shared contract tests. Run against every adapter implementation.
    Requirement: FR-PX-1001
    """
    adapter: PlatformAdapter  # set by subclass

    def test_capabilities_returns_manifest(self):
        caps = self.adapter.capabilities()
        assert isinstance(caps, CapabilityManifest)

    def test_publish_is_idempotent(self):
        """Two publishes with the same artifact_ref must not create duplicates."""
        ref1 = self.adapter.publish(self.test_artifact, self.test_metadata, self.test_schedule)
        ref2 = self.adapter.publish(self.test_artifact, self.test_metadata, self.test_schedule)
        assert ref1.publication_id == ref2.publication_id

    def test_collect_metrics_returns_canonical_names(self):
        metrics = self.adapter.collect_metrics(self.test_ref, self.test_window)
        canonical_names = {m.canonical_name for m in metrics}
        for name in canonical_names:
            assert name in CANONICAL_METRIC_REGISTRY, (
                f"Adapter returned unknown canonical metric: {name}. "
                f"Register it in the Metric Registry first."
            )

    def test_health_returns_valid_status(self):
        status = self.adapter.health()
        assert status in (HealthStatus.HEALTHY, HealthStatus.DEGRADED, HealthStatus.FAILED)

    def test_rollback_succeeds_on_published(self):
        ref = self.adapter.publish(self.test_artifact, self.test_metadata, self.test_schedule)
        result = self.adapter.rollback(ref)
        assert result.success is True
```

---

# 12. Writing a Prompt

Prompts are versioned artifacts in the registry, not strings scattered across the codebase.

```python
# execution/prompts/registry/lesson_extraction_v1.py

PROMPT_METADATA = {
    "id": "lesson_extraction",
    "version": "1.0.0",
    "task_class": "REASONING_HEAVY",
    "capability": "Learn",
    "engine": "LearningEngine",
    "requirement": "FR-EC-110",
    "model_compatibility": ["gpt-4o", "gemini-1.5-pro", "claude-3-5-sonnet"],
    "output_schema": "LessonExtractionOutput",  # validated on every response
    "changelog": "Initial version",
}

SYSTEM_PROMPT = """
You are the Learning Engine ofEvolutionOS.

Your role is to extract structured lessons from completed experiments.

A lesson must:
1. Be falsifiable — it makes a claim that could be wrong
2. Reference specific evidence from the experiment
3. State a direction (positive/negative/neutral/contradictory)
4. Include a confidence estimate between 0.01 and 0.99 — never0 or 1

A lesson must NOT:
- Reference platform-specific concepts (no "YouTube", "video", "thumbnail")
  — use canonical terms: "execution environment", "artifact", "selection_rate"
- Make causal claims without controlled-mutation evidence
- Express certainty (confidence = 1.0 is never valid)

Output format: JSON matching LessonExtractionOutput schema.
"""

USER_PROMPT_TEMPLATE = """
Experiment ID: {experiment_id}
Hypothesis: {hypothesis_formal_form}
Prediction: {metric_predictions}
Actual outcome: {actual_outcomes}
Mutation applied: {mutation_description}
Baseline comparison: {baseline_delta}

Extract1–{max_lessons} lessons. Prioritize lessons that:
1. Directly relate to the tested hypothesis
2. Show unexpected results (surprise_score > 0.5)
3. Can be generalized to the scope: {scope}

Return only the JSON object. No explanation outside the schema.
"""
```

Rules:
- Prompts reference canonical terms only (no platform-specific language)
- Output schema is validated on every response — schema violations trigger repair retry
- Version bump required for any change that affects output structure
- New prompt versions are canary-tested before promotion (FR-PX-1402)

---

# 13. Testing Standards

##13.1 Test Categories and What They Cover

| Category | Location | What It Tests | Required For |
|---|---|---|---|
| Unit | `tests/unit/` | Aggregate invariants, domain logic, pure functions | Every PR |
| Integration | `tests/integration/` | Engine + real DB + real event bus | Every PR |
| Contract | `tests/contract/` | Adapter conformance suite | Every adapter implementation |
| Architecture | `tests/architecture/` | Boundary rules, dependency direction | Every PR |
| Simulation | `tests/simulation/` | Intelligence gate (FR-EC-601) | Every milestone gate |
| Chaos | `tests/chaos/` | Provider kills, checkpoint resume, host restart | Monthly + release |
| E2E | `tests/e2e/` | Full dry-run pipeline | Every release |

## 13.2 The Simulation Test (Most Important)

```python
# tests/simulation/test_intelligence_gate.py

def test_core_discovers_planted_rules():
    """
    FR-EC-601: Intelligence Gate.
    The Core must discover planted rules with acceptable confidence
    within a bounded number of simulated cycles.

    This test is the primary verification that the system
    actually learns, not merely processes.
    """
    world = SimulationWorld(seed=42, rules=PLANTED_RULES)
    core = build_core_with_simulation_adapter(world)
    runner = SimulationRunner(core, world)

    report = runner.run(max_cycles=50)

    # Gate:≥ 80% of planted rules discovered (AC-V5-002)
    discovery_rate = report.rules_discovered / len(PLANTED_RULES)
    assert discovery_rate >= 0.80, (
        f"Intelligence gate FAILED: discovered {report.rules_discovered}/"
        f"{len(PLANTED_RULES)} rules ({discovery_rate:.0%}). "
        f"Undiscovered: {report.undiscovered_rule_ids}"
    )

    # Gate: calibration within±15% of realized frequency
    assert report.calibration_error <= 0.15, (
        f"Calibration gate FAILED: error={report.calibration_error:.2f}. "
        f"Stated confidence is not tracking realized frequency."
    )

    # Gate: no knowledge records were modified after creation (ADR-004)
    assert report.immutability_violations == 0, (
        "Immutability gate FAILED: knowledge records were modified post-creation."
    )

PLANTED_RULES = [
    PlantedRule(
        id="PR-001",
        scope=Scope(niche="test_niche_a"),
        condition={"hook_type": "question"},
        effect={"metric": "selection_rate", "direction": "increase",
                "magnitude": Range(0.12, 0.18)},
        noise_stddev=0.03,
    ),
    PlantedRule(
        id="PR-002",
        scope=Scope(niche="test_niche_a"),
        condition={"length_minutes": ">15"},
        effect={"metric": "attention_rate", "direction": "decrease",
                "magnitude": Range(0.20, 0.30)},
        noise_stddev=0.04,
    ),
    # ... 8–12 rules total, varied in scope, direction, magnitude
]
```

## 13.3 Chaos Tests

```python
# tests/chaos/test_checkpoint_resume.py

@pytest.mark.parametrize("kill_at_stage", [
    "RESEARCHING", "STORY_DRAFTED", "SCRIPTED",
    "NARRATED", "VISUALS_PLANNED", "COMPOSING",
    "THUMBNAIL_READY", "PUBLISHING", "MEASURING",
])
def test_pipeline_resumes_from_checkpoint_after_kill(kill_at_stage, tmp_path):
    """
    FR-PX-102, NFR-AVA-002: Crash at any stage → resume from checkpoint,
    never restart from beginning.
    """
    orchestrator = build_test_orchestrator(checkpoint_dir=tmp_path)
    directive = make_test_directive()

    # Run until the kill stage
    with pytest.raises(SimulatedCrash):
        orchestrator.execute(directive, crash_at=kill_at_stage)

    # Verify checkpoint was written BEFORE the crash
    checkpoint = load_checkpoint(tmp_path, directive.experiment_id)
    assert checkpoint.last_completed_stage != "RECEIVED", (
        f"No checkpoint was written before stage {kill_at_stage}"
    )

    # Resume and complete
    result = orchestrator.resume(directive.experiment_id)
    assert result.completed_from_stage == kill_at_stage
    assert result.restarted_from_beginning is False
    assert result.status == "THUMBNAIL_READY"  # or further
```

---

# 14. The Pull Request Checklist

Every PR must address each item before requesting review:

```markdown
## PR Checklist

### Architecture
- [ ] Which Capability does this serve? (Learn/Reason/Create/Observe/Evolve)
- [ ] Which Requirement ID(s) does this implement? (list them)
- [ ] No Core module imports execution-layer concepts (boundary test passes)
- [ ] Cross-context communication uses events, not direct calls
- [ ] If a new entity was introduced: Ontology Specification updated first
- [ ] If an existing API/schema was changed in a breaking way: ADR filed

### Implementation
- [ ] Aggregate invariants enforced with typed exceptions
- [ ] Every state transition emits a domain event
- [ ] Application service drains and publishes aggregate events
- [ ] Projection handlers are idempotent (ON CONFLICT DO NOTHING or equivalent)
- [ ] No secrets in code (env/config only)
- [ ] All configurable values externalized to config (not hardcoded)

### Data
- [ ] New migration is numbered sequentially
- [ ] Migration comment block includes requirement, ADR, breaking-change flag
- [ ] `core_events` table: no UPDATE/DELETE operations added anywhere

### Tests
- [ ] Unit tests for all new aggregate invariants
- [ ] Unit tests for state machine transitions (valid AND invalid)
- [ ] Integration test covering the happy path end-to-end
- [ ] If new adapter: conformance suite passes
- [ ] Architecture boundary test still passes
- [ ] No test uses `time.sleep()` — use fake clocks / event-driven synchronization

### Documentation
- [ ] Public interfaces have docstrings with requirement references
- [ ] CHANGELOG entry added
- [ ] If behavior change: relevant dashboard view updated or issue filed
```

---

# 15. Common Mistakes and How to Avoid Them

## 15.1 Calling Across Bounded Contexts Directly

**Wrong:**
```python
# Inside LearningEngine — VIOLATION of ADR-009
class LearningEngine:
    def extract_lesson(self, reflection):
        lesson = self._generate_lesson(reflection)
        #❌ Direct call across bounded context
        self._belief_engine.update_beliefs_from_lesson(lesson)
```

**Correct:**
```python
class LearningEngine:
    def extract_lesson(self, reflection):
        lesson = self._generate_lesson(reflection)
        # ✓ Publish event; BeliefEngine subscribes independently
        self._event_bus.publish(LessonExtracted(lesson_id=lesson.id))
```

## 15.2 Platform Concepts in the Core

**Wrong:**
```python
# Inside DecisionEngine — VIOLATION of EC-BND-001
class DecisionEngine:
    def select_strategy(self, context):
        # ❌ Platform-specific concept in Core
        if context.platform == "youtube":
            return self._youtube_strategy()
```

**Correct:**
```python
class DecisionEngine:
    def select_strategy(self, context):
        # ✓ Core reasons over abstract scope, never platform names
        relevant_rules = self._knowledge.query_by_scope(context.scope)
        candidates = self._generate_candidates(relevant_rules)
        return self._rank_and_select(candidates)
```

## 15.3 Mutating Knowledge Records

**Wrong:**
```python
# VIOLATION of ADR-004
def update_confidence(record_id, new_confidence):
    record = repo.get(record_id)
    record.confidence = new_confidence  # ❌ Mutating existing record
    repo.save(record)
```

**Correct:**
```python
def update_confidence(record_id, new_confidence, evidence_refs):
    old_record = repo.get(record_id)
    # ✓ Create new version; old record is superseded, not modified
    new_record = KnowledgeRecord(
        statement=old_record.statement,
        confidence=new_confidence,
        evidence_refs=old_record.evidence_refs + evidence_refs,
        supersedes_id=old_record.id,
        status="CANDIDATE",  # requires re-activation
    )
    old_record.supersede(new_record.id)  # marks old as DEPRECATED
    repo.save(new_record)
    repo.save(old_record)# saves the deprecation event, not the data
```

## 15.4 Confidence as a Manual Value

**Wrong:**
```python
# VIOLATION of ADR-007
belief = Belief(
    statement="Question hooks improve CTR",
    confidence=0.85,  # ❌ Where did0.85 come from? No evidence chain.
)
```

**Correct:**
```python
# ✓ Confidence is always computed from evidence
belief = belief_engine.derive_from_knowledge(
    knowledge_refs=[rule_id_1, rule_id_2, observation_id_3],
    # Confidence computed by update function (FR-EC-202)
)
```

## 15.5 Silent Failures

**Wrong:**
```python
def process_observation(obs):
    try:
        self._integrate(obs)
    except Exception:
        pass  # ❌ Silent failure — knowledge is lost; no alert
```

**Correct:**
```python
def process_observation(obs):
    try:
        self._integrate(obs)
    except ValidationError as e:
        # ✓ Quarantine with explanation; emit event; never silently drop
        self._quarantine(obs, reason=str(e))
        self._event_bus.publish(ObservationQuarantined(
            observation_id=obs.id, reason=str(e)
        ))
    except Exception as e:
        # ✓ Critical failure: log, alert, re-raise
        self._logger.critical("observation_integration_failed",
                              observation_id=obs.id, error=str(e))
        raise
```

---

# 16. Local Development Workflow

## 16.1 Initial Setup

```bash
# 1. Clone and bootstrap
git clone https://github.com/your-org/evolutionos.git
cd evolutionos
make bootstrap          # installs deps, starts containers, runs migrations

# 2. Verify everything is healthy
make health# checks all containers + DB + event bus

# 3. Run the test suite
make test               # unit + integration + architecture boundary tests

# 4. Run the simulation gate
make simulation-gate    # intelligence gate — should pass on main branch
```

## 16.2 Day-to-Day

```bash
# Start development environment
make dev

# Watch mode: tests re-run on file save
make test-watch

# Run specific test category
make test-unit
make test-integration
make test-simulation
make test-chaos         # slow — run before PR, not on every save

# Rebuild a specific projection (useful when changing projection logic)
make rebuild-projection PROJECTION=knowledge_graph

# Tail logs with correlation ID filtering
make logs CORRELATION_ID=abc-123-...

# Check module boundaries (fast — run after any new import)
make check-boundaries

# Simulate N cycles against the synthetic world
make simulate CYCLES=20SEED=42

# Full pipeline dry-run
make dry-run DIRECTIVE=examples/test_directive.yaml
```

## 16.3 Adding a New Engine

```bash
# Scaffold a new engine from template
make new-engine CAPABILITY=learn NAME=consolidation_engine

# This creates:
# core/learning/consolidation_engine.py  (engine stub)
# tests/unit/test_consolidation_engine.py (test stub)
# And adds the engine to the capability manifest
```

---

# 17. Operational Runbooks

## 17.1 Responding to a Falling Prediction Accuracy (KPI-EVO-002Alert)

```
ALERT: prediction_error_trend INCREASING over 7-day window

Step 1: Open Intelligence Health dashboard→ Check: is this specific to one niche/scope or global?

Step 2: If scope-specific:
        → Check: did that scope's environment change? (algorithm update?audience shift? new competitors?)
        → If yes: issue a FORCED_EXPLORE decision for that scope to
          generate validation experiments
        → If no: check recent belief revisions for that scope

Step 3: If global:
        → Check: was there a recent code deployment?
        → If yes: review deployment diff for LearningEngine / ReflectionEngine
          changes; consider rollback
        → If no: trigger meta-reflection manually:
          make trigger-meta-reflection REASON="manual_global_accuracy_decline"

Step 4: Review LearningHealthReport (auto-generated by meta-reflection)
        → Implement Level-0 recommendations immediately
        → For Level-1+ recommendations: review and approve via governance panel

Step 5: Document incident in quarterly self-audit log
```

## 17.2 Responding to a GoodhartAlert

```
ALERT: GoodhartAlert raisedOptimized metric: selection_rate
       Counter-metric: attention_rate
       Divergence score: 0.34(threshold: 0.25)

Interpretation: CTR is rising but average view duration is falling.
This is the clickbait signal.

Step 1: Open Decision Explorer, filter decisions from past 14 days
        → Identify decisions that maximized selection_rate
        → Review: are title candidates trending toward sensationalism?

Step 2: Open Knowledge Browser, filter by metric=selection_rate, status=ACTIVE
        → Review recent ACTIVE rules for selection_rate
        → Look for rules that have high confidence but low attention_rate support

Step 3: Immediate options:
        a. Adjust weight profile: reduce selection_rate weight,
           increase attention_rate weight(GovernancePolicy change → AuditEvent → takes effect next cycle)
        b. Add a forbidden mutation pattern to the registry:
           "title_pattern: superlative_clickbait" → blocked pre-directive
        c. Both

Step 4: Issue a VALIDATION-class experiment to explicitly test
        whether high-CTR titles from recent period maintained attention_rate
        → This generates direct contradictory evidence against the
          selection_rate rules that caused the drift

Step 5: Monitor: divergence score should decrease over next 3 cycles
```

## 17.3 Activating the Kill Switch

```
SITUATION: Unexpected behavior requires immediate halt of all publishing

Step 1: Dashboard → System Controls → Kill Switch → Activate
        (requires OWNER role credentials)
        OR:
        make kill-switch REASON="unexpected_behavior_description"

        Effect: All external actions halt within one scheduler tick (~60s)
                Learning and reflection on already-collected data may continue
                All pending directives transition to PAUSED state

Step 2: System enters GATED_STRICT mode automatically
        No new publications until explicitly re-enabled

Step 3: Review: open Experiment Board → filter PAUSED experiments
        For each: Approve (resumes), Reject (archives), or Hold

Step 4: Investigate root cause before re-enabling
        All kill-switch activations logged in immutable audit log

Step 5: Re-enable when satisfied:
        Dashboard → System Controls → Resume OperationsRequires explicit autonomy mode selection on resume
```

## 17.4 Monthly Chaos Drill

```bash
# Run the monthly chaos drill (document results in ops log)
make chaos-drill

# This executes:
# 1. Full host reboot simulation (containers restart,
```bash
# This executes:
# 1. Full host reboot simulation (containers restart,
#    verify all services healthy within 5 minutes)
# 2. Checkpoint resume test (kill orchestrator at random stage,
#    verify resume without restart)
# 3. Provider kill test (disable primary LLM provider,
#    verify fallback completes a pipeline)
# 4. Projection rebuild verification (drop + rebuild all projections,
#    verify checksums match pre-drop state)
# 5. Restore drill (restore from latest backup into scratch env,
#    verify knowledge integrity checksums)
# 6. Secret canary test (verify no secrets appear in any log sink)

# Results are written to: ops/chaos-drills/YYYY-MM-DD.md
# Any failure is a CRITICAL incident requiring resolution before next cycle
```

## 17.5 Restore from Backup

```bash
# Full restore procedure (RTO target:≤ 4 hours)

# Step 1: Provision fresh host
make provision-host ENV=prod HOST=<new-host-ip>

# Step 2: Restore event store from backup
make restore-backup \
  BACKUP_DATE=2026-07-15\
  TARGET_HOST=<new-host-ip>
# This restores: core_events (full), WAL up to RPO window
# This does NOT restore: projections (they rebuild from events)

# Step 3: Verify event store integrity
make verify-event-store TARGET_HOST=<new-host-ip>
# Checks: sequence continuity, no gaps, checksums match backup manifest

# Step 4: Rebuild all projections
make rebuild-all-projections TARGET_HOST=<new-host-ip>
# Replays full event log into all projection tables
# Duration: proportional to event log size; estimate 20min per100k events

# Step 5: Verify projection checksums
make verify-projections TARGET_HOST=<new-host-ip>
# Compares projection checksums against pre-backup reference values

# Step 6: Start all services
make start TARGET_HOST=<new-host-ip>

# Step 7: Smoke test
make smoke-test TARGET_HOST=<new-host-ip>
# Verifies: dashboard loads, knowledge browser returns data,
# experiment board shows correct states, scheduler health green

# Step 8: Knowledge integrity audit
make knowledge-integrity-audit TARGET_HOST=<new-host-ip>
# Verifies: no orphan edges, confidence bounds valid,
# all status transitions legal per state machines
# Any violations: see runbook 17.6

# Step 9: Resume operations (stays in GATED mode until owner confirms)
# Dashboard → System Controls → Confirm Restore → Resume
```

## 17.6 Knowledge Integrity Violations

```
ALERT: KnowledgeIntegrityViolation detected
       Type: ORPHAN_EDGE | CONFIDENCE_BOUND | ILLEGAL_STATUS_TRANSITION

These are detected by: nightly integrity job (INF-KG-003),post-restore audit (17.5Step 8)

ORPHAN_EDGE (edge references a non-existent node):
  Investigation:
    SELECT * FROM knowledge.edges WHERE to_id NOT IN
    (SELECT id FROM knowledge.nodes);
  Resolution:
    These edges are quarantined (status='ORPHANED'), not deleted.
    File a defect: edges should never become orphaned.
    Root cause: likely a projection rebuild race condition ora missing event handler.

CONFIDENCE_BOUND (confidence outside0.01–0.99):
  This should never happen if aggregate invariants are enforced.
  Investigation: identify which engine created the record.
  Resolution: correct confidence via new superseding record.
  File a defect: the aggregate that allowed this has a bug.

ILLEGAL_STATUS_TRANSITION (e.g., ARCHIVED → ACTIVE):
  This is a serious integrity violation.
  Investigation: query event log for the record's stream:
    SELECT * FROM core_events
    WHERE stream_id = '<record_id>'ORDER BY version;Identify which event caused the illegal transition.
  Resolution: the projection must be corrected by replaying
  the event log with the bug fixed. Never manually edit
  knowledge records (ADR-004).
```

---

# 18. Configuration Reference

All configurable parameters with their defaults, requirement references, and guidance:

```yaml
# config/defaults.yaml

evolution:
  # Minimum exploration rate (FR-EC-212)
  # Below this: system never explores; gets trapped (RSK-004)
  min_exploration_rate: 0.10

  # Maximum exploration rate (FR-EC-212)
  # Above this: system never exploits; wastes resources
  max_exploration_rate: 0.40

  # Default exploration rate (auto-adjusts within min/max)
  default_exploration_rate: 0.15

  # Cycles between meta-reflection (FR-EC-122)
  meta_reflection_interval: 20

  # Max concurrent RADICAL class experiments (GOV-EXP-002)
  # Default0: RADICAL always requires human approval
  radical_experiment_budget: 0

  # Mutation budget per experiment (FR-EC-421)
  default_mutation_budget: 1

knowledge:
  # Minimum supporting experiments before CANDIDATE → ACTIVE (FR-EC-111)
  min_evidence_count: 3

  # Semantic similarity threshold for consolidation (FR-EC-104)
  consolidation_similarity_threshold: 0.85

  # Days without validation before confidence decay begins (FR-EC-203)
  decay_window_days: 90

  # Confidence below which record transitions to DEPRECATED (FR-EC-112)
  deprecation_threshold: 0.35

  # Confidence floor (CON-ETH-003— never claim certainty)
  confidence_floor: 0.01confidence_ceiling: 0.99

belief:
  # Learning rate for confidence updates (FR-EC-202)
  # Higher = faster adaptation but less stable
  learning_rate: 0.15

  # Strength of regularization toward0.5 for unvalidated beliefs
  prior_pull: 0.05

  # Calibration audit interval in days (GOV-BEL-001)
  calibration_audit_interval_days: 14

  # Maximum calibration error before alert (KPI-BEL-002)
  calibration_error_threshold: 0.20

fitness:
  # Default weight profile (FR-EC-431)
  # Modifying weights requires a GovernancePolicy version change
  weights:
    learning_yield: 0.35# Highest: we optimize for learning (ADR-010)
    prediction_accuracy: 0.25
    performance_delta: 0.20
    strategic_alignment: 0.15
    cost_efficiency: 0.05

  # Goodhart divergence threshold (GOV-FIT-002)
  goodhart_alert_threshold: 0.25

governance:
  # Default approval mode for new experiments (ADR-017)
  default_approval_mode: GATED

  # Max publications per day (GOV-SAF-002)
  max_publications_per_day: 3

  # Cost ceiling per experiment (GOV-SAF-002)
  max_cost_per_experiment_usd: 2.00

  # Monthly budget ceiling (INF-CST-002)
  monthly_budget_ceiling_usd: 50.00

providers:
  # Task class → provider tier mapping (FR-PX-1302)
  routing:REASONING_HEAVY:[gpt-4o, gemini-1.5-pro, claude-3-5-sonnet]
    GENERATION_BULK:   [gpt-4o-mini, gemini-1.5-flash, groq-llama3]
    CLASSIFICATION_CHEAP: [gpt-4o-mini, groq-llama3]

  # LLM response cache TTL in seconds (FR-PX-1303)
  cache_ttl_seconds: 604800  # 7 days

  # Circuit breaker: failures before provider marked FAILED
  circuit_breaker_threshold: 5

  # Circuit breaker: seconds before retry (NFR-REL-002)
  circuit_breaker_reset_seconds: 300

scheduler:
  # Evolution cycle interval (FR-EC-501)
  evolution_cycle_cron: "0 6 * * *"  # Daily at 06:00 UTC

  # Measurement job offsets post-publish (FR-PX-901)
  measurement_windows:
    - offset_hours: 24- offset_hours: 72
    - offset_hours: 168# 7 days
    - offset_hours: 672   # 28 days

  # Memory consolidation schedule (FR-EC-440)
  consolidation_cron: "0 3 * * *"  # Daily at 03:00 UTC

  # Calibration audit schedule (GOV-BEL-001)
  calibration_audit_cron: "0 4 * * 1"  # Weekly Monday04:00 UTC

storage:
  # Intermediate artifact TTL in days (INF-OBJ-002)
  intermediate_ttl_days: 14

  # Storage alert threshold (INF-OBJ-003)
  storage_alert_percent: 80

  # S3-compatible endpoint (empty = use AWS S3)
  object_store_endpoint: ""# set to http://minio:9000 for local dev

simulation:
  # Planted-rule discovery threshold for intelligence gate (FR-EC-601)
  min_discovery_rate: 0.80

  # Max cycles for intelligence gate (FR-EC-601)
  max_simulation_cycles: 50

  # Acceptable calibration error in simulation (AC-V5-002)
  max_calibration_error: 0.15

  # Noise level for synthetic observations
  default_noise_stddev: 0.03
```

---

# 19. Glossary of Engineering Terms

For terms specific to the domain, see Ontology Specification §10. This section covers engineering/implementation terminology:

| Term | Meaning in this codebase |
|---|---|
| Aggregate | A cluster of domain objects treated as a single unit for data changes. Enforces invariants. Emits events. Lives in `core/domain/`. |
| Application Service | Thin orchestration layer: loads aggregates, calls domain methods, persists, publishes events. Not domain logic. |
| Bounded Context | A module boundary with exclusive data ownership. Cross-context access via events only. |
| Command | An intent to change state. Validated by an aggregate. Distinct from an event (which records what happened). |
| CQRS | Command Query Responsibility Segregation. Write model (aggregates) and read models (projections) are separate. |
| Dead Letter | An event or message that failed processing and was moved to a dead-letter stream for investigation. |
| Event Sourcing | Persisting state as a sequence of events, not as current values. Current state = replay of events. |
| Idempotent | An operation that produces the same result regardless of how many times it is applied. Required for all projection handlers and publish operations. |
| Optimistic Concurrency | Allowing concurrent writes but detecting conflicts at save time via a version number. No locking. |
| Port | An interface declared by the Core describing what it needs from the outside world (e.g., `KnowledgeRepository`). Implemented by infrastructure adapters. |
| Projection | A read-only view built from the event stream. Disposable and rebuildable. |
| Saga | A long-running process manager coordinating work across multiple aggregates and bounded contexts using events. |
| Snapshot | A point-in-time capture of aggregate state to avoid replaying the full event history on every load. |
| Upcaster | A function that transforms an event of schema version N into version N+1. Enables schema evolution without rewriting historical events. |
| Value Object | An immutable object defined by its attributes, not its identity. Events are value objects. |

---

# 20. Contributing Guidelines

## 20.1 Issue First, Code Second

For anything beyond a typo fix, open an issue before writing code:

- **Bug:** description, reproduction steps, affected requirement ID
- **Feature:** which requirement it addresses (or a requirements addition proposal)
- **Architecture change:** always requires an ADR proposal in the issue before any code

## 20.2 Branch Naming

```
feat/FR-EC-123-lesson-extraction-pipeline
fix/FR-PX-203-fact-ledger-null-source
adr/ADR-021-vector-database-evaluation
refactor/knowledge-engine-interface-cleanup
```

## 20.3 Commit Messages

```
feat(FR-EC-110): implement lesson extraction pipeline

Implements FR-EC-110: statistical guardrails for lesson promotion.
Lessons require min_evidence_count=3 before ACTIVE transition.

Closes #142
```

Format: `type(requirement-id): short description`

Types: `feat`, `fix`, `test`, `refactor`, `docs`, `infra`, `adr`

## 20.4 Review Standards

Every PR requires at least one reviewer to verify:

1. **Architecture boundary test passes** — Core contains no execution concepts
2. **Requirement traceability** — every new function references a requirement
3. **Event discipline** — cross-context communication uses events
4. **Immutability** — no knowledge records mutated
5. **Tests cover gates** — new behavior has tests that would catch regression

## 20.5 What Maintainers Will Reject

- Code that violates EC-BND-001 (platform concepts in Core)
- Code that mutates knowledge records (ADR-004)
- Features without requirement traceability
- New entities not in the Ontology Specification
- Breaking API changes without an ADR
- Tests using `time.sleep()` (flaky by design)
- Silent exception swallowing
- Hardcoded secrets or API keys
- Confidence values assigned manually without evidence (ADR-007)

---

# 21. Performance Tuning Guide

## 21.1 Knowledge Query Optimization

The most common performance bottleneck is knowledge retrieval during decision-making (NFR-PERF-002).

**Profile first:**
```bash
make profile-decision-engine CYCLES=10
# Outputs: flame graph + per-query timing breakdown
```

**Common causes of slow knowledge queries:**

| Symptom | Likely Cause | Fix |
|---|---|---|
| Slow `query_by_scope()` | Missing GIN index on `scope` JSONB | `CREATE INDEX CONCURRENTLY idx_knowledge_scope ON knowledge.knowledge_nodes USING GIN (scope)` |
| Slow `query_related()` | Graph depth too high | Reduce default depth from 4 to 3; or add materialized path caching |
| Slow semantic search | HNSW index not built or stale | `SELECT * FROM pg_indexes WHERE indexname LIKE '%embedding%'`; rebuild if needed |
| Belief snapshot miss | Cache invalidation too aggressive | Tune `BeliefRevised` event handling to only invalidate affected beliefs, not all |

**Decision Engine hot path** (runs on every strategic decision):

```python
# This sequence must complete within NFR-PERF-001threshold
# Profile this path specifically if latency alerts fire

# 1. Belief snapshot (Redis cache — should be sub-millisecond)
beliefs = belief_snapshot_cache.get_for_scope(context.scope)

# 2. Knowledge retrieval (indexed query — should be < 50ms)
knowledge = knowledge_repo.query_for_decision(context, min_confidence=0.40)

# 3. Candidate generation (LLM call — typically500ms–2s)
# This is the dominant latency contributor; optimize routing to fast models
# for GENERATION_BULK tasks that don't need heavyweight reasoning

# 4. Scoring (CPU-bound, in-process — should be < 10ms)
scored = self._score_candidates(candidates, knowledge, beliefs)
```

## 21.2 Event Processing Backpressure

If the event consumer lag grows (visible in the System Health dashboard):

```bash
# Check consumer group lag
make check-consumer-lag

# If a specific consumer is far behind:
# 1. Check for errors in its dead-letter stream
make check-dlq CONSUMER=knowledge_engine

# 2. If DLQ has messages: inspect and replay or discard
make inspect-dlq CONSUMER=knowledge_engine LIMIT=10
make replay-dlq CONSUMER=knowledge_engine  # after fixing the bug
make discard-dlq CONSUMER=knowledge_engine  # only if messages are truly unprocessable

# 3. If consumer is slow but healthy: check its processing time histogram
# Dashboard → System Health → Consumer Metrics → knowledge_engine
```

## 21.3 Free Tier Memory Management

On the Free Tier EC2 instance, memory is the primary constraint.

```bash
# Check current memory allocation per container
make memory-report

# If total approaches 90% of available:
# 1. Reduce LLM response cache TTL in config (fastest win)
# 2. Reduce projection cache sizes
# 3. Schedule heavy operations (consolidation, rebuild) to off-peak

# Swap should never be used for Core engine operations
# Configure swappiness low: sudo sysctl vm.swappiness=10
```

---

# 22. Security Checklist for Contributors

Before any PR touching authentication, credentials, or external APIs:

```markdown
## Security Review (required for auth/credential/API PRs)

- [ ] No credentials, tokens, or API keys in source code
- [ ] No credentials in test fixtures (use fake/mock values)
- [ ] New external API calls go through the provider abstraction layer
- [ ] OAuth flows use PKCE where applicable
- [ ] Token storage: encrypted at rest, never logged
- [ ] New webhook endpoints validate signatures before processing payload
- [ ] New user-facing inputs are validated before processing(type checking, length limits, format validation)
- [ ] New database queries use parameterized statements(no string concatenation in SQL)
- [ ] New log statements do not include sensitive values(test with secret canary: make test-secret-canary)
- [ ] Outbound requests: only to allowlisted domains
  (update allowlist in config if new domain needed — requires review)
- [ ] New dependencies: check for known CVEs before adding(make check-deps NEW_DEP=package-name)
- [ ] Dependencies pinned to exact versions, not ranges
```

---

# 23. Intelligence Debugging Guide

When the system is not learning as expected — a capability unique to EvolutionOS that has no equivalent in conventional software debugging.

## 23.1 Diagnosing Poor Prediction Accuracy

```
SYMPTOM: KPI-EVO-002 (prediction error) not improving after10+ cycles

INVESTIGATION TREE:

1. Are experiments completing with reflections?
   → Dashboard → Experiment Board → filter REFLECTED
   → If few: check pipeline failure rate; the problem is operational, not intelligence

2. Are lessons being extracted from reflections?
   → Dashboard → Knowledge Browser → filter by provenance=REFLECTION, last14 days
   → If few lessons: check LearningEngine logs for statistical guardrail rejections
   → Cause: not enough supporting evidence (min_evidence_count not reached)
   → Fix: reduce min_evidence_count temporarily to 2, or run more validation experiments

3. Are extracted lessons reaching ACTIVE status?
   → Filter Knowledge Browser: status=CANDIDATE, type=LESSON
   → If many stuck in CANDIDATE: they haven't accumulated enough evidence
   → Fix: generate VALIDATION-class experiments targeting the same hypothesis

4. Are ACTIVE lessons being used in decisions?
   → Dashboard → Decision Explorer → check knowledge_used refs
   → If decisions cite no recent knowledge: check query_for_decision()
     relevance scoring; may be filtering out relevant records by scope mismatch
   → Fix: review scope specificity on recent knowledge records

5. Are decisions' predictions calibrated?
   → Dashboard → Intelligence Health → Calibration Error chart
   → If calibration_error > 0.20: the confidence model is miscalibrated
   → Fix: review learning_rate and prior_pull in config; run calibration audit→ make trigger-calibration-audit

6. Is there systematic surprise (surprise_score consistently high)?
   → High surprise means predictions are consistently wrong
   → Good news: this is information
   → Review high-surprise reflections: Dashboard → Experiment Board →
     sort by surprise_score desc
   → Pattern in surprises? (always wrong in one scope? one metric?)
   → That pattern is the hypothesis backlog: generate experiments to explain it
```

## 23.2 Diagnosing Strategy Drift

```
SYMPTOM: System is producing experiments that don't seem related to the objective

INVESTIGATION:
1. Open Dashboard → Decision Explorer → Strategy decisions (last 30 days)
2. Trace: Strategy → Hypothesis Backlog → Individual Hypothesis → Decision
3. Check each strategy's objective vs its current experiment hypothesis backlog
4. If backlog diverged from objective: checkStrategyRevised events
   → Was there a belief revision that triggered strategy revision?
   → Was the revision justified? (check evidence chain)
5. If strategy was revised without clear evidence chain: this is GOV-STR-001 violation
   → File a defect: strategy revision must have traceable cause
```

## 23.3 Diagnosing Knowledge Accumulation Stagnation

```
SYMPTOM: KPI-KNW-001 (knowledge growth rate) flatlined

INVESTIGATION:
1. Check experiment completion rate (are experiments finishing?)
2. Check reflection completion rate (are reflections happening?)
3. Check lesson extraction rate (are lessons being generated?)
4. Check lesson activation rate (are lessons reaching ACTIVE?)

Each step can independently stall. Identify which step breaks the chain.

Common causes:
- Step 1 stall: pipeline operational issues (check orchestrator logs)
- Step 2 stall: ReflectionEngine errors (check engine health, DLQ)
- Step 3 stall: statistical guardrails rejecting all lessons→ Experiments may be too noisy (increase controlled mutation)
  → Measurement windows too short (increase to capture full effect)
- Step 4 stall: not enough experiments supporting each lesson
  → Run more VALIDATION experiments for top CANDIDATE lessons

Nuclear option: run simulation gate again against current codebase
  make simulation-gateIf it fails: there is a regression in the learning enginesBisect recent commits to find it
```

---

# 24. Release Checklist

Before cutting any release tag:

```markdown
## Release Checklist:EvolutionOS vX.Y.Z

### Intelligence Gates
- [ ] Simulation gate passes:≥ 80% planted-rule discovery (make simulation-gate)
- [ ] Calibration within bounds (make calibration-check)
- [ ] No intelligence regression vs previous release (replay regression test)

### Functionality Gates
- [ ] All unit tests pass (make test-unit)
- [ ] All integration tests pass (make test-integration)
- [ ] Architecture boundary tests pass (make check-boundaries)
- [ ] Adapter conformance suite passes (make test-contract)
- [ ] Full dry-run pipeline completes (make dry-run)
- [ ] Checkpoint resume test passes for all stages (make test-chaos SUITE=resume)

### Infrastructure Gates
- [ ] Free Tier envelope test passes (make test-free-tier)
- [ ] Topology portability test passes (laptop → EC2 same image)
- [ ] Secret canary test passes (make test-secret-canary)
- [ ] Projection rebuild test passes (make verify-projections)

### Operations Gates
- [ ] Monthly chaos drill completed within past 30 days
- [ ] Restore drill completed within past 30 days (record RTO)
- [ ] All CRITICAL alerts resolved (no open critical incidents)

### Documentation Gates
- [ ] CHANGELOG updated with all changes since last release
- [ ] New requirement IDs documented if any added
- [ ] New ADRs documented if any added
- [ ] Ontology updated if any new entities added (ONT-001 procedure)
- [ ] Config defaults.yaml reflects any new configurable parameters

### Deployment Gates
- [ ] Migration tested against production-shaped data snapshot
- [ ] Images tagged with release SHA
- [ ] Deployment notes written (any manual steps required?)
- [ ] Rollback procedure documented for this release

Sign-off: [ ] Owner[ ] Lead Engineer
```

---

# 25. Frequently Asked Questions

**Q: Why can't I call the BeliefEngine directly from the LearningEngine? It would be simpler.**

Because "simpler now" means "impossible to evolve later." Direct calls create tight coupling: the LearningEngine would need to know the BeliefEngine exists, its interface, and its location. When you add a third engine that also needs to react to new lessons, you modify the LearningEngine again. With events, you add a subscriber — the LearningEngine never changes. The event bus is the contract; ADR-009 explains this in full.

---

**Q: I want to store the current confidence on the KnowledgeRecord and update it in place. Why is this so complicated?**

Because "the current value" is not the asset — the history is. If you overwrite confidence, you lose: why it changed, what evidence caused it, what the system believed last Tuesday when it made decision #482. ADR-004 explains this. The `confidence_history` on the `Belief` entity, and the supersession chain on `KnowledgeRecord`, are where this value lives. The engineering overhead is real; so is the benefit.

---

**Q: The simulation gate requires80% rule discovery. What if a planted rule is genuinely hard to find?**

That is the point. If a rule is hard to find with 50cycles, that tells you something important about the learning system's effectiveness. You should either: (a) fix the learning system so it finds the rule, or (b) understand why it cannot and document it as a known limitation. Lowering the threshold to make the gate pass is not acceptable — the threshold exists to protect the integrity of the intelligence claim.

---

**Q: Can I add a new metric to the FitnessVector?**

Yes, but it requires: (1) adding it to the Ontology Specification as a new field on FitnessVector, (2) writing an ADR explaining the new fitness dimension and its weight rationale, (3) defining a counter-metric pair for it (ADR-020/GOV-FIT-002), (4) updating the default weight profile as a new version, and (5) verifying the simulation gate still passes. This is intentionally thorough — fitness weights are the system's values.

---

**Q: Why is there no `DELETE` in the codebase for knowledge records?**

By design. `DELETE` on knowledge is ADR-004's hardest invariant. If you think you need to delete a knowledge record, you almost certainly need to: `DEPRECATE` it (contradictory evidence), `ARCHIVE` it (no longer relevant), or `CONSOLIDATE` it (duplicate). If after reviewing all three options you still believe deletion is correct, that is an architecture discussion requiring an ADR, not a code change.

---

**Q: The exploration rate is at 15% but the system keeps exploring the same things. Is that right?**

Exploration rate controls *how often* non-optimal candidates are selected; it does not control *which* candidates are explored. If exploration keeps landing on similar areas, review the Hypothesis Engine's novelty search (FR-EC-411, type=EXPLORATION) — it should be generating genuinely novel hypotheses, not variations on the top candidates. Check `core.decisions.exploration_ratio` in metrics — if the ratio is correct but exploration still seems redundant, the Hypothesis Engine's novelty scoring may need calibration.

---

**Q: How do I add support for a new LLM provider?**

1. Implement the `LLMProvider` interface in `execution/providers/llm/your_provider.py`
2. Add it to the provider registry in config
3. Map it to appropriate task classes in `providers.routing`
4. Add it to relevant fallback chains
5. Add a cost-per-token table for the Cost Ledger
6. Test: `make test-provider PROVIDER=your_provider` (runs the provider conformance suite)

Zero changes to Core engines. Zero changes to the Orchestrator. The abstraction layer exists precisely for this.

---
---

# Complete Documentation Index

```
EvolutionOS Documentation Set
│
├── 01_EvolutionOS_SRS_Foundation.md
│   Vision, Mission, Philosophy, Core Principles, Problem Statement,
│   Functional Requirements, NFRs, Quality Attributes, Design Principles,
│   Constraints, Assumptions, Risk Register, Success Metrics,
│   Acceptance Criteria, Future Vision
│
├── 02_EvolutionOS_SRS_Evolution_Core.md
│   Cognitive Architecture, Capability Hierarchy, Engine Specifications,
│   Domain Events, Event Sourcing, CQRS, Aggregate Design, Ontology Reference,
│   Evolution Cycle Saga, Core Metrics, Core Security, Simulation Harness
│
├── 03_EvolutionOS_SRS_Platform_Execution.md
│   Workflow Orchestrator, Research Pipeline, Story/Script/Narration/Visual/
│   Composition/Thumbnail/Publishing Engines, Platform Adapters,
│   AI Provider Management, Prompt Management, Human Approval Framework,
│   Dashboard Architecture, API Gateway, Plugin Framework
│
├── 04_EvolutionOS_SRS_Data_Infrastructure.md
│   System Topology, Event Store Design, Knowledge Graph Storage,
│   Caching, Message Queue, Scheduler, CI/CD Pipeline,
│   Monitoring & Observability, Backup & Recovery, Cost Optimization,
│   Security Architecture
│
├── 05_EvolutionOS_SRS_Evolution_Governance.md
│   Scientific Method Framework, Experimentation Governance,
│   Fitness Governance, Self-Optimization, Knowledge/Memory/Belief/Decision
│   Governance, Ethical & Safety Framework, Risk Register Extension,
│   Explainability Framework, Audit & Compliance, Product Roadmap v0.1–v5.0
│
├── 06_EvolutionOS_Ontology_Specification.md  ← THIS DOCUMENT SET
│   Complete entity definitions, lifecycles, relations, domain event catalog,
│   ontology change procedure (ONT-001)
│
├── 07_EvolutionOS_ADR_Register.md
│   ADR-001 through ADR-020 — all architectural decisions with
│   context, decision, rationale, consequences, status
│
├── 08_EvolutionOS_Implementation_Roadmap.md
│   v0.1 Skeleton → v0.2 Core Loop (Sim) → v0.3 Pipeline (Dry Run) →
│   v0.4 First Contact → v0.5 Learning Verified → v1.0 Supervised Autonomy
│   Each milestone: deliverables, gate criteria, duration estimate
│   v1.5–v5.0: outline roadmap
│
└── 09_EvolutionOS_Developer_Handbook.md
    Philosophy, Repository Structure, Feature Decision Tree,
    Engine/Aggregate/Service/Projection/Adapter/Prompt patterns,
    Testing Standards, PR Checklist, Common Mistakes, Local Dev Workflow,
    Operational Runbooks, Configuration Reference, Glossary,
    Intelligence Debugging Guide, Release Checklist, FAQ
```

---

## Documentation Set: **COMPLETE**

```
01Foundation██████████  The Constitution
02 Evolution Core██████████  The Mind
03 Platform Layer     ██████████  The Hands
04 Infrastructure     ██████████  The Body
05 Governance         ██████████  The Conscience
06 Ontology           ██████████  The Vocabulary
07 ADR Register       ██████████  The Decisions
08 Implementation     ██████████  The Roadmap
09 Developer Handbook ██████████  The Guide
```

**Total specification coverage:**

| Dimension | Count |
|---|---|
| Functional Requirements | FR-001–025, FR-EC-101–601, FR-PX-101–2101 |
| Non-Functional Requirements | NFR-PERF/REL/AVA/SCL/SEC/MNT/OBS/EXP/ADP/TST/PRT/AUT |
| Architecture Decision Records |