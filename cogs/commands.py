from discord.ext import commands

class Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        print("Commands Cog Ready!")

    @commands.command(name="config")
    @commands.has_permissions(administrator=True)
    async def config(self, ctx):
        bot_channel = self.bot.get_channel(self.bot.global_config['bot_channel'])
        msg_config = ''
        if ctx.channel.id == bot_channel.id:
            for k,v in enumerate(self.bot.global_config):
                msg_config += f"{v} : {self.bot.global_config[v]}\n"
            
            await bot_channel.send(msg_config)    

async def setup(client):
  await client.add_cog(Commands(client))