import discord
from discord.ext import commands,tasks
import os
import time
import asyncio
import random
import subprocess
import requests

client = commands.Bot(command_prefix='.',status=discord.Status.dnd,case_insensitive=True,description='El bot de Shellxactas')

status=['Viendo al coscu','Estudiando','Preparando un golpe de estado','Leyendo el Don Quijote','Haciendome una paja','Analizando el mercado','Comiendome a tu vieja']

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
    await client.change_presence(status=discord.Status.dnd,activity=discord.Game(random.choice(status)))

#Va para boludeces
@client.command()
async def plan(ctx):
    """Te dice el plan de la carrera que quieras"""
    await ctx.send('Para que queres saber? Salu2 <:picardia:735101971001770055>')

@client.command()
async def rdm(ctx):
    await ctx.send(random.choice(ctx.message.guild.emojis))

@client.command(aliases = ["sensuky", "sensooky"])
async def sensu(ctx):
    await ctx.send('<@219301336544444416> <https://www.twitch.tv/sensuky>')

@client.command(aliases = ["marcos", "MDG"])
async def markz(ctx):
    await ctx.send('<@710666266972651531> <https://es.pornhub.com/gayporn>')


token=os.getenv('TOKEN')

client.run(token)
