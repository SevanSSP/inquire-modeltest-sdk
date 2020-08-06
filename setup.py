import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="modeltestSDK",
    use_scm_version=True,
    setup_requires=['setuptools_scm'],
    author="Jørgen",
    author_email="jen@sevanssp.com",
    description="Python SDK for inquire-modeltest",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/SevanSSP/inquire-modeltest-sdk",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6.9',
)
