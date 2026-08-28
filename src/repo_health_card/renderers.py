import json

from repo_health_card.models import HealthReport


def render_markdown(report: HealthReport) -> str:
    lines = [
        f"# Repository health: `{report.repository}`",
        "",
        f"**Score: {report.score}/{report.maximum_score}**",
        "",
        "| Check | Result | Weight | Recommendation |",
        "| --- | --- | ---: | --- |",
    ]
    for check in report.checks:
        result = "Pass" if check.passed else "Needs attention"
        recommendation = "—" if check.passed else check.remediation
        lines.append(
            f"| {check.label} | {result} | {check.weight} | {recommendation} |"
        )
    return "\n".join(lines) + "\n"


def render_json(report: HealthReport) -> str:
    return json.dumps(report.to_dict(), indent=2, sort_keys=True) + "\n"
