from pipenv import find_install_requires  # type: ignore [import]

from setuptools import setup  # type: ignore [import]


setup(
    name="jwts",
    version="0.0.1",
    description="Set of abstractions for jwt tokens based on pyjwt[crypto].",
    author="Vladimir Vojtenko",
    author_email="vladimirdev635@gmail.com",
    license="MIT",
    packages=["jwts"],
    install_requires=find_install_requires(),
    package_data={"jwts": ["py.typed"]},
)
