import requests
import json
import re
import discord
import configparser
from discord.ext import commands
from ttf import DataFetcher
from oil_weekly_report import extract_oil_weekly_text
from natgasweather import get_natgasweather

def get_natgas_data_and_format_message():
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
    fetcher = DataFetcher()
    data = fetcher.fetch_ttf_data()
    message = "Dutch TTF Natural Gas Futures\n\n"
    for item in data:
        futures = item['Futures: ']
        last_price = item['Last Price: ']
        # print(f'Futures: {futures}, Last Price: {last_price}')
        message += f"{futures}: {last_price}\n"

    return message

# Read the config.ini file
config = configparser.ConfigParser()
config.read("config.ini")

# Get the Discord bot's token from the config.ini file
TOKEN = config["DISCORD"]["TOKEN"]

# Create a Discord client
client = discord.Client(intents=discord.Intents.all())



@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@client.event
async def on_message(message):
    # Only respond to commands from users, not other bots
    if message.author == client.user:
        return

    if message.content.startswith("!natgas"):
        # Get the data from the API and format it as a message
        data = get_natgas_data_and_format_message()
    
        # Send the message to the channel where the command was used
        await message.channel.send(data)
    
    elif message.content.startswith("!ttf"):  
        data = get_and_format_ttf_message()
        await message.channel.send(data)

    elif message.content.startswith("!oilreport"):
        text = extract_oil_weekly_text()
        print(len(text))
        
        MAX_LENGTH = 1500

        # Split the text into chunks
        chunks = [text[i:i+MAX_LENGTH] for i in range(0, len(text), MAX_LENGTH)]

        # Send each chunk as a separate message
        for chunk in chunks:
            # Send the message (code for this step goes here)
            await message.channel.send(chunk)

    elif message.content.startswith("!ng"):
        natgaseather_update = get_natgasweather()
        headline = natgaseather_update['headline']
        await message.channel.send(headline)
        daily_update = natgaseather_update['daily_update']
        await message.channel.send(daily_update)


client.run(TOKEN)