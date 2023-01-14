import discord
from discord import app_commands, Embed
import configparser
import requests
import json
import re
from ttf import DataFetcher
from oil_weekly_report import extract_oil_weekly_text
from natgasweather import get_natgasweather

def get_natgas_data_and_format_message():
    """
    This function retrieves data from the "https://ir.eia.gov/ngs/wngsr.json" API and formats it as a message.
    The function makes a GET request to the API and retrieves the data.
    It then checks if the response status code is 200, if it is, it attempts to load the response text as a JSON object.
    If the response status code is not 200 or if the response text is not a valid JSON object, it prints an error message.
    If the response is valid, the function formats the data as a message and returns it.
    """
    # Make a GET request to the API and retrieve the data
    response = requests.get("https://ir.eia.gov/ngs/wngsr.json")
    
    if response.status_code == 200:
    # Try to load the response text as a JSON object
        try:
            data = json.loads(re.sub('ï»¿', '', response.text))
        except json.decoder.JSONDecodeError:
            # The response is not a valid JSON object
            print("Error: the server did not return a valid JSON object")
    else:
        # There was an error making the request
        print("Error loading data from URL (status code: {})".format(response.status_code))

    # Format the data as a message
    release_date = data['release_date']
    message = f"Natural Gas Storage Report for {release_date}\n\n"
    for series in data['series']:
        name = series['name']
        net_change = series['calculated']['net_change']
        message += f"{name}: {net_change}\n"
    
    return message

def get_and_format_ttf_message(): 
    """
    This function retrieves data from the DataFetcher class and formats it as a message.
    It creates an instance of the DataFetcher class and retrieves the data by calling the fetch_ttf_data() method.
    The function then formats the data as a message, adding the title "Dutch TTF Natural Gas Futures" and appending
    the "futures" and "last price" information for each item in the data.
    The function returns the formatted message.
    """
    fetcher = DataFetcher()
    data = fetcher.fetch_ttf_data()
    message = ""
    for item in data:
        futures = item['Futures: ']
        last_price = item['Last Price: ']
        # print(f'Futures: {futures}, Last Price: {last_price}')
        message += f"{futures}: {last_price}\n"

    return message

# Read the config.ini file
config = configparser.ConfigParser()
config.read("config.ini")

# Get the Discord bot's token and guild ID from the config.ini file
TOKEN = config["DISCORD"]["TOKEN"]
guild_id = config["DISCORD"]["GUILD"]


class aclient(discord.Client):
    def __init__(self):
        super().__init__(intents = discord.Intents.default())
        self.synced = False #we use this so the bot doesn't sync commands more than once

    async def on_ready(self):
        await self.wait_until_ready()
        if not self.synced: #check if slash commands have been synced 
            await tree.sync(guild = discord.Object(id=guild_id)) #guild specific: leave blank if global (global registration can take 1-24 hours)
            self.synced = True
        print(f"We have logged in as {self.user}.")

client = aclient()
tree = app_commands.CommandTree(client)


@tree.command(guild = discord.Object(id=guild_id), name = 'natgas', description='Prints the up to date Weekly Natural Gas Storage Report') #guild specific slash command
async def slash2(interaction: discord.Interaction):
    # Get the data from the API and format it as a message
    data = get_natgas_data_and_format_message()
     # Create a Discord embed message
    embed = Embed(
        title="Weekly Natural Gas Storage report", 
        description=data,
        )
    embed.set_footer(text = "Source: EIA")
    # Send the message to the channel where the command was used
    await interaction.response.send_message(embed=embed) 

@tree.command(guild = discord.Object(id=guild_id), name = 'ttf', description='Prints to up to date Dutch TTF futures prices') #guild specific slash command
async def slash2(interaction: discord.Interaction):
    data = get_and_format_ttf_message()
    # Create a Discord embed message
    embed = Embed(
        title="Dutch TTF Natural Gas futures", 
        description=data,
        )
    embed.set_footer(text = "Source: theice.com")
    await interaction.response.send_message(embed=embed) 

@tree.command(guild = discord.Object(id=guild_id), name = 'oilreport', description='Prints the weekly petroleum status report') #guild specific slash command
async def slash2(interaction: discord.Interaction):
    await interaction.response.send_message(f'Retriving the Weekly Petroleum Status Report') 

    text = extract_oil_weekly_text()
    print(len(text))
        
    MAX_LENGTH = 1500

    # Split the text into chunks
    chunks = [text[i:i+MAX_LENGTH] for i in range(0, len(text), MAX_LENGTH)]

    # Send each chunk as a separate message
    for chunk in chunks:
        # Send the message (code for this step goes here)
        await interaction.channel.send(chunk)

@tree.command(guild = discord.Object(id=guild_id), name = 'ngweather', description='Prints the headline and daily update from natgasweather.com') #guild specific slash command
async def slash2(interaction: discord.Interaction):
    await interaction.response.send_message(f'Retriving data from natgasweather.com') 
    natgaseather_update = get_natgasweather()
    headline = natgaseather_update['headline']
    daily_update = natgaseather_update['daily_update']
    embed = Embed(
        title=headline, 
        description=daily_update,
        )
    embed.set_footer(text = "Source: Natgasweather.com")
    await interaction.channel.send(embed=embed)
    '''
    natgaseather_update = get_natgasweather()
    headline = natgaseather_update['headline']
    await interaction.channel.send(headline)
    daily_update = natgaseather_update['daily_update']
    await interaction.channel.send(daily_update)
    '''


client.run(TOKEN)