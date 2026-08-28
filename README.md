# Repo Health Card

Repo Health Card is a small command-line tool and GitHub Action that turns
GitHub's repository metadata into an actionable maintenance report.

It checks discovery metadata, issue availability, licensing, and community
health files. Every check has a visible weight and a concrete recommendation.

## Command-line usage

Install the project from source with [uv](https://docs.astral.sh/uv/):

```bash
uv tool install git+https://github.com/Apurva3509/repo-health-card
repo-health-card owner/repository
repo-health-card owner/repository --format json
```

Set `GITHUB_TOKEN` to increase API rate limits or inspect a private repository.

## GitHub Action

Add the report to a workflow's job summary:

```yaml
permissions:
  contents: read

steps:
  - uses: Apurva3509/repo-health-card@main
```

The action uses `github.repository` and `github.token` by default.

## Roadmap

- Configurable score policies
- Status badges for README files
- Organization-wide repository comparison

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for the development workflow and the
issue tracker for planned improvements.

## License

[MIT](LICENSE)
