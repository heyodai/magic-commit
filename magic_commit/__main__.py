import argparse
from .magic_commit import run_magic_commit

def main() -> None:
    """
    Entry point for the `magic-commit` command.
    """
    parser = argparse.ArgumentParser(description='Generate commit messages with OpenAI’s GPT.')

    parser.add_argument('-d', '--directory', help='Specify the git repository directory')
    parser.add_argument('-m', '--model', help='Specify the OpenAI GPT model')
    parser.add_argument('-k', '--key', metavar='API_KEY', help='Set your OpenAI API key')
    parser.add_argument('--set-model', metavar='MODEL_NAME', help='Set the default OpenAI GPT model')

    args = parser.parse_args()
    run_magic_commit(args)

if __name__ == '__main__':
    main()
