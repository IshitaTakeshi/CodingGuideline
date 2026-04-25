"""Assigns a version label to a milestone PR based on its commits.

Parses the Conventional Commits subject of each commit in the PR and assigns
the highest-impact version label: major > feature > fix/performance/revert.
If no versioned commits are found, no label is assigned (no version bump).
"""

import argparse
import re

import requests

BREAKING_RE = re.compile(r"^[a-z]+(\([^)]+\))?!:")
TYPE_RE = re.compile(r"^([a-z]+)(?:\([^)]+\))?!?:")
PATCH_TYPES = {"fix", "performance", "revert"}
VERSION_LABELS = {"major", "feature", "fix", "performance", "revert"}


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--token", required=True)
    parser.add_argument("--repo", required=True)
    parser.add_argument("--pr-number", type=int, required=True)
    return parser.parse_args()


def make_headers(token):
    return {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }


def get_commits(repo, pr_number, headers):
    commits = []
    page = 1
    while True:
        resp = requests.get(
            f"https://api.github.com/repos/{repo}/pulls/{pr_number}/commits",
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


def determine_label(commits):
    label = None
    priority = float("inf")
    for commit in commits:
        subject = commit["commit"]["message"].split("\n")[0]
        if BREAKING_RE.match(subject):
            return "major"
        m = TYPE_RE.match(subject)
        if not m:
            continue
        type_ = m.group(1)
        if type_ == "feature" and priority > 1:
            label, priority = "feature", 1
        elif type_ in PATCH_TYPES and priority > 2:
            label, priority = type_, 2
    return label


def get_current_labels(repo, pr_number, headers):
    resp = requests.get(
        f"https://api.github.com/repos/{repo}/issues/{pr_number}/labels",
        headers=headers,
    )
    resp.raise_for_status()
    return [entry["name"] for entry in resp.json()]


def remove_label(repo, pr_number, name, headers):
    resp = requests.delete(
        f"https://api.github.com/repos/{repo}/issues/{pr_number}/labels/{name}",
        headers=headers,
    )
    if resp.status_code not in (200, 404):
        resp.raise_for_status()


def add_label(repo, pr_number, name, headers):
    resp = requests.post(
        f"https://api.github.com/repos/{repo}/issues/{pr_number}/labels",
        headers=headers,
        json={"labels": [name]},
    )
    resp.raise_for_status()


def main():
    args = parse_args()
    headers = make_headers(args.token)

    commits = get_commits(args.repo, args.pr_number, headers)
    label = determine_label(commits)

    for existing in get_current_labels(args.repo, args.pr_number, headers):
        if existing in VERSION_LABELS:
            remove_label(args.repo, args.pr_number, existing, headers)
            print(f"Removed label: {existing}")

    if not label:
        print("No version label assigned (no versioned commits found)")
        return
    add_label(args.repo, args.pr_number, label, headers)
    print(f"Assigned label: {label}")


if __name__ == "__main__":
    main()
