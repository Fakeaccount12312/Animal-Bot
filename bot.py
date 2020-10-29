import discord
import random
import csv
from synonyms import synonyms
from tokens import tokens
from datetime import datetime
import os

token = tokens["animal-bot"]

data = {}
with open("imageurls.csv", "r", newline="") as f:
    reader = csv.reader(f)
    for row in reader:
        data[row[0]] = row[1:]
data.pop("animal")

client = discord.Client()

supported_animals = ", ".join(sorted(list(data.keys()) + ["random"]))


async def postimage(channel, imageurl, title=None, description=None):
    #print(imageurl, title, description, type(imageurl))
    embedded = discord.Embed(title=title, description=description)
    embedded.set_image(url=imageurl)
    await channel.send(embed=embedded)

print("Animal bot started at " + datetime.now().strftime("the %d.%m.%y at %H:%M:%S"))


@client.event
async def on_ready():
    print('Logged in as {0.user} at '.format(client) + datetime.now().strftime("the %d.%m.%y at %H:%M:%S"))
    await client.change_presence(activity=discord.Activity(name="süße Kaninchenvideos", type=discord.ActivityType.watching))


@client.event
async def on_message(message):
    msg = message.content
    if message.author == client.user:
        return
    if msg.startswith('-') and message.channel.name == "bot-test":
        msg = msg[1:]
        if msg == "help animals":
            embedded = discord.Embed(title="Unterstützte Tierarten/ Befehle:", description=supported_animals)
            await message.channel.send(embed=embedded)
        elif msg in synonyms and synonyms[msg] in data:
            await postimage(message.channel, data[synonyms[msg]][0] + random.choice(data[synonyms[msg]]))
        elif msg == "random":
            animal = random.choice(list(data.keys()))
            await postimage(message.channel, data[synonyms[animal]][0] + random.choice(data[synonyms[animal]]), title="A random " + animal)
        elif msg == "human":
            await postimage(message.channel, "https://m.media-amazon.com/images/M/MV5BOTIyODY1OTYtZjAzNS00ZGQ2LWFhNmItMTJkYTc0MDNkYTk0XkEyXkFqcGdeQXVyODg3NTgyODQ@._V1_.jpg")
        elif msg in ("github", "source", "sourcecode", "code"):
            await message.channel.send(embed=discord.Embed(title="Github", url="https://github.com/Fakeaccount12312/Animal-Bot"))
        elif msg == "update" and message.author.name == "Fakeaccount1231":
            await message.channel.send(embed=discord.Embed(title="updating..."))
            os.system("sh update.sh &")
        elif msg == "stop" and message.author.name == "Fakeaccount1231":
            await message.channel.send(embed=discord.Embed(title="Bot stopped"))
            exit()

client.run(token)
