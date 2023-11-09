import argparse
import os

import dagwood
import pyperclip

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
    parser.add_argument(
        "--no-copy",
        action="store_true",
        help="Do not copy the commit message to the clipboard",
    )
    parser.add_argument(
        "--no-load", action="store_true", help="Do not show loading message"
    )
    parser.add_argument(
        "-t",
        "--ticket",
        help="Request that the provided GitHub issue be linked in the commit message",
        type=int,
    )
    parser.add_argument("-s", "--start", help="Provide the start of the commit message")
    parser.add_argument("--llama", help="Pass a localhost Llama2 server as a replacement for OpenAI API")

    # Decide what to do based on the arguments
    args = parser.parse_args()
    if args.key:
        # Set the OpenAI API key
        try:
            set_api_key(args.key)
            print("🔑 OpenAI API key set!")
        except OSError as e:
            print("Unable to set OpenAI API key.")
        except Exception as e:
            print(e)

    else:
        # Generate a commit message
        directory = args.directory or "."  # Default to the current directory
        directory = os.path.expanduser(
            directory
        )  # Expand the user's home directory if the tilde is used
        directory = os.path.abspath(
            directory
        )  # Convert relative paths to absolute paths

        key = get_api_key()
        model = get_model()
        ticket = f"Closes #{args.ticket}" if args.ticket else ""
        start = args.start if args.start else ""
        show_loading_message = False if args.no_load else True

        results = run_magic_commit(
            directory=directory,
            api_key=key,
            model=model,
            ticket=ticket,
            start=start,
            show_loading_message=show_loading_message,
            llama2_url=args.llama,
        )

        print(results)
        if not args.no_copy:
            pyperclip.copy(results)


if __name__ == "__main__":
    main()
