"""
DirectiveIssuer Port Interface (`Plan.md` Section 5 / Appendix B).
Abstract boundary contract defining how the Core issues experiment directives across the boundary to the Execution Layer (`EC-BND-001`).
"""
from abc import ABC, abstractmethod
from evolutionos.core.domain.ontology import ExperimentDirective


class DirectiveIssuer(ABC):
    @abstractmethod
    def issue_directive(self, directive: ExperimentDirective) -> bool:
        pass
