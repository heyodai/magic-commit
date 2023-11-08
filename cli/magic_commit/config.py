import configparser
import os
from logging import Logger  # Just so the linter doesn't complain

CONFIG_FILE = os.path.expanduser("~/.magic_commit_config")


def set_model(model_name: str, log: Logger) -> None:
    pass


def get_model() -> str:
    """
    Get the stored preferred OpenAI GPT model.

    Returns
    -------
    str
        The stored preferred OpenAI GPT model.
    """
    # TODO: Implement this
    # https://github.com/heyodai/magic-commit/issues/16

    # TODO: Add verification that the model is a valid option
    return "gpt-3.5-turbo"


def get_api_key() -> str:
    """
    Get the stored OpenAI API key.

    Returns
    -------
    str
        The stored OpenAI API key.
    """
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE)
    return config.get("DEFAULT", "api_key", fallback=None)


def set_api_key(api_key) -> None:
    """
    Set the OpenAI API key.

    Parameters
    ----------
    api_key : str
        The OpenAI API key.

    Returns
    -------
    bool
        True if the API key was successfully written to the config file.

    Raises
    ------
    OSError
        If the config file could not be written to.
    """
    config = configparser.ConfigParser()
    config["DEFAULT"] = {"api_key": api_key}

    try:
        with open(CONFIG_FILE, "w") as configfile:
            config.write(configfile)
    except OSError:
        raise OSError("Could not write to config file")

    return True
