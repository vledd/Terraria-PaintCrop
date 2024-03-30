# Terraria PaintCrop

![Logo](./resources_internal/splash_1.jpg)

[![License](https://img.shields.io/badge/License-MIT-Color?style=flat&color=%23a83281)](https://github.com/git/git-scm.com/blob/main/MIT-LICENSE.txt)
![Static Badge](https://img.shields.io/badge/Made-with_love-violet)
![Static Badge](https://img.shields.io/badge/Platforms-Any-cyan)

# What is this
Terraria PaintCrop is a little crossplatform piece of software written
in Python that enables users to quickly modify tilesets extracted from
the game.

It works with any tileset but best with non-block tilesets (more that 1x1 tile size).

# Installation
## Using pre-built package

You can use our precompiled releases but please note that they 
will be threaten as malware and will update not so often, so 
proceed if you want a stable version without the need to build.

For the newest untested updates building from sources is required.

## Building from sources
Since this software was created only with power of energetic drinks and big enthusiasm,
we cannot sign resulting packages, so Win Defender and any other similar software will
treat it as a malware. Thus, building from sources is preferred.

You can easily do it using the Python functionality.

### Pre-requisites (Skippable)
You may encounter some errors while building, so probably you want to do some steps first.

#### Windows
1. Step 2 may fail because your Windows Policy will not allow to run .ps1 scripts to 
activate venv. In that case, open PowerShell as Admin and enter 
`Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope LocalMachine` to run such scripts.
Reopen terminal (you can now run it as non-admin).

activate.ps1 is a script written by Python devs, not us, so it's completely safe to allow its execution.

#### MacOS (In development since there is no Macs in team)

#### Linux

1. Pyinstaller may fail because no Python devel packages are installed.
In that case run `sudo apt install python-dev` or `sudo apt install python3-dev` to fix it.

### Actual building

0. Auto build scripts are coming soon.
1. Clone the repository (usually it will be the ``main`` branch)
2. Better create a separate [virtual environment](https://docs.python.org/3/library/venv.html) for this project 
(Python 3.10+ as main installation is preferred).
For example, enter the project folder and type
```
mkdir venv
python -m venv ./venv/

# FOR WINDOWS ONLY
cd venv/Scripts
./activate.ps1
# END WINDOWS

# FOR LINUX AND MAC
source venv/bin/activate
# END LINUX AND MAC

cd ../../
```
3. Execute `pip install -r requirements_build.txt` to get all the packages needed for building.
4. Execute `pyinstaller --onefile --noconsole --add-data=./resources_internal:resources_internal src/app.py` to build the ELF or EXE file.
Path may to resources_internal (before ":" may vary depending on the platform)
5. Find your executable file in `dist` folder and run it

# Operation

TODO for now use your heart to operate this software.

# Editing the program

At least for March 2024, pyqt6 tools are too outdated for new PyQt6.
Thus, for release verions, to have dark mode etc, we are using different requirements file.

If you want to edit this program using Qt Designer etc, please install `requirements_edit.txt` in your venv.