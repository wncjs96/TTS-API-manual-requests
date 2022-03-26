# bot.py
import os
import re
# TODO: asyncio.sleep
import time

import discord
import client as cc
from threading import *

from dotenv import load_dotenv, find_dotenv
import urllib
import json
import asyncio

load_dotenv()
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
#GUILD = os.getenv('DISCORD_GUILD')
GUILD = 'KuroMouse'

count = 0
intents = discord.Intents.all()
path = 'D:\\py_typecast_typer\\TTS-API-manual-requests\\src\\assets\\' 
client = discord.Client(intents=intents)

lock = Lock()

def genAudio(text,voice_client):
	global count
	lock.acquire()
	
	cc.generate_audio(text, count, 'MIO')	
	filename = path + 'temp' + str(count) + '.wav'
	voice_client.play(discord.FFmpegPCMAudio(path + 'temp' + str(count)+'.wav'))
	#sleep(5000)	
	#with audioread.audio_open(path) as f:
	#	sleep(f.duration)
	#player = voice_client.create_ffmpeg_player(filename, after=lambda: print('Audio played'))
	#player.start()

	#while not player.is_done():
	#	time.sleep(1)
	#player.stop()
	
	count = count + 1
	if (count >= 9):
		count = 0
		cc.clearfiles()
	lock.release()
	return	


@client.event
async def on_ready():
	print(f'Discord bot has successfully been connected!')
	for g in client.guilds:
		# Top to bottom text channels within the "guilds"
		if g.name == GUILD:
			break
		print (f'{client.user} connected to {g.name}(id: {g.id})')

@client.event
async def on_message(message):
	if message.author == client.user:
		return
	# collection of msg sent
	msgCollection = []
	if message.content.startswith('\''):
		print('Bot received a message!')
		arg = (' ').join(message.content.split(' ')[1:])
		# check whether a bot is in a voice channel of the sender or not, if they're in the same voice channel, disregard the next step and move onto outputting the wav
		connected = message.author.voice
		if connected:
			voice_client = discord.utils.get(client.voice_clients, guild=message.guild)
			if voice_client:	
				await voice_client.disconnect()			
				print('Disconnected.')

			voice_client = await connected.channel.connect(timeout=60.00)
			#generate first
			t1 = Thread(target = genAudio, args=(arg,voice_client,))
			t1.start()
			#output wav
		else:
			await message.channel.send('The user has to be in a voice channel for the bot to join!')
		
	#return	

		
client.run(DISCORD_TOKEN)

		
	
