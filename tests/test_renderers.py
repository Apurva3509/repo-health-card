import json
import unittest

from repo_health_card.models import CheckResult, HealthReport
from repo_health_card.renderers import render_json, render_markdown, render_shields_json


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

    def test_shields_json_format_and_boundaries(self) -> None:
        # Default report has 60/100 score (60%), which should be orange
        output = json.loads(render_shields_json(self.report))
        self.assertEqual(output["schemaVersion"], 1)
        self.assertEqual(output["label"], "health")
        self.assertEqual(output["message"], "60/100")
        self.assertEqual(output["color"], "orange")

        # Helper function to test other boundary colors
        def make_report(score: int) -> HealthReport:
            return HealthReport(
                repository="test/repo",
                checks=(
                    CheckResult("p", "P", True, score, ""),
                    CheckResult("f", "F", False, 100 - score, "")
                )
            )

        # Testing boundary scores
        self.assertEqual(json.loads(render_shields_json(make_report(90)))["color"], "green")
        self.assertEqual(json.loads(render_shields_json(make_report(70)))["color"], "yellow")
        self.assertEqual(json.loads(render_shields_json(make_report(49)))["color"], "red")

if __name__ == "__main__":
    unittest.main()
