from dataclasses import asdict, dataclass
from typing import Any


@dataclass(frozen=True)
class CheckResult:
    key: str
    label: str
    passed: bool
    weight: int
    remediation: str


@dataclass(frozen=True)
class HealthReport:
    repository: str
    checks: tuple[CheckResult, ...]

    @property
    def score(self) -> int:
        return sum(check.weight for check in self.checks if check.passed)

    @property
    def maximum_score(self) -> int:
        return sum(check.weight for check in self.checks)

    def to_dict(self) -> dict[str, Any]:
        return {
            "repository": self.repository,
            "score": self.score,
            "maximum_score": self.maximum_score,
            "checks": [asdict(check) for check in self.checks],
        }
