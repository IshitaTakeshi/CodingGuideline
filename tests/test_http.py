from unittest.mock import MagicMock, patch

import pytest
import requests

from github_scripts.label_milestone_pr import (
    GITHUB_API_URL,
    add_label,
    get_commits,
    get_current_labels,
    make_headers,
    remove_label,
)

REPO = "owner/repo"
PR = 42
HEADERS = {"Authorization": "Bearer tok"}


def _ok(data):
    m = MagicMock()
    m.status_code = 200
    m.json.return_value = data
    m.raise_for_status = MagicMock()
    return m


def _error(status_code):
    m = MagicMock()
    m.status_code = status_code
    m.raise_for_status.side_effect = requests.HTTPError(response=m)
    return m


class TestMakeHeaders:
    def test_contains_bearer_token(self):
        assert make_headers("my-token")["Authorization"] == "Bearer my-token"

    def test_contains_required_github_headers(self):
        headers = make_headers("tok")
        assert headers["Accept"] == "application/vnd.github+json"
        assert headers["X-GitHub-Api-Version"] == "2022-11-28"


class TestGetCommits:
    def test_single_page(self):
        commit = {"commit": {"message": "feat: add thing"}}
        with patch("requests.get") as mock_get:
            mock_get.side_effect = [_ok([commit]), _ok([])]
            result = get_commits(REPO, PR, HEADERS)
        assert result == [commit]

    def test_paginates_until_empty(self):
        c1 = {"commit": {"message": "feat: a"}}
        c2 = {"commit": {"message": "fix: b"}}
        with patch("requests.get") as mock_get:
            mock_get.side_effect = [_ok([c1]), _ok([c2]), _ok([])]
            result = get_commits(REPO, PR, HEADERS)
        assert result == [c1, c2]
        assert mock_get.call_count == 3

    def test_empty_pr_returns_empty_list(self):
        with patch("requests.get") as mock_get:
            mock_get.side_effect = [_ok([])]
            result = get_commits(REPO, PR, HEADERS)
        assert result == []

    def test_passes_correct_url_and_params(self):
        with patch("requests.get") as mock_get:
            mock_get.side_effect = [_ok([])]
            get_commits(REPO, PR, HEADERS)
        mock_get.assert_called_once_with(
            f"{GITHUB_API_URL}/repos/{REPO}/pulls/{PR}/commits",
            headers=HEADERS,
            params={"per_page": 100, "page": 1},
        )

    def test_raises_on_http_error(self):
        with patch("requests.get", return_value=_error(403)):
            with pytest.raises(requests.HTTPError):
                get_commits(REPO, PR, HEADERS)


class TestGetCurrentLabels:
    def test_returns_label_names(self):
        with patch("requests.get", return_value=_ok([{"name": "feature"}, {"name": "fix"}])):
            assert get_current_labels(REPO, PR, HEADERS) == ["feature", "fix"]

    def test_empty_returns_empty_list(self):
        with patch("requests.get", return_value=_ok([])):
            assert get_current_labels(REPO, PR, HEADERS) == []

    def test_raises_on_http_error(self):
        with patch("requests.get", return_value=_error(404)):
            with pytest.raises(requests.HTTPError):
                get_current_labels(REPO, PR, HEADERS)


class TestRemoveLabel:
    def test_200_does_not_raise(self):
        m = MagicMock()
        m.status_code = 200
        with patch("requests.delete", return_value=m):
            remove_label(REPO, PR, "feature", HEADERS)

    def test_404_is_silently_ignored(self):
        m = MagicMock()
        m.status_code = 404
        with patch("requests.delete", return_value=m):
            remove_label(REPO, PR, "feature", HEADERS)
        m.raise_for_status.assert_not_called()

    def test_other_error_raises(self):
        with patch("requests.delete", return_value=_error(500)):
            with pytest.raises(requests.HTTPError):
                remove_label(REPO, PR, "feature", HEADERS)

    def test_passes_correct_url(self):
        m = MagicMock()
        m.status_code = 200
        with patch("requests.delete", return_value=m) as mock_delete:
            remove_label(REPO, PR, "feature", HEADERS)
        mock_delete.assert_called_once_with(
            f"{GITHUB_API_URL}/repos/{REPO}/issues/{PR}/labels/feature",
            headers=HEADERS,
        )


class TestAddLabel:
    def test_successful_add_does_not_raise(self):
        with patch("requests.post", return_value=_ok([])):
            add_label(REPO, PR, "feature", HEADERS)

    def test_raises_on_http_error(self):
        with patch("requests.post", return_value=_error(422)):
            with pytest.raises(requests.HTTPError):
                add_label(REPO, PR, "feature", HEADERS)

    def test_passes_correct_url_and_payload(self):
        with patch("requests.post", return_value=_ok([])) as mock_post:
            add_label(REPO, PR, "feature", HEADERS)
        mock_post.assert_called_once_with(
            f"{GITHUB_API_URL}/repos/{REPO}/issues/{PR}/labels",
            headers=HEADERS,
            json={"labels": ["feature"]},
        )
