import configparser
import os
from logging import Logger  # Just so the linter doesn't complain

CONFIG_FILE = os.path.expanduser("~/.magic_commit_config")


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


def set_api_key(api_key, log: Logger) -> None:
    """
    Set the OpenAI API key.

    Parameters
    ----------
    api_key : str
        The OpenAI API key.
    """
    config = configparser.ConfigParser()
    config["DEFAULT"] = {"api_key": api_key}
    with open(CONFIG_FILE, "w") as configfile:
        config.write(configfile)

    log.info("API key set successfully.")
