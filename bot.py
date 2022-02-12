import os
import datetime
import asyncio

import discord
import feedparser


TOKEN = os.environ['BOT_TOKEN'] # your bot token
CHANNEL_ID = int(os.environ['BOT_CHANNEL_ID']) # your discord channel id
RSS = os.environ['BOT_RSS'] # "https://www.x-null.net/forums/external.php?type=rss2&lastpost=1"
WAITTIME = 60*5 # time to wait between each check in seconds

async def loop():
    last_entries = []

    while True:
        print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "Checking for new posts...")

        d = feedparser.parse(RSS)

        if d.entries:
            if last_entries and d.entries[0].published != last_entries[0].published:
                print("New post found:", d.entries[0].title, "made by", d.entries[0].author, "-", d.entries[0].published)
                await embed(d)
            else:
                pass # No new posts found

            last_entries = d.entries
        else:
            print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "xNULL is down")

        await asyncio.sleep(WAITTIME)

async def embed(d):
    embed = discord.Embed(
        title=d.entries[0].title,
        url=d.entries[0].link,
        colour=discord.Colour.blue(),
        timestamp=datetime.datetime.utcnow()
    )
    embed.add_field(name=f"{d.entries[0].author} posted in: {d.entries[0].title}", value=d.entries[0].description, inline=False)
    embed.set_footer(text=f"Posted by {d.entries[0].author}")

    channel = client.get_channel(CHANNEL_ID)
    await channel.send(embed=embed)

class Client(discord.Client):
    async def on_ready(self):
        print(f"Logged on as {self.user}!")
        await loop()

client = Client()
client.run(TOKEN)
