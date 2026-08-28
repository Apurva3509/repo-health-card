import io
import unittest
from urllib.error import HTTPError

from repo_health_card.github import GitHubApiError, GitHubClient


class Response(io.BytesIO):
    def __enter__(self) -> "Response":
        return self

    def __exit__(self, *args: object) -> None:
        self.close()


class GitHubClientTest(unittest.TestCase):
    def test_sends_authentication_and_api_headers(self) -> None:
        requests = []

        def opener(request: object, timeout: int) -> Response:
            requests.append((request, timeout))
            return Response(b'{"description": "example"}')

        result = GitHubClient(token="secret", opener=opener).repository("octo/example")

        request, timeout = requests[0]
        self.assertEqual(result, {"description": "example"})
        self.assertEqual(timeout, 15)
        self.assertEqual(request.get_header("Authorization"), "Bearer secret")
        self.assertEqual(request.get_header("X-github-api-version"), "2022-11-28")

    def test_translates_http_errors(self) -> None:
        def opener(request: object, timeout: int) -> Response:
            raise HTTPError(request.full_url, 404, "Not Found", {}, None)

        with self.assertRaisesRegex(GitHubApiError, "HTTP 404"):
            GitHubClient(opener=opener).repository("octo/missing")


if __name__ == "__main__":
    unittest.main()
