# Diddi and the Bugs

[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/G2G3AL6D6)

My Game Off 2021 entry.

## Introduction

> The Earth is under invasion. A fleet of giant bugs, bacteria, and viruses are
> outside of the planet.
>
> In the meantime, Diddi was developing a secret spacecraft. When his frineds told him of
> the invasion, he decided to visit the brilliant Dr. Chuck (a scientist, and also
> an old friend of Diddi). The doctor gave him the **L1-F3** experimental serum, that kills anything
> alive. That should destroy those bugs...
>
> To ensure that those bugs will be destroyed, Diddi modified his spacecraft to convert it into a
> starfighter that energizes the serum and shoot it. Then, he named the starfighter **Willpower**.
> Suddendly, the Willpower goes outside of the planet, to start the fight...

## Installation

Since the GameOff 2021 event is hosted by [itch.io](https://itch.io), the distributions are available there. The source
code lives in this GitHub repository, but the stable distributions are available at itch.io.

The itch.io page for my game is here: https://diddileija.itch.io/diddi-and-the-bugs.

Once you are there, read the installation instructions and find the right distribution for you.
If you don't find what you expected, feel free to open an issue on GitHub (or comment in the itch.io page).

### Python version

If you will use Python get sure to have **Python >= 3.8**.

### Building the zipped distributions by yourself

_New since 2.0.0_.

If you have a local clone of this repo, you can build the zipped distributions (those that we distribute on itch.io),
If you have [Nox](https://nox.thea.codes) and the Python required version (see above), run `nox -s create-packages`. It will run a lot
of commands to generate the source zip, the Pyxel executable and the Windows executable (if running under Windows). The final
contents will be found on a `dist` folder [^1].

## How to win

Use the energized serum to destroy **200 bugs** and win! In the meantime, you can earn extra points
by destroying space trash. **Try to get all the points as you can!**

Read the [game guide](https://github.com/DiddiLeija/diddi-and-the-bugs/blob/main/guide.md) for more information (and maybe a few hints!).

## Game engine

This game is made using [Pyxel](https://github.com/kitao/pyxel), a Python tool for retro games. The executables are uploaded to the itch.io page manually
each time a tag (release) is published here.

## Contributing

Read [this contributing guidelines](https://github.com/DiddiLeija/diddi-and-the-bugs/blob/main/CONTRIBUTING.md) for full details.

## More resources

### Discord server

There's a Discord server where you can ask and share stuff related to Diddi and The Bugs! Check out https://github.com/DiddiLeija/diddi-and-the-bugs/issues/45
for full details.

### Wiki

We have a wiki to keep some tips, records, and that stuff. It can be found [at the GitHub repo's wiki](https://github.com/DiddiLeija/diddi-and-the-bugs/wiki).

[^1]: Contributor's advice: This folder is ignored by Git, so it won't be shown on GitHub.
