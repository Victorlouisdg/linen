import setuptools
from setuptools import find_packages

setuptools.setup(
    name="linen",
    version="0.0.1",
    author="Victor-Louis De Gusseme",
    author_email="victorlouisdg@gmail.com",
    description="TODO",
    install_requires=[
        "numpy",
        "scipy",
        "matplotlib",
        "numdifftools",
    ],
    packages=find_packages(),
)
