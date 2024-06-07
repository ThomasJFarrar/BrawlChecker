
# Brawl Checker Discord Bot
## Introduction
This Discord Bot, known as the Brawl Checker, has been developed to offer club owners in the mobile game Brawl Stars a convenient way within Discord to verify if players meet the necessary requirements to join their club. The bot will only work for one discord server at a time.
## Prerequisites
**python 3.11.4** was used for the development of the Brawl Checker bot. To run you will need Python as well as the requests and discord.py libraries installed for the bot to run.

You will need an API key for the Brawl Stars API which you can get for free from https://developer.brawlstars.com/. Register, then copy your API key into the `brawlchecker.py` file on line 9.

You will also need to set up the discord bot on the Discord Developer Portal which you can do for free at https://discord.com/developers/applications. You will need to get a bot token and copy it into the `brawlchecker.py` file on line 7. You will need to invite the bot to your discord server.
## Getting Started
To get started with the Brawl Checker, run `brawlchecker.py`. The bot should come online on your Discord server.
### Setting the Requirements
On your Discord server you can use the following commands to use the bot:
* `!setclub <clubtag>` sets the club. This will automatically set the minimum trophies required.
* `!setminmaxedbrawlers <number>` sets the minimum number of maxed brawlers the player needs. The player must have at least a two gears, a star power and gadget.
* `!setmin3v3wins <number>` sets the minimum number of 3 vs 3 wins the player needs.
### Checking Players
* `!checkplayer <playertag>` checks if the player meets the club requirements that have been set.
## Known Issues
* Currently no known issues
## Author
* **Thomas Farrar** - Discord: Slamtom
## License
This project is licensed under the MIT License - see `LICENSE` for more details.
