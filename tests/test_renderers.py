import json
import unittest

from repo_health_card.models import CheckResult, HealthReport
from repo_health_card.renderers import render_badge, render_json, render_markdown


class RenderersTest(unittest.TestCase):
    def setUp(self) -> None:
        self.report = HealthReport(
            repository="octo/example",
            checks=(
                CheckResult("readme", "README", True, 60, "Add a README."),
                CheckResult("security", "Security", False, 40, "Add SECURITY.md."),
            ),
        )

    def test_markdown_contains_score_and_failed_recommendation(self) -> None:
        output = render_markdown(self.report)

        self.assertIn("**Score: 60/100**", output)
        self.assertIn("| README | Pass | 60 | — |", output)
        self.assertIn("Add SECURITY.md.", output)

    def test_json_is_machine_readable(self) -> None:
        output = json.loads(render_json(self.report))

        self.assertEqual(output["repository"], "octo/example")
        self.assertEqual(output["score"], 60)
        self.assertFalse(output["checks"][1]["passed"])

    def test_badge_uses_shields_endpoint_schema(self) -> None:
        output = json.loads(render_badge(self.report))

        self.assertEqual(
            output,
            {
                "schemaVersion": 1,
                "label": "repo health",
                "message": "60%",
                "color": "yellowgreen",
            },
        )

    def test_badge_color_boundaries(self) -> None:
        expected_colors = {
            0: "red",
            20: "orange",
            40: "yellow",
            60: "yellowgreen",
            75: "green",
            90: "brightgreen",
            100: "brightgreen",
        }

        for score, expected_color in expected_colors.items():
            with self.subTest(score=score):
                report = HealthReport(
                    repository="octo/example",
                    checks=(
                        CheckResult("score", "Score", True, score, ""),
                        CheckResult("gap", "Gap", False, 100 - score, ""),
                    ),
                )
                output = json.loads(render_badge(report))
                self.assertEqual(output["color"], expected_color)

    def test_badge_handles_an_empty_policy(self) -> None:
        report = HealthReport(repository="octo/example", checks=())

        output = json.loads(render_badge(report))

        self.assertEqual(output["message"], "0%")
        self.assertEqual(output["color"], "red")


if __name__ == "__main__":
    unittest.main()
