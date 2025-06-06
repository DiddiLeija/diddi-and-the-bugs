# Contribution guide to _Diddi and the Bugs_

[![Nox](https://img.shields.io/badge/%F0%9F%A6%8A-Nox-D85E00.svg)](https://github.com/wntrblm/nox)
[![License](https://img.shields.io/github/license/DiddiLeija/diddi-and-the-bugs)](https://github.com/DiddiLeija/diddi-and-the-bugs)
[![GitHub](https://img.shields.io/github/v/release/DiddiLeija/diddi-and-the-bugs?logo=github&sort=semver)](https://github.com/DiddiLeija/diddi-and-the-bugs)

[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/G2G3AL6D6)

This is an open source project, so contributors are totally welcome! We've added here a short guide to contribute, and a few extra suggestions.

## License

This project is licensed under the [MIT License](https://github.com/DiddiLeija/diddi-and-the-bugs/blob/main/LICENSE). Take that in count when making contributions.

## Issues and pull requests

At GitHub, we have an issue tracker. You can use it to report bugs, request new features, etc. It is recommended to open an issue before
sending a pull request, so we can discuss your ideas first and discard possible false-positives / unfitting requests.

## Getting started with code contributions

### Fork this repo

We suggest you to fork [this game's repository](https://github.com/DiddiLeija/diddi-and-the-bugs) on your GitHub account,
and create a branch that would get merged on the original repo. You can do all this on GitHub online.

**Please don't try to create branches on the main repository**.

### Get the code

Once you have a fork, you can clone the fork locally by running this command:

```sh
git clone https://github.com/{your-gh-username}/diddi-and-the-bugs
cd diddi-and-the-bugs
```

After that, you can open branches, push commits, and everything you need to start contributing.

### Get the tools

You will need some additional stuff before getting started:

- [Python](https://python.org) (version 3.7 or higher)
- [Nox](https://nox.thea.codes), for running linters and formatters, and some other useful commands we've set up
- [Pyxel](https://github.com/kitao/pyxel): you can either install the `requirements.txt` file (suggested method), or the version pinned on that file using [these instructions](https://github.com/kitao/pyxel#how-to-install)

Also, you may want to set up a Python-oriented virtual environment for installing the packages (Nox, Pyxel), but of course that's optional.

### Run linters and checks

We use several formatters/linters \(listed [here](https://github.com/DiddiLeija/diddi-and-the-bugs/blob/main/test-requirements.txt)\) for keeping
the code quality civilized. On GitHub, an automated action will do it for you, but in a local clone, you can use Nox to run them by yourself.

Just run this command in the root directory of the repository:

```sh
nox
```

This will run formatters (code-fixers), and then the linters (quality-checkers). Most issues should be resolved by the formatters (as they tend to be small style mistakes), but you may find issues after linting. You can run Nox as many times as you need, anytime. This prevents you from pushing a commit with potential mistakes, and you can fix mistakes before GitHub Actions goes mad online ;)

### Building the zipped distribution by yourself

Since version 2.0.0, you can get these distributions at a `dist/` folder. To generate them, run this command with Nox:

```sh
nox -s package
```

This will trigger the following steps of the build:

- **Zip version**: Just compress the source code into an elegant ZIP file.
- **Pyxel version**: A Pyxel executable.
- **HTML version**: A standalone HTML to run the game without extra tools, offline!
- **Windows version** [^1]: A Windows executable (`.exe`), a bit heavier than other versions but functional as a desktop app.

If these four steps finish correctly [^1] you'll be able to see the packed results on a `dist` folder, in the main tree of the repo.

[^1]: Please note this step only works on Windows devices. If the Nox task detects you're not using Windows, this step will just get skipped.
