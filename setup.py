import json

from setuptools import setup  # type: ignore

with open("Pipfile.lock", "r") as file:
    pipfile_lock = json.load(file)

setup(
    name="jwts",
    version="0.0.1",
    description="Set of abstractions for jwt tokens based on pyjwt[crypto].",
    author="Vladimir Vojtenko",
    author_email="vladimirdev635@gmail.com",
    license="MIT",
    packages=["jwts"],
    install_requires=list(
        map(
            lambda package: package[0] + package[1]["version"],  # type: ignore
            pipfile_lock["default"].items(),
        )
    ),
    package_data={"jwts": ["py.typed"]},
)
