import discord
from discord.ext import commands

class Mensajes(commands.Cog):

    def __init__(self,client):
        self.client=client

    @commands.Cog.listener()
    async def on_message(self,message):
        if message.author == client.user or message.author.bot:
            return

        if message.content.lower()=='f':
            await message.add_reaction('<:f_:768439683020488724>')

        if message.content.lower()=='si':
            await message.add_reaction('<a:si:767567093896839179>')

        if message.content.lower()=='no':
            await message.add_reaction('<a:no:767567093482520586>')

        if 'q onda' in message.content.lower():
            await message.add_reaction('<:degenerado:751791150364491966>')

        if 'cringe' in message.content.lower():
            await message.add_reaction('<:cringe:735225671969669221>')

        if '<:picardia:735101971001770055>' in message.content:
            await message.add_reaction('<:picardia:735101971001770055>')

        if '<:picardiant:748344255906447432>' in message.content:
            await message.add_reaction('<:picardiant:748344255906447432>')

        if 'gracias' in message.content.lower() or 'garcias' in message.content.lower():
            await message.add_reaction('<:garcias:764579105542373387>')
        
        if random.choice(list(range(1000)))==0:
            await message.add_reaction(random.choice(message.guild.emojis))
        
        if len(message.content)>500:
            await message.add_reaction('<:mucho_texto:743541235637026818>')
        
        if 'uwu' in message.content.lower() and message.content.lower()!='<:uwu:768614592699957278>':
            await message.add_reaction('<:uwu:768614592699957278>')

        if 'medialuna' in message.content.lower():
            pedido.append('🥐')

        if 'cafe' in message.content.lower():
            pedido.append(':coffee:')
        if len(pedido)!=0:
            await message.channel.send("".join(pedido))

def setup(client):
    client.add_cog(Mensajes(client))