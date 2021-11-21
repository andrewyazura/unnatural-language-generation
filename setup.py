from setuptools import setup, find_packages

setup(
    name="unnatural-language-generation",
    version="3.0.0",
    packages=find_packages(),
    include_package_data=True,
    entry_points={"console_scripts": ["ulg = text_generator.scripts.cli:cli"]},
)
