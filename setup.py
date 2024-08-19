from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="pishockpy",
    version="0.0.4",
    author="Ralf Rademacher",
    description="Control a PiShock via the API.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/UWUplus/pishockpy",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    keywords='pishock',
    install_requires=['requests'],
    packages=find_packages(exclude=['tests']),
)