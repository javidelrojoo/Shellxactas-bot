import discord
from discord.ext import commands
import random


class Mensajes(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, discord.ext.commands.errors.CommandNotFound):
            await ctx.send('¿Necesitas ayuda para escribir el comando?')
            return

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        if member.guild.id != 734914669667418214:
            return
        chatdeadmins = member.guild.get_channel(734917753693274224)
        await chatdeadmins.send(f'Se fué {member.mention}')

    @commands.Cog.listener()
    async def on_member_join(self, member):
        if member.guild.id != 734914669667418214:
            return
        chatdeadmins = member.guild.get_channel(734917753693274224)
        botrole = member.guild.get_role(756934683790671873)
        onlinerole = member.guild.get_role(756934020343922719)
        if member.bot:
            await member.add_roles(botrole)
        else:
            await member.add_roles(onlinerole)
        await chatdeadmins.send(f'Se unió {member.mention}')

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        if message.content.lower() == 'f':
            await message.add_reaction('<:f_:768439683020488724>')

        if message.content.lower() == 'si' or message.content.lower() == 'sí':
            await message.add_reaction('<a:si:767567093896839179>')

        if message.content.lower() == 'no':
            await message.add_reaction('<a:no:767567093482520586>')

        if 'q onda' in message.content.lower():
            await message.add_reaction('<:degenerado:751791150364491966>')

        if 'cringe' in message.content.lower():
            await message.add_reaction('<:cringe:832829654259859537>')

        if '<:picardia:735101971001770055>' in message.content:
            await message.add_reaction('<:picardia:735101971001770055>')

        if '<:picardiant:748344255906447432>' in message.content:
            await message.add_reaction('<:picardiant:748344255906447432>')

        if 'gracias' in message.content.lower() or 'garcias' in message.content.lower():
            await message.add_reaction('<:garcias:835015498697146398>')
        
        if 'sape' in message.content.lower():
            await message.add_reaction('<:sape:735262152675295343>')

        if random.randint(0, 1000) == 0:
            await message.add_reaction(random.choice(message.guild.emojis))

        if len(message.content) > 500:
            await message.add_reaction('<:mucho_texto:743541235637026818>')

        if 'uwu' in message.content.lower() and message.content.lower() != '<:uwu:768614592699957278>':
            await message.add_reaction('<:uwu:768614592699957278>')
        
        if 'jaja' in message.content.lower() and message.author.id == 452285420609339402:
            await message.add_reaction('<:joaco:788188614328713217>')

        if 'basado' in message.content.lower() or 'based' in message.content.lower(): 
            await message.add_reaction("<:BASED:783045382426722344>")

        pedido = []
        if 'medialuna' in message.content.lower():
            pedido.append('🥐')

        if 'cafe' in message.content.lower():
            pedido.append(':coffee:')
        if len(pedido) != 0:
            await message.channel.send("".join(pedido))


def setup(client):
    client.add_cog(Mensajes(client))
