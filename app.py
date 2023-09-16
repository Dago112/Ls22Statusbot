import discord
import asyncio
import requests

intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)

# Die URL der API des Landwirtschafts Simulator Servers, die die Spielerinformationen bereitstellt
LS_SERVER_API_URL = "http://example.com/api/players"

@client.event
async def on_ready():
    print(f'{client.user} is connected to Discord!')
    asyncio.get_event_loop().create_task(status_task())
    asyncio.get_event_loop().create_task(players_task())

async def status_task():
    await client.wait_until_ready()
    while not client.is_closed():
        try:
            response = requests.get('link zum server)
            server_status = response.text
            channel = client.get_channel(replace channel_id) # replace channel_id with the id of the desired channel
            if 'online' in server_status:
                await channel.send('🟢 Server is online.')
            else:
                await channel.send('🔴 Server is offline.')
            await asyncio.sleep(3600) # wait 20 minutes
        except requests.exceptions.RequestException:
            channel = client.get_channel(replace channel_id) # replace channel_id with the id of the desired channel
            await channel.send('🔴 Server ist nicht erreichbar.')
            await asyncio.sleep(900) # wait 5 minutes

async def players_task():
    await client.wait_until_ready()
    while not client.is_closed():
        try:
            response = requests.get(LS_SERVER_API_URL)
            players = response.json()
            channel = client.get_channel(1) # replace channel_id with the id of the desired channel
            player_names = ", ".join([player['name'] for player in players])
            await channel.send(f"👥 {len(players)} Spieler online: {player_names}")
            await asyncio.sleep(600) # wait 10 minutes
        except requests.exceptions.RequestException:
            channel = client.get_channel(1102) # replace channel_id with the id of the desired channel
            await channel.send('🔴 Spielerinformationen konnten nicht abgerufen werden.')
            await asyncio.sleep(900) # wait 5 minutes

@client.event
async def on_message(message):
    if message.content.startswith('!kick'):
        user = message.mentions[0]
        if user == message.author:
            await message.channel.send("❌ Du kannst dich nicht selbst kicken.")
            return
        if user.guild_permissions.administrator:
            await message.channel.send("❌ Du kannst keinen Administrator kicken.")
            return
        await user.kick()
        await message.channel.send(f"👢 {user.name} wurde gekickt.")

    if message.content.startswith('!ban'):
        user = message.mentions[0]
        if user == message.author:
            await message.channel.send("❌ Du kannst dich nicht selbst bannen.")
            return
        if user.guild_permissions.administrator:
            await message.channel.send("❌ Du kannst keinen Administrator bannen.")
            return
        await user.ban()
        await message.channel.send(f"🔨 {user.name} wurde gebannt.")

client.run('TOKEN')
