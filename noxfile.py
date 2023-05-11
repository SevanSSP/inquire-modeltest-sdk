import nox
import tempfile
import os

# override default sessions
nox.options.sessions = ["lint", "tests"]


@nox.session
def lint(session):
    """Highlight syntactical and stylistic problems in the code."""
    session.install("flake8")
    session.run(
        "flake8",
        "modeltestSDK/",
        "--count",
        "--select=E9,F63,F7,F82",
        "--show-source",
        "--statistics",
    )
    session.run(
        "flake8",
        "modeltestSDK/",
        "--count",
        "--exit-zero",
        "--max-complexity=10",
        "--max-line-length=127",
        "--statistics",
    )


@nox.session
def tests(session):
    """Run test suite."""
    # install dependencies
    req_path = os.path.join(tempfile.gettempdir(),'requirements.txt')
    session.install("poetry")

    session.run(
        "poetry",
        "export",
        "--dev",
        "--format=requirements.txt",
        f"--output={req_path}",
        external=True,
    )
    session.install("-r", req_path)


    session.install("pytest")
    session.install("requests")
    session.install("coverage")

    # unit tests
    session.run("coverage", "run", "--source", "modeltestSDK", "-m", "pytest")
    session.notify("cover")


@nox.session
def cover(session):
    """Analyse and report test coverage."""
    session.install("coverage")
    # TODO: Add "--fail-under=99" once test coverage is improved
    session.run("coverage", "report", "--show-missing")
    session.run("coverage", "erase")


@nox.session
def blacken(session):
    """Run black code formatter."""
    session.install("black", "isort")
    files = ["modeltestSDK", "tests", "noxfile.py"]
    session.run("black", *files, "--diff", "--color")
    session.run("isort", *files, "--diff")
