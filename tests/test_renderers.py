import json
import unittest

from repo_health_card.models import CheckResult, HealthReport
from repo_health_card.renderers import render_json, render_markdown


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


if __name__ == "__main__":
    unittest.main()
