import setuptools


with open("README.md", "r", encoding="utf-8") as file:
    long_description = file.read()


setuptools.setup(
    name="pubmed_api",
    version="1.0.0",
    author="Shivam",
    author_email="shivam@visfo.health",
    description="Runs PubMed search strings over pubmed API using a batch logic",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/shivam221098/pubmed-api-v1.git",
    packages=["pubmed_api"],
    install_requires=[
        "xmltodict",
        "requests"
    ]
)
