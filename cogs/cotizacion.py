import discord
from discord.ext import commands
import dolar as dlr

class Cotizacion(commands.Cog):

    def __init__(self,client):
        self.client=client

    @commands.command(brief='Cotización dolar',help='Este comando te brinda informacion actualizada sobre el valor del dolar.')
    async def dolar(ctx):
        if dlr.valor_dolar_blue()==-1:
            await ctx.send('Ocurrió un error.')
            return
        compra,venta,act=dlr.valor_dolar_blue()
        embedVar = discord.Embed(title="Precio Dolar",url="https://www.dolarhoy.com/cotizaciondolarblue",color=0x0400ff)
        embedVar.add_field(name="Compra", value=f"${compra}", inline=False)
        embedVar.add_field(name="Venta", value=f"${venta}", inline=False)
        embedVar.set_footer(text=f"Última actualizacion: {act}")
        await ctx.send(embed=embedVar)

    @commands.command()
    async def dolarapeso(ctx,dolares=None):
        try:
            dolares=float(dolares)
        except ValueError:
            await ctx.send('Ingresá un numero.')
            return
        except TypeError:
            await ctx.send('¿Cuantos dolares queres convertir a pesos?')
            return
        venta=dlr.valor_dolar_blue()[1]
        await ctx.send(f'${round(venta*dolares)}')

def setup(client):
    client.add_cog(Cotizacion(client))