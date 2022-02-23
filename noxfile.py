"""
I use Nox here to reformat the code.
"""

import os
import sys

import nox

nox.options.sessions = ["keep-codebase-clean", "check-quality"]

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


@nox.session(name="create-packages")
def create_packages(session):
    "Build and package everything up."
    # First of all, install the requirements
    session.install("-r", "requirements.txt")
    # Look for the 'dist' path, that will store everything
    session.warn("Looking for the destination path...")
    dist_generation = "import os; os.mkdirs('./dist')"
    if os.path.exists("./dist"):
        if not input(
            "The destination directory ('./dist') already exists. Do you want to remove it? (y/n)"
        ).strip().lower() not in ("y", "yes"):
            session.warn("Aborting...")
            quit()
        dist_generation = (
            "import os, shutil; shutil.rmtree('./dist'); os.mkdirs('./dist')"
        )
    session.run("python", "-c", dist_generation)
    # Zip the source code
    session.warn("Generating the source code distribution...")
    session.run(
        "python",
        "-c",
        "import os, shutil; shutil.copy('main.py', './dist/main.py'); "
        "shutil.copy('resource.pyxres', './dist/resource.pyxres')",
    )
    session.run(
        "python",
        "-m",
        "zipfile",
        "-c",
        "./dist/source.zip",
        "./dist/main.py",
        "./dist/resource.pyxres",
    )
    # Generate and zip the Pyxel executable
    session.warn("Generating the Pyxel executable...")
    session.run("pyxel", "package", "./dist/", "./dist/main.py")
    session.run(
        "python",
        "-c",
        "import os; os.rename('./dist/main.pyxapp', './dist/pyxel_dist.pyxapp')",
    )
    session.run(
        "python",
        "-m",
        "zipfile",
        "-c",
        "./dist/pyxel_dist.zip",
        "./dist/pyxel_dist.pyxapp",
    )
    # If Windows, create the cx_Freeze executable
    if sys.platform == "win32":
        session.warn("Running in Windows, generating the cx_Freeze executable...")
        session.install("cx_Freeze")
        session.run("python", "setup.py", "build")
        session.run("python", "-m", "zipfile", "-c", "./dist/windows.zip", "./build")
    # Before closing, it's cleanup time!
    session.warn("Cleaning up the excedents...")
    session.run(
        "python",
        "-c",
        "import os, shutil; os.remove('./dist/main.py'); os.remove('./dist/resource.pyxres'); "
        "if os.path.exists('./build'): shutil.rmtree('./build')",
    )
    # Send a success message
    session.warn("All done! The contents are ready at './dist'.")
