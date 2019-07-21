import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="TinderBot",
    version="0.0.1",
    author="Hosam Fikry",
    author_email="hfikry92@gmail.com",
    description="A small example package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/hfikry92/TinderBot",
    packages=setuptools.find_packages(),

)