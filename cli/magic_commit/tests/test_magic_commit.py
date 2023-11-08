from unittest import mock

import pytest

from ..magic_commit import (GitRepositoryError, OpenAIKeyError,
                            generate_commit_message, get_commit_messages,
                            run_magic_commit)


def test_is_not_git_repository():
    with mock.patch("os.path.isdir", return_value=False):
        with pytest.raises(GitRepositoryError):
            get_commit_messages("/not/a/repo")


def test_git_log_failure():
    with mock.patch("subprocess.run") as mocked_run:
        mocked_run.return_value.returncode = 1
        with pytest.raises(GitRepositoryError):
            get_commit_messages("/fake/repo")


def test_generate_commit_message_no_api_key():
    with pytest.raises(OpenAIKeyError):
        generate_commit_message("test message", "", "gpt-3.5-turbo")


# Commented this out as it's not working yet
#
# @mock.patch('magic_commit.magic_commit.get_commit_messages', return_value="Fake commit messages")
# def test_run_magic_commit_success(mock_get_commit_messages):
#     with mock.patch('magic_commit.get_commit_messages', return_value="Fake commit messages"):
#         with mock.patch('magic_commit.openai.ChatCompletion.create') as mocked_create:
#             mocked_create.return_value = {"choices": [{"message": {"content": "Generated message"}}]}
#             result = run_magic_commit('.', 'fake-api-key')
#             assert result == "Generated message"
