import json

from repo_health_card.models import HealthReport

BADGE_COLORS = (
    (90, "brightgreen"),
    (75, "green"),
    (60, "yellowgreen"),
    (40, "yellow"),
    (20, "orange"),
    (0, "red"),
)


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


def render_badge(report: HealthReport) -> str:
    percentage = (
        round(report.score / report.maximum_score * 100) if report.maximum_score else 0
    )
    color = next(color for minimum, color in BADGE_COLORS if percentage >= minimum)
    payload = {
        "schemaVersion": 1,
        "label": "repo health",
        "message": f"{percentage}%",
        "color": color,
    }
    return json.dumps(payload, indent=2, sort_keys=True) + "\n"
