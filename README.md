# Terraria PaintCrop

[![License](https://img.shields.io/badge/License-MIT-Color?style=flat&color=%23a83281)](https://github.com/git/git-scm.com/blob/main/MIT-LICENSE.txt)
![Static Badge](https://img.shields.io/badge/Made-with_love-violet)
![Static Badge](https://img.shields.io/badge/Platforms-Any-cyan)

# What is this
Terraria PaintCrop is a little crossplatform piece of software written
in Python that enables users to quickly modify tilesets extracted from
the game.

It works with any tileset but best with non-block tilesets (more that 1x1 tile size).

# Installation
## Building from sources
Since this software was made only on energetics and big enthusiasm,
we cannot sign packages, so Win Defender and any other software will
treat it as a malware. Thus, building from sources is preferred.

You can easily do it using the Python functionality.

1. Clone the repository (usually it will be the ``main`` branch)
2. Better create a separate [virtual environment](https://docs.python.org/3/library/venv.html) for this project 
(Python 3.10+ as main installation is preferred)
3. Execute `pip install -r requirements.txt` to get all the packages needed.
4. Execute `pyinstaller --onefile --noconsole --add-data=./resources_internal:resources_internal src/app.py` to build the ELF or EXE file.
Path may to resources_internal (before ":" may vary depending on the platform)
5. Find your executable file in `dist` folder and run it

## Using pre-built package

You can use our precompiled releases but please note that they 
will be threaten as malware and will update not so often, so 
proceed if you want a stable version without the need to build.

# Operation

TODO for now use your heart to operate this software.