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
        intents.message_content = True  # Enable message content intent
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        # This is called before the bot starts
        register_commands(self.tree)

        # Sync commands with Discord
        guild_id = os.getenv("GUILD_ID")
        if guild_id:
            guild = discord.Object(id=int(guild_id))
            self.tree.copy_global_to(guild=guild)
            await self.tree.sync(guild=guild)
            logger.info(f"Synced commands to guild {guild_id}")
        else:
            await self.tree.sync()
            logger.info("Synced commands globally")

    async def on_ready(self):
        logger.info(f"Logged in as {self.user} (ID: {self.user.id})")
        logger.info("------")


async def main():
    async with EnergyBot() as client:
        await client.start(os.getenv("DISCORD_TOKEN"))


if __name__ == "__main__":
    asyncio.run(main())
