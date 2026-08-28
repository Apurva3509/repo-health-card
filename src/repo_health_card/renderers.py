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

def render_shields_json(report: HealthReport) -> str:
    """Renders a Shields.io custom endpoint JSON with documented thresholds."""
    percentage = 0
    if report.maximum_score > 0:
        percentage = (report.score / report.maximum_score) * 100

    # Score-to-color thresholds
    if percentage >= 90:
        color = "green"
    elif percentage >= 70:
        color = "yellow"
    elif percentage >= 50:
        color = "orange"
    else:
        color = "red"

    payload = {
        "schemaVersion": 1,
        "label": "health",
        "message": f"{report.score}/{report.maximum_score}",
        "color": color
    }
    return json.dumps(payload, indent=2) + "\n"