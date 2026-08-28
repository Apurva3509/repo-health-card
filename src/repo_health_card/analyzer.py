from collections.abc import Mapping
from typing import Any

from repo_health_card.models import CheckResult, HealthReport

CHECK_DEFINITIONS = (
    (
        "description",
        "Repository description",
        10,
        "Add a concise repository description.",
    ),
    ("topics", "Discovery topics", 10, "Add topics that describe the project."),
    ("license", "License", 15, "Choose and add an open-source license."),
    ("issues", "Issue tracker", 10, "Enable GitHub Issues for feedback."),
    ("readme", "README", 15, "Add a README with setup and usage guidance."),
    (
        "contributing",
        "Contributing guide",
        10,
        "Add CONTRIBUTING.md with a development workflow.",
    ),
    (
        "code_of_conduct",
        "Code of conduct",
        10,
        "Add a community code of conduct.",
    ),
    (
        "security",
        "Security policy",
        10,
        "Add SECURITY.md with private reporting instructions.",
    ),
    (
        "pull_request_template",
        "Pull request template",
        10,
        "Add a pull request template for consistent reviews.",
    ),
)


def analyze_repository(
    repository: str,
    metadata: Mapping[str, Any],
    community_profile: Mapping[str, Any],
) -> HealthReport:
    files = community_profile.get("files")
    community_files = files if isinstance(files, Mapping) else {}
    values = {
        "description": bool(metadata.get("description")),
        "topics": bool(metadata.get("topics")),
        "license": bool(metadata.get("license") or community_files.get("license")),
        "issues": bool(metadata.get("has_issues")),
        "readme": bool(community_files.get("readme")),
        "contributing": bool(community_files.get("contributing")),
        "code_of_conduct": bool(community_files.get("code_of_conduct")),
        "security": bool(community_files.get("security")),
        "pull_request_template": bool(community_files.get("pull_request_template")),
    }
    checks = tuple(
        CheckResult(
            key=key,
            label=label,
            passed=values[key],
            weight=weight,
            remediation=remediation,
        )
        for key, label, weight, remediation in CHECK_DEFINITIONS
    )
    return HealthReport(repository=repository, checks=checks)
