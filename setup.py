from setuptools import setup, find_packages
from codecs import open

REPO_URL = "https://github.com/mandarons/library-name"
VERSION = "0.3.1"

with open("README.md", "r") as fh:
    long_description = fh.read()
with open("requirements.txt", "r") as fh:
    required = fh.read().splitlines()

setup(
    name="library-name",
    version=VERSION,
    author="Mandar Patil",
    author_email="mandarons@pm.me",
    # TODO: update description
    description="Python library to ...",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=REPO_URL,
    package_dir={".": ""},
    packages=find_packages(exclude=["tests"]),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=required,
    # TODO remove if there is no entry point
    entry_points="""
    [console_scripts]
    icloud=library-name.cmdline:main
    """,
)
