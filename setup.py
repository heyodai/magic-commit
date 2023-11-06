from setuptools import setup, find_packages

# Read in the README.md for the long description.
with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="magic-commit",
    version="0.3.0",
    packages=find_packages(),
    include_package_data=True,  # This line is needed to include non-code files
    package_data={
        "": ["*.jinja", "*.jinja2", "*.html"],
        "magic_commit": ["templates/*.html", "templates/*.jinja", "templates/*.jinja2"],
    },
    install_requires=["openai", "jinja2", "dagwood"],
    author="Odai Athamneh, Rahul Mysore",
    author_email="heyodai@gmail.com, rmf9t@umkc.edu",
    entry_points={
        "console_scripts": [
            "magic-commit = magic_commit.__main__:main",
        ],
    },
    description="Generate commit messages with OpenAI\’s GPT.",
    long_description_content_type="text/markdown",
    url="https://github.com/heyodai/magic-commit",
)
