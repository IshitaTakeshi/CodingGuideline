import argparse

from github_scripts.label_milestone_pr import (
    VERSION_LABELS,
    add_label,
    determine_label,
    get_commits,
    get_current_labels,
    make_headers,
    remove_label,
)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--token", required=True)
    parser.add_argument("--repo", required=True)
    parser.add_argument("--pr-number", type=int, required=True)
    return parser.parse_args()


def main():
    """Assign the most significant version label to a milestone PR.

    Fetches all commits in the PR, determines the highest-impact version label
    (major > feature > patch > none), removes any stale version labels, and
    assigns the new one. If no versioned commits are found, no label is assigned.

    The workflow triggers on every push to the PR, so this function may run
    multiple times. Stale version labels from prior runs are always removed
    before the new label is assigned.

    Examples
    --------
    1. First run, one feature commit:
         Labels before : (none)
         Commits       : feature: add login
         Labels after  : feature

    2. Developer pushes a breaking change; workflow re-runs:
         Labels before : feature
         Commits       : feature: add login, fix!: breaking auth change
         Labels after  : major

    3. Developer pushes only a non-versioned commit; label is re-applied from history:
         Labels before : major
         Commits       : fix!: breaking auth change, documentation: update README
         Labels after  : major
    """
    args = parse_args()
    headers = make_headers(args.token)

    commits = get_commits(args.repo, args.pr_number, headers)
    label = determine_label(commits)

    for existing in get_current_labels(args.repo, args.pr_number, headers):
        if existing in VERSION_LABELS:
            remove_label(args.repo, args.pr_number, existing, headers)

    if not label:
        print("No version label assigned (no versioned commits found)")
        return
    add_label(args.repo, args.pr_number, label, headers)
    print(f"Assigned label: {label}")


if __name__ == "__main__":
    main()
