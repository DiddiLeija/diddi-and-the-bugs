"""
I use Nox here to reformat the code.
"""
import nox

files = ["noxfile.py", "main.py", "setup.py"]


@nox.session(name="keep-codebase-clean")
def keep_codebase_clean(session):
    "Run formatters."
    session.install("-r", "test-requirements.txt")
    session.run("isort", *files)
    session.run("black", *files)


@nox.session(name="check-quality")
def check_quality(session):
    "Check the style and quality."
    session.install("-r", "test-requirements.txt")
    session.run("flake8", *files, "--max-line-length=127")
    session.run("isort", "--check-only", *files)
    session.run("black", "--check", *files)
