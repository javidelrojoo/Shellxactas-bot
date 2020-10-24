import discord
from discord.ext import commands, tasks
import os
import time
import asyncio
import random
import subprocess
import requests
from datetime import datetime
from datetime import timedelta

client = commands.Bot(command_prefix='.', status=discord.Status.dnd, case_insensitive=True,
                      description='El bot de Shellxactas')

status = ['Viendo al coscu', 'Estudiando', 'Preparando un golpe de estado', 'Leyendo el Don Quijote',
          'Haciendome una paja', 'Analizando el mercado', 'Comiendome a tu vieja']

if __name__ == '__main__':
    for filename in os.listdir('cogs'):
        if filename.endswith('.py'):
            client.load_extension(f'cogs.{filename[:-3]}')


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


token = os.getenv('TOKEN')

client.run(token)
