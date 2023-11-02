# Magic Commit! ✨

`magic-commit` is a command-line tool for writing your commit messages. It pings OpenAI's GPT-3 API to generate commit messages based on your commit history.

## Installation

On Mac:
```bash
brew install magic-commit
```

## Setup

You'll need to set up an OpenAI account and get an API key. You can do that on [OpenAI's website](https://platform.openai.com/account/api-keys).

Once you have a key, add it to `magic-commit` like so:
```bash
magic-commit -k <your-key-here>
```

## Usage

Running `magic-commit` is straightforward:
```bash
magic-commit # will run in your current directory
>>> [your commit message] # automatically copied to your clipboard
```

To specify a directory:
```bash
magic-commit -d <path-to-git-repo>
```

For help:
```bash
magic-commit -h # or --help
```

## Specifying a model

To change the model for this run:
```bash
magic-commit -m <model-name> 
```

To change the model globally:
```bash
magic-commit --set_model <model-name>
```

For models, note that:
- You need to specify an [OpenAI GPT model](https://platform.openai.com/docs/models).
    - e.g. `gpt-3.5-turbo-0301`, or `gpt-4`
- Your account needs to have access to the model you specify.