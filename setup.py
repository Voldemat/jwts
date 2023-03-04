from pathlib import Path

from setuptools import setup  # type: ignore [import]

from version import get_git_tag


setup(
    name="jwts",
    version=get_git_tag(),
    description="Set of abstractions for jwt tokens based on pyjwt[crypto].",
    author="Vladimir Vojtenko",
    author_email="vladimirdev635@gmail.com",
    license="MIT",
    packages=["jwts"],
    install_requires=["pyjwt[crypto]"],
    package_data={"jwts": ["py.typed"]},
    long_description=(Path(__file__).parent / "README.md").read_text(),
    long_description_content_type="text/markdown",
)
