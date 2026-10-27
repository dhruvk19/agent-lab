import os
import asyncio
import discord
from dotenv import load_dotenv
from agent import run_agent, system_prompt

load_dotenv()
TOKEN = os.environ["DISCORD_TOKEN"]
OWNER_ID = int(os.environ["OWNER_ID"])
MAX_HISTORY = 20

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
history = {}

@client.event
async def on_ready():
    print(f"Logged in as {client.user}")

@client.event
async def on_message(message):
    if message.author.id != OWNER_ID:
        return
    text = message.content.strip()
    if not text:
        return
    chan = history.setdefault(message.channel.id, [])
    if text.lower() == "!reset":
        chan.clear()
        await message.channel.send("Memory cleared.")
        return
    work = [{"role": "system", "content": system_prompt()}] + chan + [{"role": "user", "content": text}]
    async with message.channel.typing():
        try:
            reply = await asyncio.to_thread(run_agent, work)
        except Exception as e:
            reply = f"Something went wrong: {e}"
    reply = reply or "(no reply)"
    chan += [{"role": "user", "content": text}, {"role": "assistant", "content": reply}]
    del chan[:-MAX_HISTORY]
    for i in range(0, len(reply), 1900):
        await message.channel.send(reply[i:i + 1900])

client.run(TOKEN)
