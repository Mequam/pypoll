#!/bin/python
import discord
from discord.ext import commands
from time import sleep
print(discord.version_info)
def get_token(fname='token.txt'):
	f = open(fname,'r')
	token = f.readline()
	f.close()
	return token[:-1]
	
bot = commands.Bot(command_prefix='/')
@bot.command()
async def ping(ctx):
	await ctx.send('pong')
@bot.command()
async def test(ctx):	
	print(ctx.message.reactions)
@bot.command()
async def echo(ctx,*args):
	ret_val = ''
	for arg in args:
		ret_val += arg + ' '
	msg = await ctx.send(ret_val)	
	await msg.add_reaction('☺')
	dt = 0
	for i in range(0,10):	
		print('[wating] ' + str(dt) + ' seconds have elapsed...')
		sleep(1)
		dt += 1
	print('[*] Deleting the reaction!')	
	await msg.clear_reactions()
	print('[*] the reaction should be deleted!')
	print('-'*20)
@bot.event
async def on_ready():
	print('[*] the bot is ready to rumble')
@bot.event
async def on_reaction_add(reaction, user):
	print('[*] there was a reaction added!')
bot.run(get_token())
