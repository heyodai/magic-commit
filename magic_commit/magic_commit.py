import os
import subprocess

import openai
from jinja2 import Environment, PackageLoader

from .config import get_api_key, get_model, set_api_key, set_model


class GitRepositoryError(Exception):
    """Custom exception for Git repository errors."""

    pass


class OpenAIKeyError(Exception):
    """Custom exception for OpenAI API key errors."""

    pass


def is_git_repository(directory: str) -> bool:
    """
    Check if a directory is a Git repository.

    Parameters
    ----------
    directory : str
        The path to check.

    Returns
    -------
    bool
        True if the directory is a Git repository, False otherwise.
    """
    print(directory)
    return os.path.isdir(os.path.join(directory, ".git"))


def run_git_diff(directory: str) -> str:
    """
    Run the `git diff --cached` command and return the result.

    Parameters
    ----------
    directory : str
        The directory to run the command in.

    Returns
    -------
    str
        The output of the command.
    """
    # TODO: Write unit tests for this function
    return subprocess.run(
        ["git", "diff", "--cached"], cwd=directory, capture_output=True, text=True
    ).stdout


def run_git_log(directory: str) -> subprocess.CompletedProcess:
    """
    Run 'git log' command in a specified directory.

    Parameters
    ----------
    directory : str
        The directory to run the command in.

    Returns
    -------
    subprocess.CompletedProcess
        The result of the subprocess run command.
    """
    return subprocess.run(
        ["git", "log", "--pretty=%B", "-n", "10"],
        cwd=directory,
        capture_output=True,
        text=True,
    )


def get_commit_messages(directory: str) -> str:
    """
    Fetch the last 10 commit messages from the Git repository.

    Parameters
    ----------
    directory : str
        The path to the Git repository.

    Returns
    -------
    str
        The commit messages.

    Raises
    ------
    GitRepositoryError
        If the specified directory is not a Git repository.
    """
    if not is_git_repository(directory):
        raise GitRepositoryError("The specified directory is not a Git repository.")

    result = run_git_log(directory)

    if result.returncode != 0:
        raise GitRepositoryError("Unable to get commit messages.")

    return result.stdout


def generate_commit_message(diff: str, api_key: str, model: str) -> str:
    """
    Generate a commit message.

    Parameters
    ----------
    diff : str
        The git diff to use.
    api_key : str
        The OpenAI API key.
    model : str
        The OpenAI GPT model to use.

    Returns
    -------
    str
        The generated commit message.

    Raises
    ------
    OpenAIKeyError
        If the OpenAI API key is not set.
    """
    # Perform guard check for the OpenAI API key
    if not api_key:
        raise OpenAIKeyError("OpenAI API key not set.")

    # Generate the prompt
    system_msg = render_template("", "system")
    user_msg = render_template(diff, "user")

    # Generate the commit message
    messages = [
        {"role": "system", "content": system_msg},
        {"role": "user", "content": user_msg},
    ]
    openai.api_key = api_key
    response = openai.ChatCompletion.create(model=model, messages=messages)
    return response.choices[0].message.content.strip()


def render_template(message: str, template_name: str) -> str:
    """
    Render the commit message template.

    Parameters
    ----------
    message : str
        The commit message to render.
    template_name : str
        The name of the template to use.

    Returns
    -------
    str
        The rendered commit message.
    """
    # TODO: Write unit tests for this function

    # Render any escape sequences in the message
    message.encode().decode("unicode_escape")

    # Render and return the template
    jinja = Environment(loader=PackageLoader("magic_commit", "templates")).get_template(
        f"{template_name}.jinja"
    )
    return jinja.render(diff=message)


def run_magic_commit(directory: str, api_key: str, model: str) -> str:
    """
    Generate a commit message and return it.

    Parameters
    ----------
    directory : str
        The path to the Git repository.
    api_key : str
        The OpenAI API key.
    model : str
        The OpenAI GPT model to use.

    Returns
    -------
    str
        The generated commit message.
    """
    diff = run_git_diff(directory)
    commit_message = generate_commit_message(diff, api_key, model)
    return commit_message
