import discord
import os
from joke import get_joke,search_joke
from meme import get_meme

my_secret = os.environ['TOKEN']

client = discord.Client()


#register event, also call back
@client.event
#onready event, call when the bot being used
async def on_ready():
    print("We are {0.user}".format(client))


@client.event
#message from bot
#triggered when message is received
async def on_message(message):
    if message.author == client.user:
        return


    msg = message.content
    
    #Convert joke
    splitStr = msg.split()[3];
    
    if msg.startswith('$tell me a joke'):
      await message.channel.send(get_joke())
    if msg.startswith('$tell me a {0} joke'.format(splitStr)):
      await message.channel.send(search_joke(splitStr))
  
    #convert meme
    if msg.startswith("$send me a meme"):
      await message.channel.send(get_meme())
    


  
#run the bot

client.run(my_secret)
