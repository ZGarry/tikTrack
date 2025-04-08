import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="tikTrack",
    version="0.1.0",
    author="kezhuanzhai",
    author_email="your.email@example.com",
    description="A simple performance tracking and visualization tool for Python applications",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/tikTrack",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "pandas>=1.0.0",
        "matplotlib>=3.0.0",
    ],
) 