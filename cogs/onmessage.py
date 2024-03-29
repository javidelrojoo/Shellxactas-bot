import discord
from discord.ext import commands
import random
import asyncio

class Mensajes(commands.Cog):

    def __init__(self, client):
        self.client = client

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
        joserole = member.guild.get_role(858022564626038844)
        mutedrole = member.guild.get_role(757376238053621850)
        if member.bot:
            await member.add_roles(botrole)
        else:
            await member.add_roles(onlinerole)
            if member.id == 470723884166021120:
                await member.add_roles(joserole)
        await chatdeadmins.send(f'Se unió {member.mention}')
        await asyncio.sleep(5.)
        if mutedrole in member.roles:
            await member.remove_roles(mutedrole)

    # @commands.Cog.listener()
    # async def on_message(self, message):
    #     if message.author.bot:
    #         return

    #     if message.content.lower() == 'f':
    #         await message.add_reaction('<:f_:768439683020488724>')

    #     if message.content.lower() == 'si' or message.content.lower() == 'sí':
    #         await message.add_reaction('<a:si:767567093896839179>')

    #     if message.content.lower() == 'no':
    #         await message.add_reaction('<a:no:767567093482520586>')

    #     if 'q onda' in message.content.lower():
    #         await message.add_reaction('<:degenerado:751791150364491966>')

    #     if 'cringe' in message.content.lower():
    #         await message.add_reaction('<:cringe:832829654259859537>')

    #     if '<:picardia:735101971001770055>' in message.content:
    #         await message.add_reaction('<:picardia:735101971001770055>')

    #     if '<:picardiant:748344255906447432>' in message.content:
    #         await message.add_reaction('<:picardiant:748344255906447432>')

    #     if 'gracias' in message.content.lower() or 'garcias' in message.content.lower():
    #         await message.add_reaction('<:garcias:835015498697146398>')
        
    #     if 'sape' in message.content.lower():
    #         await message.add_reaction('<:sape:735262152675295343>')

    #     if 'god' in message.content.lower() or 'good' in message.content.lower() or 'goood' in message.content.lower():
    #         await message.add_reaction('<a:gooood:861332255904759808>')

    #     if 'messi' in message.content.lower():
    #         await message.add_reaction('<a:messsi:861332725247508490>')

    #     if random.randint(0, 1000) == 0:
    #         await message.add_reaction(random.choice(message.guild.emojis))

    #     if len(message.content) > 500:
    #         if message.author.id == 470723884166021120:
    #             await message.channel.send('Callate puta')
    #         await message.add_reaction('<:mucho_texto:743541235637026818>')

    #     if 'uwu' in message.content.lower() and message.content.lower() != '<:uwu:768614592699957278>':
    #         await message.add_reaction('<:uwu:768614592699957278>')
        
    #     if 'jaja' in message.content.lower() and message.author.id == 452285420609339402:
    #         await message.add_reaction('<:joaco:788188614328713217>')

    #     if 'basado' in message.content.lower() or 'based' in message.content.lower(): 
    #         await message.add_reaction("<:BASED:783045382426722344>")

    #     if 'cuervo' in message.content.lower(): 
    #         await message.add_reaction("<:rojo:855269121561329704>")

    #     josewords = ['https://cdn.discordapp.com/attachments/734921776882122762/887134902544375860/static-assets-upload17303428989518158196.webp', 'sussy', 'tfw', 'kys', 'finna', 'kms', 'ubi', 'nene daun', 'nene down', 'ya lo pasé', 'ya lo pase', 'ya lo pasaron', 'inb4', 'viejazo', 'kino']
    #     if message.author.id == 470723884166021120:
    #         if (sum([i in message.content.lower() for i in josewords]) > 0):
    #             await message.channel.send('Callate puta')
    #     # pedido = []
    #     # if 'medialuna' in message.content.lower():
    #     #     pedido.append('🥐')

    #     # if 'cafe' in message.content.lower():
    #     #     pedido.append(':coffee:')
    #     # if len(pedido) != 0:
    #     #     await message.channel.send("".join(pedido))


def setup(client):
    client.add_cog(Mensajes(client))
