import discord
from discord.ext import commands
from webserver import keep_alive
import os
import sys
import json
import time

#repl.it specific: You need to have a secret named "TOKEN" that holds your discord application token in order to run instead of using config.json for security reasons

# Make sure there's a config
if not os.path.exists("./config.json"):
    print("Generating default configuration.")
    time.sleep(2.0) #Arbitrary sleep so they think something is happening.
    with open("config.json", "w") as fp:
        fp.write(
"""{
    "token": "xyz",
    "extensions": ["commands.aim", "commands.editsnipe", "commands.py", "commands.reactionsnipe", "commands.snipe", "utils.errorhandler"],
    "prefix": "~",
    "mentionprefix": true,
    "ignorecase": true,
    "status": "Sniping the sus"
}"""
                 )
    input("Generated a default config for you. Please edit it and try again.")
    sys.exit()

#Load config
with open("config.json", "r") as fp:
    opts = json.load(fp)
    print("Configuration file successfully loaded.")
    print("=================")


PREFIX = commands.when_mentioned_or(opts['prefix']) if opts["mentionprefix"] else opts['prefix']
print(f"Your bot's prefix is set to `{opts['prefix']}` and {'is' if callable(PREFIX) else 'is not'} able to be mentioned instead of using a prefix")

CASE_INSENSITIVE = True if opts['ignorecase'] else False
print(f"Your bot {'is' if not CASE_INSENSITIVE else 'is not'} case sensitive.")
# Your intents may have to be different.
bot_intents = discord.Intents.all()

bot_mem_cache_flags = discord.MemberCacheFlags.from_intents(bot_intents)
_botinstance = commands.Bot(PREFIX, None,  member_cache_flags=bot_mem_cache_flags, intents=bot_intents, case_insensitive=CASE_INSENSITIVE, activity=discord.Activity(type=discord.ActivityType.playing, name=opts['status']))
print(f"Your bot's status is set to: {opts['status']}")

print(f"Loading bot with extensions: {opts['extensions']}")
for ext in opts["extensions"]:  # Load all the extensions
    _botinstance.load_extension(ext)
    print(f"Successfully loaded extension: {ext}")


if __name__ == "__main__":
    print("=================")
    keep_alive()
    print("Starting Bot")
    _botinstance.run(os.environ["TOKEN"])
