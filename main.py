import os
import discord
from discord.ext import commands
from tinydb import TinyDB, Query
import requests

token = os.environ['discord_key']

intents = discord.Intents.default()

client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix='$', intents=intents)

db = TinyDB('./users.db')
dbuser = Query()

@client.event
async def on_ready():
    print(f'{client.user} has connected to discord')

@bot.command()
async def setup(message, query: str):
    channel = message.channel
    userID =  message.author.id

    req = f'https://nominatim.openstreetmap.org/search?q={query}&format=json'
    r = requests.get(req).json()

    print(r)
    # await channel.send(f"You are {userID}, requesting for {query}")
    await channel.send(f"Location: {r[0]['display_name']}")
    
    lat = r[0]['lat']
    lon = r[0]['lon']

    if db.search(dbuser.id == userID) == []:
        db.insert({
            'id':userID,
            'lat' : lat,
            'lon' : lon,
            'name' : r[0]['display_name']
        })
    else:
        db.update({'lat' :lat, 'lon' : lon, 'name' : r[0]['display_name']}, dbuser.id == userID)


def getUserLoc(userID):
    # userID = message.author.id
    userinfo = db.search(dbuser.id == int(userID))[0]
    name, lat, lon = userinfo['name'], userinfo['lat'], userinfo['lon']

    return name,lat,lon

@bot.command()
async def aqi(message):
    name, lat, lon = getUserLoc(message.author.id)

    token = '7c3a4323f76a6485febfb00a0ec5f161984d9225'
    baseurl = 'https://api.waqi.info'
    # print(lat, lon)
    req = f'{baseurl}/feed/geo:{lat};{lon}/?token={token}'
    r = requests.get(req).json()
    # print(r)

    aqi = r['data']['aqi']
    o3 = r['data']['iaqi']['o3']['v']
    pm25 = r['data']['iaqi']['pm25']['v']

    await message.channel.send(f"Information for {name}")
    await message.channel.send(f"The AQI is {aqi}")
    await message.channel.send(f"PM2.5: {pm25}")
    await message.channel.send(f"Ozone: {o3}")
bot.run(token)   