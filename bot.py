import discord
from discord.ext import commands

client = commands.Bot(command_prefix='.')

@client.event
async def on_ready():
    print('Ya arranqué')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if 'q onda' in message.content:
        await message.add_reaction('<:degenerado:751791150364491966>')
        await message.channel.send('q onda')

@client.command()
@commands.is_owner()
async def shutdown(ctx):
    await ctx.bot.logout()

client.run('NzY3NDQwNzExOTUxMDU2OTM2.X4x83A.Yr4cM0K1C2WlhWcN3Mlqy7N421c')
