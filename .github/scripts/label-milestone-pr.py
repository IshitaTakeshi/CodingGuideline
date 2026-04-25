"""Assigns a version label to a milestone PR based on its commits.

Parses the Conventional Commits subject of each commit in the PR and assigns
the highest-impact version label: major > feature > fix/performance/revert.
If no versioned commits are found, no label is assigned (no version bump).
"""

import os
import re
import sys

import requests

TOKEN = os.environ["GITHUB_TOKEN"]
REPO = os.environ["GITHUB_REPOSITORY"]
PR_NUMBER = int(os.environ["PR_NUMBER"])

HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Accept": "application/vnd.github+json",
    "X-GitHub-Api-Version": "2022-11-28",
}
BASE_URL = f"https://api.github.com/repos/{REPO}"

BREAKING_RE = re.compile(r"^[a-z]+(\([^)]+\))?!:")
TYPE_RE = re.compile(r"^([a-z]+)(?:\([^)]+\))?!?:")
PATCH_TYPES = {"fix", "performance", "revert"}
VERSION_LABELS = {"major", "feature", "fix", "performance", "revert"}


def get_commits():
    commits = []
    page = 1
    while True:
        resp = requests.get(
            f"{BASE_URL}/pulls/{PR_NUMBER}/commits",
            headers=HEADERS,
            params={"per_page": 100, "page": page},
        )
        resp.raise_for_status()
        batch = resp.json()
        if not batch:
            break
        commits.extend(batch)
        page += 1
    return commits


def determine_label(commits):
    label = None
    priority = float("inf")
    for commit in commits:
        subject = commit["commit"]["message"].split("\n")[0]
        if BREAKING_RE.match(subject):
            return "major"
        m = TYPE_RE.match(subject)
        if m:
            type_ = m.group(1)
            if type_ == "feature" and priority > 1:
                label, priority = "feature", 1
            elif type_ in PATCH_TYPES and priority > 2:
                label, priority = type_, 2
    return label


def get_current_labels():
    resp = requests.get(f"{BASE_URL}/issues/{PR_NUMBER}/labels", headers=HEADERS)
    resp.raise_for_status()
    return [entry["name"] for entry in resp.json()]


def remove_label(name):
    resp = requests.delete(
        f"{BASE_URL}/issues/{PR_NUMBER}/labels/{name}", headers=HEADERS
    )
    if resp.status_code not in (200, 404):
        resp.raise_for_status()
    print(f"Removed label: {name}")


def add_label(name):
    resp = requests.post(
        f"{BASE_URL}/issues/{PR_NUMBER}/labels",
        headers=HEADERS,
        json={"labels": [name]},
    )
    resp.raise_for_status()
    print(f"Assigned label: {name}")


def main():
    commits = get_commits()
    label = determine_label(commits)

    for existing in get_current_labels():
        if existing in VERSION_LABELS:
            remove_label(existing)

    if label:
        add_label(label)
    else:
        print("No version label assigned (no versioned commits found)")


if __name__ == "__main__":
    main()
