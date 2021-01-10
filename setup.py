import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()
    
setuptools.setup(
    name = "legcop",
    version = "0.0.5",
    author = "James Tollefson",
    author_email = "james.l.tollefson@alaskaupdate.com",
    description = "API utilities to access legislative information from across the 54 U.S. States and Territories",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = "https://github.com/jamestollefson/legcop",
    packages = setuptools.find_packages(),
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        ],
    python_requires = '>=3.6',
    )