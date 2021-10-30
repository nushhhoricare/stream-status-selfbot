import discord, os, keep_alive, asyncio, datetime, json, requests, pyarmor, discord_webhook
from discord.ext import tasks, commands

config = json.load(open('config.json'))

token = config["Token"]
url = config["Stream_Url"]
name = config["Stream_Name"]
def check_token(token: str) -> str:
    if requests.get("https://discord.com/api/v9/users/@me", headers={"Authorization": token}).status_code == 200:
        return "user"
    else:
        return "bot"

token_type = check_token(token)

if token_type == "user":
    headers = {'Authorization': token}
    client = commands.Bot(
        command_prefix=':',
        case_insensitive=False,
        self_bot=True
    )

elif token_type == "bot":
    headers = {'Authorization': f'Bot {token}'}
    client = commands.Bot(
        command_prefix=':',
        case_insensitive=False
    )

client = commands.Bot(
  command_prefix=':',
  self_bot=True
)

@client.event
async def on_connect():
  await client.change_presence(activity = discord.Streaming(name = name, url = url))
keep_alive.keep_alive()

try:
    if token_type == "user":
        client.run(
		token, 
		bot=False
	)
    elif token_type == "bot":
        client.run(token)
except:
    print(f"Connection error. VPNs sometimes are the cause for this or token is incorrect.")
