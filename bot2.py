import requests
import json
import re
import discord
import configparser
from discord.ext import commands

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

'''
@client.event
async def on_ready():
  # Make a GET request to the URL
  response = requests.get("https://ir.eia.gov/ngs/wngsr.json")

  # Check the status code of the response
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

  # Iterate through each series
  for series in data['series']:
    # Send a message to the "general" channel with the net change value
        channel = client.get_channel(908099245402378290)
        await channel.send('{}: {}'.format(series['name'], series['calculated']['net_change']))

'''

client.run(TOKEN)