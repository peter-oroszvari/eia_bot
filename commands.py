import discord
from discord import app_commands, Embed
from controllers.ng_storage_report_controller import NGController
from controllers.ttf_controller import TTFController
from controllers.rigcount_controller import RigCountController
from services.oil_weekly_report import extract_oil_weekly_text
from services.natgasweather import get_natgasweather
from utils.image_handler import save_and_send_image
from utils.logger import get_logger
from utils.logger import setup_logger

main_logger = setup_logger()
logger = get_logger(__name__)


def register_commands(tree: app_commands.CommandTree):
    @tree.command(name="ping", description="Check if the bot is responsive")
    async def ping(interaction: discord.Interaction):
        await interaction.response.send_message("Pong!")
        logger.info("Ping command executed")

    @tree.command(
        name="natgas",
        description="Prints the up-to-date Weekly Natural Gas Storage Report",
    )
    async def natgas(interaction: discord.Interaction):
        await interaction.response.defer()
        try:
            controller = NGController()
            data = controller.get_formatted_data()
            embed = Embed(title="Weekly Natural Gas Storage Report", description=data)
            embed.set_footer(text="Source: EIA")
            await interaction.followup.send(embed=embed)
        except Exception as e:
            logger.error(f"Error in natgas command: {str(e)}")
            await interaction.followup.send(
                "An error occurred while fetching the Natural Gas Storage Report."
            )

    @tree.command(name="ttf", description="Prints up-to-date Dutch TTF futures prices")
    async def ttf(interaction: discord.Interaction):
        await interaction.response.defer()
        try:
            controller = TTFController()
            data = controller.get_formatted_data()
            embed = Embed(title="Dutch TTF Natural Gas Futures", description=data)
            embed.set_footer(text="Source: theice.com")
            await interaction.followup.send(embed=embed)
        except Exception as e:
            logger.error(f"Error in ttf command: {str(e)}")
            await interaction.followup.send(
                "An error occurred while fetching TTF futures prices."
            )

    @tree.command(
        name="oilreport", description="Prints the weekly petroleum status report"
    )
    async def oilreport(interaction: discord.Interaction):
        await interaction.response.defer()
        try:
            text = extract_oil_weekly_text()

            if text.startswith("Error"):
                await interaction.followup.send(text)
                return

            MAX_LENGTH = 1900  # Increased to 1900 to maximize Discord's message limit
            chunks = [text[i : i + MAX_LENGTH] for i in range(0, len(text), MAX_LENGTH)]

            embed = discord.Embed(
                title="Weekly Petroleum Status Report", color=0x00FF00
            )
            await interaction.followup.send(embed=embed)

            for i, chunk in enumerate(chunks, 1):
                formatted_chunk = f"```\n{chunk}\n```"
                await interaction.followup.send(formatted_chunk)

            logger.info(
                f"Oilreport command successfully executed by {interaction.user.name} (ID: {interaction.user.id})"
            )

        except Exception as e:
            error_message = f"```diff\n- An error occurred while fetching the oil report. Please try again later.\n```"
            await interaction.followup.send(error_message)
            logger.error(f"Error in oilreport command: {str(e)}", exc_info=True)

        logger.debug("Oilreport command execution completed")

    @tree.command(
        name="ngweather",
        description="Prints the headline and daily update from natgasweather.com",
    )
    async def ngweather(interaction: discord.Interaction):
        await interaction.response.defer()
        try:
            natgasweather_update = get_natgasweather()
            embed = Embed(
                title=natgasweather_update["headline"],
                description=natgasweather_update["daily_update"],
            )
            embed.set_footer(text="Source: Natgasweather.com")
            await interaction.followup.send(embed=embed)
        except Exception as e:
            logger.error(f"Error in ngweather command: {str(e)}")
            await interaction.followup.send(
                "An error occurred while fetching the natural gas weather update."
            )

    @tree.command(
        name="rigcount", description="Retrieves the Baker Hughes Rig Count Overview"
    )
    async def rigcount(interaction: discord.Interaction):
        await interaction.response.defer()
        try:
            controller = RigCountController()
            controller.display_data()
            await save_and_send_image(interaction, "dataframe.png")
        except Exception as e:
            logger.error(f"Error in rigcount command: {str(e)}")
            await interaction.followup.send(
                "An error occurred while fetching the rig count data."
            )

    logger.info(f"Registered {len(tree.get_commands())} commands")
