# BotAQ
BotAQ is a bot made to grind Am-Boss in Adventure Quest. It utilises the PyAutoGUI library to simulate human input and perform template matching. Unfortunately, this was not made with versatility in mind, as it requires the user to reach certain specific conditions within the game. 

## How it works
BotAQ is based on three fundamental steps.

### Finding Am-Boss
A template matcher looks for Am-Boss and challenges it.

### Prepare
A one-time preparationary phase is engaged to identify if the user has utilised specific abilities/equipments. 

### Attack
An attack is performed on Am-Boss and checked if Am-Boss is killed for every attack. If Am-Boss is not killed, the function is repeated.

### Repeat
If Am-Boss is killed, the steps are repeated without the preparationary phase. This stops when the maximum daily limit of fighting Am-Boss is reached.
