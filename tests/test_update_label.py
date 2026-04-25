import pytest

from github_scripts.label_milestone_pr import PATCH_TYPES, Label, _update_label


class TestUpdateLabel:
    def test_feature_string_sets_feature(self):
        label, priority = _update_label(None, float("inf"), "feature")
        assert label == Label.FEATURE
        assert priority == 1

    def test_feat_no_change_when_already_feature(self):
        label, priority = _update_label(Label.FEATURE, 1, "feat")
        assert label == Label.FEATURE
        assert priority == 1

    @pytest.mark.parametrize("commit_type", ["fix", "performance", "revert"])
    def test_patch_type_sets_patch_label(self, commit_type: str) -> None:
        label, priority = _update_label(None, float("inf"), commit_type)
        assert label == commit_type
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


class TestPatchTypesStrEnumCompatibility:
    def test_plain_strings_are_members(self):
        assert "fix" in PATCH_TYPES
        assert "performance" in PATCH_TYPES
        assert "revert" in PATCH_TYPES
