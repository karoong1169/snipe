# Welcome

This repo houses the code and information necessary for you to host your own version of SnipeBot.

## Update 9/14/21

The future of this project is up in the air currently, as discord.py no longer has a maintainer and, at least at the time of writing, has not been forked. Furthermore, Discord is phasing out legacy bot formats in favor of slash commands, which they expect all bots to be using by early to mid next year. Seeing as discord.py does not currently support slash commands and I do not have the time necessary to rework the lib myself for effective slash command usage, the future of this project is fairly bleak. For the forseeable future, the option to self host this bot is your best bet, and will allow you to run the very same version of the bot as before, at least until discord requires slash commands, or discord.py gets a maintainer and I have some time to rework the code in the repo to support slash commands. See https://replit.com/@fretgfr/SnipeBotTemplate

If you're interested in potentially helping this project, please DM me on Discord fretgfr#3216.

## About

This project started on my relatively small server back in April of 2020. SnipeBot first went public back in August of 2020, and has since grown rapidly to be in over 32,000 discord servers, ranging from ones with just a few members, to ones with over 78,000 members, and boy has it been one hell of a journey. After being approved on top.gg, the bot hit the 100 server limit in just a few weeks. Following Dank Memer's snipe feature either being disabled or breaking, the bot started to grow exponentially, hitting 1,000 servers in only a few days following it's verification.

Since this point, the bot has grown beyond what I ever could have imagined it would. Being self-hosted on a pair of \(very dedicated\) Raspberry Pi 4s, the bot has recently began having trouble handling the sheer load of messages it needs to store, seeing as how it's currently written, all information is held in memory. Seeing as I currently don't have the time to convert the entire bot to using a database, setting up the database server, etc. I have decided to put out a version of the bot that you can use to host it for yourself!

In the future, I will be reworking the bot, but it may take some time due to my schedule.

Please note that the version that is in this repo is a slimmed down version designed for you to be able to run the essential features on your own, and does not include some of the other features, such as whitelisting, etc.

### Requirements

Software was developed and tested using Python 3.9.5 64 bit, though any version over 3.7.3 *should* work, I recommend using 3.9.5 64 bit.

* A text editor ([Notepad++](https://notepad-plus-plus.org/downloads/) or the built in Notepad will work).
* A Python installation on your host.
* The `discord.py` and `pillow` python modules installed using pip: (`py -3 -m pip -install --upgrade discord.py pillow`) on Windows.
* A machine to run on. Can be any computer that you'd like to use, but should be one that is constantly running.

### Installing

To begin, please read the ***license*** associated with this software. Then do the following:

1. Create a bot application on the Discord developer page, instructions for doing this can be found online. Please note that you will have to have all privileged intents enabled to run without modifying the source.
2. Edit the `config.json` provided so that, at the minimum, your bot's token is in there.
3. Make sure the `config.json` file and your `snipebot.py` are in the same directory, and run the `snipebot.py` script.
4. Your bot should come online.

*repl.it specific: You need to have a secret named "TOKEN" that holds your discord application token in order to run instead of using config.json for security reasons. `snipebot.py` will need to be named `main.py`. Because repl.it provides relatively weak machines, the `aim` command may perform poorly.*

### Configuration Options

The default configuration file is below. Along with a table detailing how each option can be used. This file should be in the same directory/folder as your `snipebot.py` file and should be named `config.json`.

```json

{
    "token": "xyz",
    "extensions": ["commands.aim", "commands.editsnipe", "commands.py", "commands.reactionsnipe", "commands.snipe", "utils.errorhandler"],
    "prefix": "~",
    "mentionprefix": true,
    "ignorecase": true,
    "status": "Sniping the sus"
}

```


| Option        | Values         | Purpose                                                                                                             |
| --------------- | ---------------- | :-------------------------------------------------------------------------------------------------------------------- |
| token         | String         | The token the code will be run using, should be your application's bot token from the Discord developers dashboard. |
| extensions    | List of String | List of modules that will be loaded by the bot.                                                                     |
| prefix        | String         | The prefix your bot will have when running                                                                          |
| mentionprefix | boolean        | Whether or not people should be able to mention the bot instead of using it's command prefix                        |
| status        | String         | The status your bot will have when it comes online                                                                  |

**Please note that the `py` extension allows the execution of arbitrary code, and should always be safeguarded against use by others or disabled.**

### Resources

I highly encourage you to make your own changes to this code! Please feel free to add your own features or edit existing ones. Resources for doing so are below.

[discord.py Documentation](https://discordpy.readthedocs.io/en/latest/)

[discord.py getting started guide](https://discordpy.readthedocs.io/en/latest/#getting-started)

[Official Python Tutorial](https://docs.python.org/3/tutorial/)

[Python Cheat Sheet](https://learnxinyminutes.com/docs/python/)
