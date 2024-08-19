import setuptools


with open("README.md", "r", encoding="utf-8") as file:
    long_description = file.read()


setuptools.setup(
    name="pubmed_api",
    version="2.1.3",
    author="Shivam Singh",
    author_email="shivam221098@gmail.com",
    description="Runs PubMed search strings over pubmed API using a batch logic",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/shivam221098/pubmed-api-v1",
    packages=["pubmed_api"],
    install_requires=[
        "xmltodict",
        "requests"
    ]
)
