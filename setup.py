import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="modeltestSDK",
    use_scm_version=True,
    setup_requires=['setuptools_scm'],
    install_requires= [
        aiohttp==3.6.2
    async-timeout==3.0.1
    atomicwrites==1.4.0
    attrs==19.3.0
    certifi==2020.6.20
    chardet==3.0.4
    colorama==0.4.3
    coverage==5.1
    cycler==0.10.0
    databases==0.3.2
    idna==2.9
    importlib-metadata==1.6.1
    kiwisolver==1.2.0
    matplotlib==3.1.1
    more-itertools==8.4.0
    multidict==4.7.6
    numpy==1.19.0
    packaging==20.4
    pandas==0.25.3
    pluggy==0.13.1
    py==1.8.2
    pyparsing==2.4.7
    pytest==5.4.3
    pytest-cov==2.8.1
    python-dateutil==2.8.1
    pytz==2020.1
    requests==2.24.0
    six==1.15.0
    SQLAlchemy==1.3.18
    urllib3==1.25.9
    wcwidth==0.2.5
    yarl==1.4.2
    zipp==3.1.0
    qats==4.8.1
    ],
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
