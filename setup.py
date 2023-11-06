from setuptools import setup, find_packages

setup(
    name="magic-commit",
    version="0.2.0",
    packages=find_packages(),
    include_package_data=True,  # This line is needed to include non-code files
    package_data={
        "": ["*.jinja", "*.jinja2", "*.html"],
        "magic_commit": ["templates/*.html", "templates/*.jinja", "templates/*.jinja2"],
    },
    install_requires=["openai", "jinja2", "dagwood"],
    entry_points={
        "console_scripts": [
            "magic-commit = magic_commit.__main__:main",
        ],
    },
)
