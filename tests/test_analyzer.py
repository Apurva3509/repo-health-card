import unittest

from repo_health_card.analyzer import analyze_repository


class AnalyzeRepositoryTest(unittest.TestCase):
    def test_scores_present_metadata_and_community_files(self) -> None:
        metadata = {
            "description": "A useful project",
            "topics": ["github"],
            "license": {"spdx_id": "MIT"},
            "has_issues": True,
        }
        community = {
            "files": {
                "readme": {"url": "readme"},
                "contributing": {"url": "contributing"},
                "code_of_conduct": None,
                "security": None,
                "pull_request_template": None,
            }
        }

        report = analyze_repository("octo/example", metadata, community)

        self.assertEqual(report.score, 70)
        self.assertEqual(report.maximum_score, 100)
        self.assertEqual(
            [check.key for check in report.checks if not check.passed],
            ["code_of_conduct", "security", "pull_request_template"],
        )

    def test_handles_missing_community_files(self) -> None:
        report = analyze_repository(
            "octo/example", {"has_issues": False}, {"files": None}
        )

        self.assertEqual(report.score, 0)
        self.assertTrue(all(not check.passed for check in report.checks))


if __name__ == "__main__":
    unittest.main()
