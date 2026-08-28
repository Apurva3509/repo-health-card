import json
from collections.abc import Callable
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

API_ROOT = "https://api.github.com"
USER_AGENT = "repo-health-card/0.1"


class GitHubApiError(RuntimeError):
    pass


class GitHubClient:
    def __init__(
        self,
        token: str | None = None,
        opener: Callable[..., Any] = urlopen,
    ) -> None:
        self._token = token
        self._opener = opener

    def repository(self, repository: str) -> dict[str, Any]:
        return self._get(f"/repos/{repository}")

    def community_profile(self, repository: str) -> dict[str, Any]:
        return self._get(f"/repos/{repository}/community/profile")

    def _get(self, path: str) -> dict[str, Any]:
        headers = {
            "Accept": "application/vnd.github+json",
            "User-Agent": USER_AGENT,
            "X-GitHub-Api-Version": "2022-11-28",
        }
        if self._token:
            headers["Authorization"] = f"Bearer {self._token}"

        request = Request(f"{API_ROOT}{path}", headers=headers)
        try:
            with self._opener(request, timeout=15) as response:
                payload = json.load(response)
        except HTTPError as error:
            raise GitHubApiError(
                f"GitHub API returned HTTP {error.code} for {path}"
            ) from error
        except (URLError, TimeoutError) as error:
            raise GitHubApiError(f"Could not reach the GitHub API: {error}") from error

        if not isinstance(payload, dict):
            raise GitHubApiError(
                f"GitHub API returned an unexpected response for {path}"
            )
        return payload
