"""
I use Nox here to reformat the code, check
the code quality, and build the zipped distributions.
"""

import glob
import os
import sys

import nox

nox.options.sessions = ["format", "lint"]

files = ["noxfile.py", "main.py", "setup.py"]


@nox.session
def format(session):
    "Run formatters."
    session.install("-r", "test-requirements.txt")
    session.run("ruff", "check", *files, "--fix")
    session.run("ruff", "format", *files)


@nox.session
def lint(session):
    "Check the style and quality."
    session.install("-r", "test-requirements.txt")
    session.run("ruff", "check", *files)


@nox.session
def package(session):
    "Build and package everything up."
    # First of all, install the requirements
    session.install("-r", "requirements.txt")
    # Find all the resource files (using the skin packs spec from 'main.py')
    res_files = glob.glob("resource_*.pyxres")
    # Look for the 'dist' path, that will store everything
    session.warn("Looking for the destination path...")
    dist_generation = "import os; os.mkdir('./dist')"
    if os.path.exists("./dist"):
        if input(
            "The destination directory ('./dist') already exists. Do you want to remove it? (y/n) "
        ).strip().lower() not in ("y", "yes"):
            session.warn("Aborting...")
            quit()
        dist_generation = (
            "import os, shutil; shutil.rmtree('./dist'); os.mkdir('./dist')"
        )
    session.run("python", "-c", dist_generation)
    # Zip the source code
    session.warn("Generating the source code distribution...")
    session.run(
        "python",
        "-c",
        "import os, shutil; shutil.copy('main.py', './dist/main.py'); ",
    )
    for i in res_files:
        session.run(
            "python",
            "-c",
            f"import os, shutil; shutil.copy('{i}', './dist/{i}')",
        )
    zfiles = ["./dist/source.zip", "./dist/main.py"] + [
        f"./dist/{i}" for i in res_files
    ]
    session.run(
        "python",
        "-m",
        "zipfile",
        "-c",
        *zfiles,
    )
    # Generate and zip the Pyxel executable
    session.warn("Generating the Pyxel executable...")
    session.cd("dist")
    session.run("pyxel", "package", ".", "main.py")
    session.cd("..")
    session.run(
        "python",
        "-c",
        "import os; os.rename('./dist/dist.pyxapp', './dist/pyxel_dist.pyxapp')",
    )
    session.run(
        "python",
        "-m",
        "zipfile",
        "-c",
        "./dist/pyxel_dist.zip",
        "./dist/pyxel_dist.pyxapp",
    )
    # Generate an HTML using Pyxel's provided strategy
    session.warn("Generating the HTML file...")
    session.cd("dist")
    session.run("pyxel", "app2html", "pyxel_dist.pyxapp")
    session.run(
        "python", "-c", "import os; os.rename('./pyxel_dist.html', './html_dist.html')"
    )
    session.run("python", "-m", "zipfile", "-c", "./html_dist.zip", "./html_dist.html")
    session.cd("..")
    # If Windows, create the cx_Freeze executable
    if sys.platform == "win32":
        session.warn("Running in Windows, generating the cx_Freeze executable...")
        session.install("-r", "requirements-win32.txt")
        session.run("python", "setup.py", "build")
        for i in res_files:
            session.run(
                "python",
                "-c",
                "import os, shutil; exe_path = os.listdir('./build')[0]; "
                f"shutil.copy2('{i}', "
                "f'./build/{exe_path}/"
                f"{i}')",
            )
        session.run("python", "-m", "zipfile", "-c", "./dist/windows.zip", "./build")
    else:
        # It's polite to notify when a step is ignored... well, that's what I think.
        session.warn(
            "Not running in Windows, ignoring the cx_Freeze executable build..."
        )
    # Before closing, it's cleanup time!
    session.warn("Cleaning up the excedents...")
    session.run(
        "python",
        "-c",
        "import os; os.remove('./dist/main.py'); "
        "os.remove('./dist/pyxel_dist.pyxapp'); os.remove('./dist/html_dist.html')",
    )
    for i in res_files:
        session.run(
            "python",
            "-c",
            f"import os; os.remove('./dist/{i}')",
        )
    if os.path.exists("./build"):
        session.run("python", "-c", "import shutil; shutil.rmtree('./build')")
    # Send a success message
    session.warn("All done! The contents are ready at './dist'.")
