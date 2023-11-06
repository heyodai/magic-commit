import os
import subprocess
from logging import Logger  # Just so the linter doesn't complain

import openai
from jinja2 import Environment, PackageLoader

from .config import get_api_key, set_api_key


def get_commit_messages(directory) -> str:
    """
    Fetch the last 10 commit messages from the Git repository.

    Parameters
    ----------
    directory : str
        The path to the Git repository.

    Returns
    -------
    str
        The last 10 commit messages.

    Raises
    ------
    Exception
        If the specified directory is not a Git repository.
    """
    if not os.path.isdir(os.path.join(directory, ".git")):
        raise Exception("Error: The specified directory is not a Git repository.")

    # Run 'git log' to get the commit messages
    result = subprocess.run(
        ["git", "log", "--pretty=%B", "-n", "10"],
        cwd=directory,
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        raise Exception(
            "Error: Unable to get commit messages. Are you in a Git repository?"
        )

    return result.stdout


def generate_commit_message(commit_messages: str, model: str = "gpt-3.5-turbo") -> str:
    """
    Generate a commit message.

    Parameters
    ----------
    commit_messages : str
        The last 10 commit messages.
    model : str, optional
        The OpenAI GPT model to use, by default "gpt-3.5-turbo"

    Returns
    -------
    str
        The generated commit message.

    Raises
    ------
    Exception
        If the OpenAI API key is not set.
    """
    # Verify an API key is set
    if not get_api_key():
        raise Exception(
            "Error: OpenAI API key not set. Use the -k flag to set your API key."
        )

    # Create a list of messages to send to the API
    openai.api_key = get_api_key()
    commit_messages_list = commit_messages.strip().split("\n")
    jinja = Environment(loader=PackageLoader("magic_commit", "templates")).get_template(
        "chat_completion.jinja"
    )
    message = (
        commit_messages_list[-1]
        if len(commit_messages_list) > 1
        else commit_messages_list[0]
    )
    rendered_template = jinja.render(message=message)

    # Send the messages to the API
    messages = [{"role": "system", "content": rendered_template}]
    response = openai.ChatCompletion.create(model=model, messages=messages)
    return response["choices"][0]["message"]["content"].strip()


def run_magic_commit(args: dict, log: Logger) -> None:
    """
    Generate a commit message and print it to the console.

    Parameters
    ----------
    args : dict
        The command line arguments.
    log : Logger
        The logger.

    Raises
    ------
    Exception
        If the specified directory is not a Git repository.
    """
    # Get commit messages
    directory = args.directory or "."
    commit_messages = get_commit_messages(directory)

    # Generate a commit message
    try:
        model = args.model or "gpt-3.5-turbo"
        commit_message = generate_commit_message(commit_messages, model)
        log.info(commit_message)
    except Exception as e:
        log.error(e)

    return
