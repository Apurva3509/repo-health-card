import argparse
import os
import sys
from pathlib import Path
from typing import NoReturn

from repo_health_card.analyzer import analyze_repository
from repo_health_card.github import GitHubApiError, GitHubClient
from repo_health_card.renderers import render_badge, render_json, render_markdown

FORMATTERS = {
    "badge": render_badge,
    "json": render_json,
    "markdown": render_markdown,
}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Generate a health report for a GitHub repository."
    )
    parser.add_argument(
        "repository",
        nargs="?",
        default=os.environ.get("GITHUB_REPOSITORY"),
        help="Repository in owner/name form; defaults to GITHUB_REPOSITORY.",
    )
    parser.add_argument(
        "--format",
        choices=FORMATTERS,
        default="markdown",
        help="Output format.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="Write the report to this file instead of standard output.",
    )
    return parser


def fail(message: str) -> NoReturn:
    sys.stderr.write(f"repo-health-card: {message}\n")
    raise SystemExit(1)


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if not args.repository or args.repository.count("/") != 1:
        fail("repository must use the owner/name format")

    client = GitHubClient(token=os.environ.get("GITHUB_TOKEN"))
    try:
        metadata = client.repository(args.repository)
        community_profile = client.community_profile(args.repository)
    except GitHubApiError as error:
        fail(str(error))

    report = analyze_repository(args.repository, metadata, community_profile)
    output = FORMATTERS[args.format](report)
    if args.output:
        args.output.write_text(output, encoding="utf-8")
    else:
        sys.stdout.write(output)
    return 0
