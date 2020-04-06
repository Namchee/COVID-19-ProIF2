from os import environ
from dotenv import load_dotenv, find_dotenv
from bot import bot

load_dotenv(find_dotenv())

if __name__ == "__main__":
    bot.run(environ.get("DISCORD_TOKEN"))
