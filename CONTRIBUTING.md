# Contributing to _Diddi and the Bugs_

[![Nox](https://img.shields.io/badge/%F0%9F%A6%8A-Nox-D85E00.svg)](https://github.com/wntrblm/nox)
[![License](https://img.shields.io/github/license/DiddiLeija/diddi-and-the-bugs)](https://github.com/DiddiLeija/diddi-and-the-bugs)
[![GitHub](https://img.shields.io/github/v/release/DiddiLeija/diddi-and-the-bugs?logo=github&sort=semver)](https://github.com/DiddiLeija/diddi-and-the-bugs)

[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/G2G3AL6D6)

This is an open source project, so contributors are welcome. We have added here a short guide to contribute, and a few suggestions.

## License

This project is licensed under the [MIT License](https://github.com/DiddiLeija/diddi-and-the-bugs/blob/main/LICENSE).

## Issues and pull requests

At GitHub, we enabled the issue tracker. You can use it for reporting bugs, requesting new features, etc. It is recommended to open an issue before
sending a pull request, so we can discuss your ideas first and discard possible false-positives and unfitting requests.

## Getting started with code contributions

### Fork this repo

We suggest you to fork [this game's repository](https://github.com/DiddiLeija/diddi-and-the-bugs) on your GitHub account,
and create a branch that would get merged on the original repo. You can do all this on GitHub.

### Get the code

Once you have a fork of the main repository, and you have
installed Git on your device, you can clone the fork locally by running this command:

```sh
git clone https://github.com/{your-gh-username}/diddi-and-the-bugs
cd diddi-and-the-bugs
```

After that, you can open branches, push commits, and everything you need to get your contribution done.

### Get the tools

You will need some additional stuff before getting started:

- [Python](https://python.org) (version 3.7 or higher)
- [Nox](https://nox.thea.codes), for running linters and formatters, and some other useful commands we've set up
- [Pyxel](https://github.com/kitao/pyxel) (you can both install the `requirements.txt` file,
  or the version pinned on that file using [this instructions](https://github.com/kitao/pyxel#how-to-install))

Also, you may want to set up a virtual environment for installing the packages (except Python), but that's optional.

### Run linters and checks

We use several formatters/linters \(listed [here](https://github.com/DiddiLeija/diddi-and-the-bugs/blob/main/test-requirements.txt)\) for keeping
the code quality civilized. On GitHub, an automated action will do it for you, but in a local clone, you can use Nox to run them by yourself.

Just run this command in the root directory of the repository:

```sh
nox
```

This will run formatters, and then the linters. Most of the issues should be resolved by the formatters, but you may find issues after linting. You
can run Nox as many times as you need, anytime.

### Building the zipped distribution by yourself

Since version 2.0.0, you can get these distributions at a `dist/` folder. To generate them, run this command with Nox:

```sh
nox -s package
```
