import os
import asyncio
import discord
from discord import app_commands
from dotenv import load_dotenv

from commands import register_commands
from utils.logger import setup_logger

load_dotenv()
logger = setup_logger()


class EnergyBot(discord.Client):
    def __init__(self):
        intents = discord.Intents.default()
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)
        self.synced = False

    async def setup_hook(self):
        await self.tree.sync(guild=discord.Object(id=int(os.getenv("GUILD_ID"))))
        self.synced = True

    async def on_ready(self):
        logger.info(f"Logged in as {self.user} (ID: {self.user.id})")
        logger.info("------")


async def main():
    async with EnergyBot() as client:
        register_commands(client.tree)
        await client.start(os.getenv("DISCORD_TOKEN"))


if __name__ == "__main__":
    asyncio.run(main())
