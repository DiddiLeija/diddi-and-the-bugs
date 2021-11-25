"""
I use Nox here to reformat the code.
"""
import nox


@nox.session(name="keep-codebase-clean")
def keep_codebase_clean(session):
    "Run linters and formatters."
    files = ("noxfile.py", "main.py")
    session.install("black==21.11b1", "flake8==4.0.1", "isort==5.10.1")
    # format
    session.run("isort", *files)
    session.run("black", *files)
    # lint
    session.run("flake8", *files, "--max-line-length=127")
    session.run("isort", "--check-only", *files)
    session.run("black", "--check", *files)
