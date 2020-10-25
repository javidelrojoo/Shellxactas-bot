import discord
from discord.ext import commands, tasks
import os
import time
import asyncio
import random
import subprocess
import requests
import pymongo
from datetime import datetime, timedelta, time

intents = discord.Intents.default()
intents.members = True

client = commands.Bot(command_prefix='.', status=discord.Status.dnd, case_insensitive=True,
                      description='El bot de Shellxactas', intents=intents)

status = ['Viendo al coscu', 'Estudiando', 'Preparando un golpe de estado', 'Leyendo el Don Quijote',
          'Haciendome una paja', 'Analizando el mercado', 'Comiendome a tu vieja']

if __name__ == '__main__':
    for filename in os.listdir('cogs'):
        if filename.endswith('.py'):
            client.load_extension(f'cogs.{filename[:-3]}')

mongo_url = os.getenv('MONGO_URL')

mongoclient = pymongo.MongoClient(mongo_url)

mongoprueba = mongoclient['Prueba']
mongoremindme = mongoprueba["remindme"]


@client.event
async def on_ready():
    change_status.start()
    print('Loggeado como:')
    print(client.user.name)
    print(client.user.id)
    print('------')


@tasks.loop(minutes=20)
async def change_status():
    await client.change_presence(status=discord.Status.dnd, activity=discord.Game(random.choice(status)))


@client.command()
async def ahora(ctx):
    await ctx.send(datetime.now())


async def upremindme():
    await client.wait_until_ready()
    nowtime = datetime.utcnow()
    for x in mongoremindme.find():
        authorid = int(x['authorid'])
        author = client.get_user(authorid)
        canalid = int(x['channelid'])
        canal = client.get_channel(canalid)
        record = x['recordatorio']
        url = x['url']
        dbwait = time.fromisoformat(x['wait'])
        if dbwait > nowtime:
            wait = dbwait-nowtime
            await asyncio.sleep(wait.total_seconds())
            await canal.send(f'{author.mention} ya pasó el tiempo. {record} {url}')
        else:
            mongoremindme.delete_one(x)

client.loop.create_task(upremindme())

token = os.getenv('TOKEN')

client.run(token)
