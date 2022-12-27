import json
import requests
import os
from dotenv import load_dotenv

import discord
from discord.ext import commands, tasks
from discord.utils import get

class Notifications(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Notifications Cog Ready!")
        self.checkforvideos.start()

    async def cog_load(self):
        self.checkforvideos.start()

    async def cog_unload(self):
        self.checkforvideos.stop()

    @tasks.loop(minutes=15)
    async def checkforvideos(self):
        guild = await self.bot.fetch_guild(self.bot.global_config['guild_id'])
        
        with open("youtubedata.json", "r") as f:
            data=json.load(f)
    
        YT_API_KEY = os.getenv('YT_API_KEY')

        for youtube_channel in data:
            channel = f"https://www.googleapis.com/youtube/v3/search?key={YT_API_KEY}&channelId={youtube_channel}&part=snippet,id&order=date&maxResults=1"

            response = requests.get(channel)
            response = response.json()

            video_id = response["items"][0]['id']["videoId"]
            latest_video_url = f"https://www.youtube.com/watch?v={video_id}"

            previous_video = data[youtube_channel]["latest_video_url"]

            if not str(data[youtube_channel]["latest_video_url"]) == latest_video_url:

                data[str(youtube_channel)]['latest_video_url'] = latest_video_url

                with open("youtubedata.json", "w") as f:
                    json.dump(data, f)

                annonces_channel: discord.TextChannel = await self.bot.fetch_channel(self.bot.global_config['annonces_channel'])  
                
                msg = f"{guild.default_role} Just Uploaded A Video Or He is Live Go Check It Out: {latest_video_url}"
                await annonces_channel.send(msg)

async def setup(client):
  await client.add_cog(Notifications(client))