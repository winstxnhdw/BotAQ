# BotAQ
BotAQ is a bot made to grind Am-Boss in Adventure Quest. It utilises the PyAutoGUI library to simulate human input and perform template matching. Unfortunately, this was not made with versatility in mind, as it requires the player to reach certain specific conditions within the game. 

## Usage
1. `pip install -r requirements.txt`

2. `python main.py -b <boss-name>`

e.g. 
```
python main.py -b amboss
```

## How it works
BotAQ is based on five fundamental steps.

### Finding Am-Boss
A template matcher looks for Am-Boss and challenges it.

### Set Loadout
A one-time phase to permanently set the player's loadout is engaged to identify if the player has utilised specific abilities/equipments. This is to ensure that the boss is killing Am-Boss as efficiently as possible.

### Prepare
The preparationary phase is only engaged once per battle. This is used to cast semi-permanent buffs on the player.

### Attack
An attack is performed on Am-Boss and checked if Am-Boss is killed for every attack. If Am-Boss is not killed, the function is repeated.

### Repeat
If Am-Boss is killed, the steps are repeated without the setting the loadout again. This cycle eventually stops when the maximum daily limit of fighting Am-Boss is reached. Player has the choice whether to keep last exp gained

## Future Works
There may be plans to use a Optical Character Recognition (OCR) engine or deep-learning model to recognise certain texts and improve the versatility of this project. There are plans to switch to the game's timezone for easier saving of user data.
