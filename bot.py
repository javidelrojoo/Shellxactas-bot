import discord
from discord.ext import commands, tasks
import os

intents = discord.Intents.default()
intents.members = True

client = commands.Bot(command_prefix='.', status=discord.Status.dnd, case_insensitive=True,
                      description='El bot de Shellxactas', intents=intents)


if __name__ == '__main__':
    for filename in os.listdir('cogs'):
        if filename.endswith('.py'):
            client.load_extension(f'cogs.{filename[:-3]}')


@client.event
async def on_ready():
    print('Loggeado como:')
    print(client.user.name)
    print(client.user.id)
    print('------')


token = os.getenv('TOKEN')

client.run(token)
