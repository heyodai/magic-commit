from setuptools import setup

setup(
    name="magic-commit",
    version="0.2.0",
    packages=["magic_commit"],
    install_requires=[
        "openai",
    ],
    entry_points={
        "console_scripts": [
            "magic-commit = magic_commit.__main__:main",
        ],
    },
)
