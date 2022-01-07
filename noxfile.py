"""
I use Nox here to reformat the code.
"""
import nox

deps = ["black==21.11b1", "flake8==4.0.1", "isort==5.10.1"]
files = ["noxfile.py", "main.py"]


@nox.session(name="keep-codebase-clean")
def keep_codebase_clean(session):
    "Run formatters."
    session.install(*deps)
    session.run("isort", *files)
    session.run("black", *files)


@nox.session(name="check-quality")
def check_quality(session):
    "Check the style and quality."
    session.install(*deps)
    session.run("flake8", *files, "--max-line-length=127")
    session.run("isort", "--check-only", *files)
    session.run("black", "--check", *files)
