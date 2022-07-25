# BotAQ

[![Total alerts](https://img.shields.io/lgtm/alerts/g/winstxnhdw/BotAQ.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/winstxnhdw/BotAQ/alerts/)
[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/winstxnhdw/BotAQ.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/winstxnhdw/BotAQ/context:python)

BotAQ is a CLI bot made to grind bosses in Adventure Quest. It utilises the PyAutoGUI library to simulate human input and perform template matching. Unfortunately, this was not made with versatility in mind, as it requires the player to reach certain specific conditions within the game.

<div align="center">
  <img src="resources/terminal.gif" \>
</div>

## Install

We will install the dependencies in a Python virtual environment to avoid polluting the global environment.

```bash
python -m venv venv
```

Then we will activate the virtual environment in our shell. For Windows, execute the following commands.

```ps1
venv\Scripts\activate
```

If you are on Linux, you should prepend the `source` command like so.

```bash
source venv/Scripts/activate
```

You may install the dependencies once you have activated the virtual environment.

```bash
pip install -r requirements.txt
```

## Usage

```bash
python main.py
```

## Custom Bosses

Save a screengrab template of the boss you have chosen and save it into the templates folder

<div align="center">
  <img src="resources/snipping.gif" \>
</div>

## How it works

BotAQ is based on five fundamental steps.

<div align="center">
  <img src="resources/flowchart.png" \>
</div>

### Finding the Boss

A template matcher looks for the selected boss and challenges it.

### Prepare

The preparationary phase is only engaged once per battle. This is used to cast semi-permanent buffs on the player.

### Attack

An attack is performed on the boss and checked if it is killed for every attack. If the boss is not killed, the function is repeated.

### Repeat

If the boss is killed, the steps are repeated without the setting the loadout again. This cycle eventually stops when the maximum daily limit of fighting the boss is reached. Player has the choice whether to keep last experience points gained from previous sessions.
