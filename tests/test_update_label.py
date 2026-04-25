import pytest

from github_scripts.label_milestone_pr import PATCH_LABELS, Label, _update_label


class TestUpdateLabel:
    def test_feature_string_sets_feature(self):
        label, priority = _update_label(None, float("inf"), "feature")
        assert label == Label.FEATURE
        assert priority == 1

    def test_feat_no_change_when_already_feature(self):
        label, priority = _update_label(Label.FEATURE, 1, "feat")
        assert label == Label.FEATURE
        assert priority == 1

    @pytest.mark.parametrize(
        ("commit_type", "expected_label"),
        [
            ("fix", Label.FIX),
            ("performance", Label.PERFORMANCE),
            ("revert", Label.REVERT),
        ],
    )
    def test_patch_type_sets_patch_label(self, commit_type: str, expected_label: Label) -> None:
        label, priority = _update_label(None, float("inf"), commit_type)
        assert label == expected_label
        assert priority == 2

    def test_patch_does_not_override_feature(self):
        label, priority = _update_label(Label.FEATURE, 1, "fix")
        assert label == Label.FEATURE
        assert priority == 1

    def test_patch_does_not_override_existing_patch(self):
        label, priority = _update_label(Label.FIX, 2, "revert")
        assert label == Label.FIX
        assert priority == 2

    def test_unknown_type_leaves_label_unchanged(self):
        label, priority = _update_label(None, float("inf"), "chore")
        assert label is None
        assert priority == float("inf")


class TestPatchLabelsStrEnumCompatibility:
    def test_plain_strings_are_members(self):
        assert "fix" in PATCH_LABELS
        assert "performance" in PATCH_LABELS
        assert "revert" in PATCH_LABELS
