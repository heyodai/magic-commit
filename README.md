# Magic Commit! ✨ 🍰

<img src="splash-image.png" alt="Magic Commit" width="400"/>

`magic-commit` writes your commit messages with AI. 

It's available as a command-line tool currently. There is an experimental VSCode extension in alpha, which you can read about in `Experiments > VSCode Extension` below.

## Table of Contents

- [Installation](#installation)
- [Setup](#setup)
- [Usage](#usage)
- [Experiments](#experiments)
    - [VSCode Extension](#vscode-extension)
    - [Llama2 Model](#llama2-model)
- [Developer Notes](#developer-notes)
    - [Building the Command-Line Tool](#building-the-command-line-tool)
    - [Building the VSCode Extension](#building-the-vscode-extension)
    - [Publishing to PyPI](#publishing-to-pypi)
    - [Unit Tests](#unit-tests)

## Installation

To install the command-line tool, [PyPI](https://pypi.org/project/magic-commit/) is the easiest way:
```bash
pip install magic-commit
```

## Setup

You'll need to set up an OpenAI account and [get an API key](https://platform.openai.com/account/api-keys).

Once you have a key, add it to `magic-commit` like so:
```bash
magic-commit -k <your-key-here>
```

## Usage

Running `magic-commit` is straightforward:
```bash
>>> magic-commit # will run in your current directory
[your commit message] # automatically copied to your clipboard
```

To see all the options, run:
```bash
>>> magic-commit --help

usage: magic-commit [-h] [-d DIRECTORY] [-m MODEL] [-k API_KEY] [--set-model MODEL_NAME] [--no-copy] [--no-load] [-t TICKET] [-s START] [--llama LLAMA]

Generate commit messages with OpenAI’s GPT.

optional arguments:
  -h, --help            show this help message and exit
  -d DIRECTORY, --directory DIRECTORY
                        Specify the git repository directory
  -m MODEL, --model MODEL
                        Specify the OpenAI GPT model
  -k API_KEY, --key API_KEY
                        Set your OpenAI API key
  --set-model MODEL_NAME
                        Set the default OpenAI GPT model
  --no-copy             Do not copy the commit message to the clipboard
  --no-load             Do not show loading message
  -t TICKET, --ticket TICKET
                        Request that the provided GitHub issue be linked in the commit message
  -s START, --start START
                        Provide the start of the commit message
  --llama LLAMA         Pass a localhost Llama2 server as a replacement for OpenAI API
```

For models, note that:
- You need to specify an [OpenAI GPT model](https://platform.openai.com/docs/models).
    - e.g. `gpt-3.5-turbo-0301`, or `gpt-4`
    - There is an experimental mode which uses Meta's Llama2 models instead. 
        - (see `Experiments > Llama2 Model` below)
- Your OpenAI account needs to have access to the model you specify.
    - i.e. Don't specify `gpt-4` if you don't have access to it.

## Experiments

### VSCode Extension

Currently in "alpha" status (v 0.0.3). It works, completely, but we need to address the following:

- [ ] Write automated tests
- [ ] Fix any [known bugs](https://github.com/heyodai/magic-commit/issues?q=is%3Aissue+is%3Aopen+label%3Abug)
- [ ] Write documentation
- [ ] Officially publish to the VSCode Marketplace

### Llama2 Model

Llama2 is a free alternative to OpenAI's `GPT-3.5`, created by Meta (Facebook). A long-term goal of `magic-commit` is to support Llama2 fully, allowing you to use it without needing to pay OpenAI or send any potentially sensitive data to them.

To that end, you can pass a running `localhost` Llama2 server to `magic-commit` like so:
```bash
magic-commit --llama http://localhost:8080 # or whatever port you're using
```

Note that you'll need to have a running Llama2 server. If you're on MacOS, I found [these instructions](https://github.com/abetlen/llama-cpp-python/blob/main/docs/install/macos.md) from the `llama-cpp-python` project fairly easy to follow.

In the future, the end goal is to seamlessly support both OpenAI and Llama2 models, and to allow you to switch between them with a simple flag.

### LoRA Fine-Tuned Model

Llama2 models capable of running on a normal computer have to be fairly small, e.g. 7 billion parameters. This is a lot, but it's a far cry from the 175 billion parameters of OpenAI's `GPT-3.5` model. Performance for this task out-of-the-box is not great.

However, there is hope. Low-Rank Adaptation (LoRA) is a technique for specializing a large model to a smaller one. To quote the [research paper](https://arxiv.org/abs/2106.09685):

> Compared to GPT-3 175B fine-tuned with Adam, LoRA can reduce the number of trainable parameters by 10,000 times and the GPU memory requirement by 3 times. LoRA performs on-par or better than fine-tuning in model quality on RoBERTa, DeBERTa, GPT-2, and GPT-3

I do believe that we can potentially get GPT-3.5 level of quality while running on a laptop. You can see my experiments with this in the `lora-experiments` folder. If you have any ideas or suggestions, please reach out!

## Developer Notes

Please feel free to open a GitHub issue, submit a pull request, or to reach out if you have any questions or suggestions!

### Building the Command-Line Tool

Note: This is referring to a local development build. For production, see `Publishing to PyPI` below.

```bash
cd cli/magic_commit
pip install -e . # install the package in editable mode
```

### Building the VSCode Extension

```bash
cd vscode/magic-commit
npm install vsce # if you don't have it already
vsce package # creates a .vsix file
```

### Publishing to PyPI

To publish a new version to PyPI:
```bash
cd cli/magic_commit
pip install twine wheel
python setup.py sdist bdist_wheel # build the package
twine upload dist/* # upload to PyPI
```

### Unit Tests

To run the unit tests:
```bash
cd cli/magic_commit/tests
pytest
```
