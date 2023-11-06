import argparse
import os

import dagwood

from .magic_commit import (
    get_api_key,
    get_model,
    run_magic_commit,
    set_api_key,
    set_model,
)


def main() -> None:
    """
    Entry point for the `magic-commit` command.
    """
    # Set up logging
    log = dagwood.assemble(format="")

    # Get the command line arguments
    parser = argparse.ArgumentParser(
        description="Generate commit messages with OpenAI’s GPT."
    )

    parser.add_argument(
        "-d", "--directory", help="Specify the git repository directory"
    )
    parser.add_argument("-m", "--model", help="Specify the OpenAI GPT model")
    parser.add_argument(
        "-k", "--key", metavar="API_KEY", help="Set your OpenAI API key"
    )
    parser.add_argument(
        "--set-model", metavar="MODEL_NAME", help="Set the default OpenAI GPT model"
    )

    # Decide what to do based on the arguments
    args = parser.parse_args()
    if args.key:
        set_api_key(args.key, log)

    else:
        directory = args.directory or "."  # Default to the current directory
        directory = os.path.expanduser(
            directory
        )  # Expand the user's home directory if the tilde is used
        directory = os.path.abspath(
            directory
        )  # Convert relative paths to absolute paths

        key = get_api_key()
        model = get_model()
        results = run_magic_commit(directory=directory, api_key=key, model=model)

        print(results)


if __name__ == "__main__":
    main()
