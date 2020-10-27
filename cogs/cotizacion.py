import discord
from discord.ext import commands
import dolar as dlr


class Cotizacion(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(brief='Cotización dolar',
                      help='Este comando te brinda informacion actualizada sobre el valor del dolar. No requiere de '
                           'ningún argumento.')
    async def dolar(self, ctx):
        if dlr.valor_dolar_blue() == -1:
            await ctx.send('Ocurrió un error.')
            return
        compra, venta, act = dlr.valor_dolar_blue()
        embedVar = discord.Embed(title="Precio Dolar", url="https://www.dolarhoy.com/cotizaciondolarblue",
                                 color=0x0400ff)
        embedVar.add_field(name="Compra", value=f"${compra}", inline=False)
        embedVar.add_field(name="Venta", value=f"${venta}", inline=False)
        embedVar.set_footer(text=f"Última actualizacion: {act}")
        await ctx.send(embed=embedVar)

    @commands.command(brief='Convierte dolares a pesos',
                      help='Convierte dolares a pesos, toma como argumento un numero. Por ejemplo: .dolarapeso 100')
    async def dolarapeso(self, ctx, dolares: float):
        venta = dlr.valor_dolar_blue()[1]
        await ctx.send(f'${round(venta * dolares)}')

    @dolarapeso.error
    async def dolarapeso_error(self, ctx, error):
        error = getattr(error, "original", error)
        if isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
            await ctx.send('Tenés que darme un número como argumento, por ejemplo: .dolarapeso 100')
            return
        if isinstance(error, discord.ext.commands.errors.BadArgument):
            await ctx.send('Tenés que darme un número como argumento, por ejemplo: .dolarapeso 100')
            return
        if isinstance(error, OverflowError):
            await ctx.send('¿Tantos dolares tenés? ¿O solo me estas boludeando?')
            return
        raise error


def setup(client):
    client.add_cog(Cotizacion(client))
