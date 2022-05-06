import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="nuwinter",
    version="0.0.1",
    author="Robert Stein",
    author_email="rdstein@caltech.edu",
    description="Data reduction pipeline for Nu WINTER",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    keywords="astronomy image WINTER",
    url="https://github.com/robertdstein/nuwinter",
    packages=setuptools.find_packages(),
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
    ],
    python_requires='>=3.8',
    install_requires=[
        "astropy",
        "jupyter",
        "matplotlib",
        "numpy",
        "nuztf",
        "pandas",
        "wintertoo==0.1.0"
    ]
)
