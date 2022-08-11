from setuptools import setup

setup(
    name="unnatural-language-generation",
    version="4.0.0",
    author="Andrew Yatsura",
    url="https://github.com/andrewyazura/unnatural-language-generation",
    packages=["text_generator"],
    install_requires=["click", "networkx", "tokenize-uk"],
    entry_points={"console_scripts": ["textgen = cli:cli"]},
)
