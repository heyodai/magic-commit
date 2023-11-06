import os
import subprocess

import openai
from jinja2 import Environment, PackageLoader

from .config import get_api_key, set_api_key, get_model, set_model


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
    return os.path.isdir(os.path.join(directory, ".git"))


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


def generate_commit_message(commit_messages: str, api_key: str, model: str) -> str:
    """
    Generate a commit message.

    Parameters
    ----------
    commit_messages : str
        The commit messages to use as context.
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
    # Throw an error if the API key is not set
    if not api_key:
        raise OpenAIKeyError("OpenAI API key not set.")

    # Set the OpenAI API key
    openai.api_key = api_key

    # Render the template
    commit_messages_list = commit_messages.strip().split("\n")
    jinja = Environment(loader=PackageLoader("magic_commit", "templates")).get_template(
        "chat_completion.jinja"
    )
    message = commit_messages_list[-1] if commit_messages_list else ""
    rendered_template = jinja.render(message=message)

    # Generate the commit message
    messages = [{"role": "system", "content": rendered_template}]
    response = openai.ChatCompletion.create(model=model, messages=messages)
    return response.choices[0].message.content.strip()


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
    commit_messages = get_commit_messages(directory)
    commit_message = generate_commit_message(commit_messages, api_key, model)
    return commit_message
