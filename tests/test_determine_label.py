import pytest

from github_scripts.label_milestone_pr import VERSION_LABELS, Label, determine_label


def _make_commit(subject: str):
    return {"commit": {"message": subject}}


class TestDetermineLabel:
    def test_empty_commits_returns_none(self):
        assert determine_label([]) is None

    def test_unrecognized_types_return_none(self):
        commits = [_make_commit("chore: update deps"), _make_commit("docs: update readme")]
        assert determine_label(commits) is None

    @pytest.mark.parametrize("subject,expected", [
        ("feature: add feature", Label.FEATURE),
        ("fix: fix bug", Label.FIX),
        ("performance: improve speed", Label.PERFORMANCE),
        ("revert: revert change", Label.REVERT),
        ("feature!: breaking change", Label.MAJOR),
        ("feature(scope)!: breaking change", Label.MAJOR),
        ("feature(auth): add login", Label.FEATURE),
        ("fix(ui): fix button", Label.FIX),
    ])
    def test_single_commit_label(self, subject: str, expected: Label) -> None:
        assert determine_label([_make_commit(subject)]) == expected

    def test_feature_beats_fix_regardless_of_order(self):
        commits = [_make_commit("fix: fix bug"), _make_commit("feature: add feature")]
        assert determine_label(commits) == Label.FEATURE

    def test_breaking_commit_short_circuits_to_major(self):
        commits = [_make_commit("feat: add feature"), _make_commit("fix!: breaking"), _make_commit("revert: r")]
        assert determine_label(commits) == Label.MAJOR

    def test_multiline_message_uses_subject_only(self):
        message = "feature: add feature\n\nfix!: this line is in the body and not parsed"
        assert determine_label([_make_commit(message)]) == Label.FEATURE


class TestVersionLabelsStrEnumCompatibility:
    def test_plain_strings_are_members(self):
        for string_label in ("major", "feature", "fix", "performance", "revert"):
            assert string_label in VERSION_LABELS
