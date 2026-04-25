"""Assigns a version label to a milestone PR based on its commits.

Parses the Conventional Commits subject of each commit in the PR and assigns
the highest-impact version label: major > feature > fix/performance/revert.
If no versioned commits are found, no label is assigned (no version bump).
"""

import re
from enum import StrEnum

import requests


class Label(StrEnum):
    MAJOR = "major"
    FEATURE = "feature"
    FIX = "fix"
    PERFORMANCE = "performance"
    REVERT = "revert"


GITHUB_API_URL = "https://api.github.com"

BREAKING_RE = re.compile(r"^[a-z]+(\([^)]+\))?!:")
TYPE_RE = re.compile(r"^([a-z]+)(?:\([^)]+\))?!?:")
PATCH_LABELS = {Label.FIX, Label.PERFORMANCE, Label.REVERT}
VERSION_LABELS = {Label.MAJOR, Label.FEATURE, Label.FIX, Label.PERFORMANCE, Label.REVERT}


def make_headers(token):
    """Return GitHub API request headers authenticated with the given token.

    >>> make_headers("tok")
    {'Authorization': 'Bearer tok', 'Accept': 'application/vnd.github+json', 'X-GitHub-Api-Version': '2022-11-28'}
    """
    return {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }


def get_commits(repo, pr_number, headers):
    """Return all commits on a pull request, paginating as needed.

    Each element is a GitHub commit object as returned by the REST API.
    Raises requests.HTTPError on a non-2xx response.
    """
    commits = []
    page = 1
    while True:
        resp = requests.get(
            f"{GITHUB_API_URL}/repos/{repo}/pulls/{pr_number}/commits",
            headers=headers,
            params={"per_page": 100, "page": page},
        )
        resp.raise_for_status()
        batch = resp.json()
        if not batch:
            break
        commits.extend(batch)
        page += 1
    return commits


def _update_label(label, priority, type_):
    """Return an updated (label, priority) pair when a higher-priority type is found.

    Priority levels: 1 = feature, 2 = patch (fix/performance/revert).
    Lower number wins; the current label is kept if already at equal or higher priority.

    >>> _update_label(None, float("inf"), Label.FEATURE)
    (<Label.FEATURE: 'feature'>, 1)
    >>> _update_label(Label.FEATURE, 1, Label.FIX)
    (<Label.FEATURE: 'feature'>, 1)
    >>> _update_label(None, float("inf"), Label.FIX)
    (<Label.FIX: 'fix'>, 2)
    >>> _update_label(Label.FIX, 2, Label.PERFORMANCE)
    (<Label.FIX: 'fix'>, 2)
    """
    if type_ == Label.FEATURE and priority > 1:
        return Label.FEATURE, 1
    if type_ in PATCH_LABELS and priority > 2:
        return type_, 2
    return label, priority


def determine_label(commits):
    """Return the highest-impact version label from a list of GitHub commit objects.

    Scans each commit subject line for Conventional Commits syntax.
    Priority: breaking change (major) > feature > fix/performance/revert (patch).
    Returns None if no versioned commits are found.

    >>> def c(msg): return {"commit": {"message": msg}}
    >>> determine_label([c("feature: add thing")])
    <Label.FEATURE: 'feature'>
    >>> determine_label([c("fix: patch"), c("feature: add thing")])
    <Label.FEATURE: 'feature'>
    >>> determine_label([c("feature!: breaking change")])
    <Label.MAJOR: 'major'>
    >>> determine_label([c("fix: patch"), c("feature!: breaking")])
    <Label.MAJOR: 'major'>
    >>> determine_label([c("chore: update deps")]) is None
    True
    >>> determine_label([]) is None
    True
    """
    label = None
    priority = float("inf")
    for commit in commits:
        subject = commit["commit"]["message"].split("\n")[0]
        if BREAKING_RE.match(subject):
            return Label.MAJOR
        m = TYPE_RE.match(subject)
        if not m:
            continue
        label, priority = _update_label(label, priority, m.group(1))
    return label


def get_current_labels(repo, pr_number, headers):
    """Return the list of label names currently applied to a pull request.

    Raises requests.HTTPError on a non-2xx response.
    """
    resp = requests.get(
        f"{GITHUB_API_URL}/repos/{repo}/issues/{pr_number}/labels",
        headers=headers,
    )
    resp.raise_for_status()
    return [entry["name"] for entry in resp.json()]


def remove_label(repo, pr_number, name, headers):
    """Remove a label from a pull request, ignoring 404 if already absent.

    Raises requests.HTTPError on any non-2xx response other than 404.
    """
    resp = requests.delete(
        f"{GITHUB_API_URL}/repos/{repo}/issues/{pr_number}/labels/{name}",
        headers=headers,
    )
    if resp.status_code not in (200, 404):
        resp.raise_for_status()


def add_label(repo, pr_number, name, headers):
    """Add a label to a pull request.

    Raises requests.HTTPError on a non-2xx response.
    """
    resp = requests.post(
        f"{GITHUB_API_URL}/repos/{repo}/issues/{pr_number}/labels",
        headers=headers,
        json={"labels": [name]},
    )
    resp.raise_for_status()
