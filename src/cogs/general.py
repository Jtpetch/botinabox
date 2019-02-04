import discord
from discord.ext import commands
import datetime
import psutil
import os
from wolfinaboxutils.formatting import truncate
class General:
    def __init__(self, bot:commands.Bot):
        self.bot = bot

    @commands.command(name='ping')
    async def ping(self,ctx:commands.Context):
        res_msg=await ctx.send('Pong!')
        time_diff=res_msg.created_at-ctx.message.created_at
        await res_msg.edit(content=f'Pong! ({time_diff.seconds}.{truncate(str(time_diff.microseconds),3)}s)')

    @commands.command(name='sysinfo',aliases=['status'])
    async def sysinfo(self,ctx:commands.Context):
        def size_conv(size):
            #2**10 = 1024
            power = 2**10
            n = 0
            Dic_powerN = {0 : '', 1: 'k', 2: 'm', 3: 'g', 4: 't'}
            while size > power:
                size /=  power
                n += 1
            return str(round(size,2))+str(Dic_powerN[n]+'b')
        msg='**Bot System Usage Info:**\n'
        process = psutil.Process(os.getpid())
        process.cpu_percent(interval=1)
        msg+=f'**CPU**: Bot: {process.cpu_percent()}%, Total: {psutil.cpu_percent()}%\n'
        used_mem=size_conv(psutil.virtual_memory().used)
        total_mem=size_conv(psutil.virtual_memory().total)
        msg+=f'**Memory**: Bot: {size_conv(process.memory_info().rss)}, Total: {used_mem}/{total_mem}'
        await ctx.send(msg)

def setup(bot):
    bot.add_cog(General(bot))