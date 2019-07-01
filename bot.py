#!/bin/python
import discord
from discord.ext import commands
from time import sleep
print(discord.version_info)

def sortDict(dicti):
	#this is a generic function that returns a sorted dictionary of a given dictionary
	#it is designed to be used with the array of emojis inside of the poll class
	ret_arr = []
	for word in dicti:
		ret_arr.append((dicti[word],word))	
	ret_arr.sort(reverse=True)
	return ret_arr
class poll:
	#this is a global array that is shared by each poll object
	polls = []
	def __init__(self,name,question,options):
		self.name = name
		self.prompt = 'poll-' + self.name + ':'
		self.question = question
		
		#options is a list of tuples where the first tupple is the text you want to vote for
		#and the second is the reaction emoji that you use
		self.options = options	
		self.votes = {}
		for option in options:
			#initilize the voting options
			self.votes[option[1]] = 0
		
		self.voters = []
		self.polls.append(self)
	def toStr(self):
		ret_val = self.prompt + '\n'
		ret_val += '---------------------' + '\n\n\t\t'
		split_q = self.question.split('\n')
		for q in split_q:
			ret_val += q + '\n' + '\t\t'
		tList = sortDict(self.votes)
		ret_val += '\n---------------------\nvotes: '
		for tup in tList:
			ret_val += tup[1] + ':' + str(tup[0]) + ' '
		return ret_val
	def addVote(self,emoji,author_id):
		#this function takes an emoji and mapps it to the votes
		print('[*] running the voting function\n' + '-'*10)
		if author_id in self.voters:
			print(str(author_id) + ' has already voted')	
			return False	
		elif emoji in self.votes:
			print('[*] voting as ' + str(author_id))
			self.votes[emoji] += 1
			print('[*] ' + str(self.votes))
			self.voters.append(author_id)
			return True
		else:
			return False  
	def getPollName(name):
		for p in poll.polls:
			if p.name == name:
				return p
		return None
def get_token(fname='token.txt'):
	f = open(fname,'r')
	token = f.readline()
	f.close()
	return token[:-1]
	
bot = commands.Bot(command_prefix='pollPy ')
clientId = int(get_token('client.txt'))
@bot.command()
async def addPoll(ctx,*args):
	#the next command will be the message to place
	fields = []
	for arg in args[2:]:
		split_a = arg.split(':')
		if len(split_a) > 1:
			fields.append((split_a[0],split_a[1]))
	p = poll(args[0],args[1],fields)
	msg = await ctx.send(p.toStr())
	for react in p.options:
		await msg.add_reaction(react[1])
	#await ctx.send('added poll!')
@bot.command()
async def listPolls(ctx,*args):
	resp = ''
	for p in poll.polls:
		#dont await a bunch of responces, add them to a variable and then await
		resp += p.name + '\n'
	if len(resp) == 0:
		resp = 'no polls found :(' 
	await ctx.send(resp)
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
@bot.command()
async def summon(ctx,*args):
	sent = ''
	for word in args:
		sent += word + ' '
	#remove the last space
	sent = sent[:-1]
	p = poll.getPollName(sent)
	msg = await ctx.send(p.toStr())
	for react in p.options:
		await msg.add_reaction(react[1])
@bot.event
async def on_ready():
	print('[*] connected to discord!')
@bot.event
async def on_reaction_add(reaction, user):	
	print('COUNT ' + str(reaction.count))
	if reaction.message.author.id == clientId: 
		print('[*] I made that message!')
		
		#this is the syntax that this if statement is looking for
		#poll-<name>:<poll description>	
		if user.id != clientId:	
			split_m = reaction.message.content.split(':')
			if len(split_m[0]) > 5 and len(split_m) > 1 and split_m[0].split('-')[0] == 'poll':
				#we have a valid poll
				p = poll.getPollName(split_m[0].split('-')[1])
				p.addVote(reaction.emoji,user.id)
				
				#update the poll
				#TODO: need to update every message in the cache that changes so all polls are up to date
				if reaction.count > 1:
					await reaction.message.remove_reaction(reaction.emoji,user)
				#TODO: add a reaciton removal system await reaction.message.remove_reaction(reaction.emoji,'a')
				await reaction.message.edit(content=p.toStr())
			#print(p.votes)
			#print(reaction.message.content)
			

bot.run(get_token())
#we need to find a way to allow ppl to chose with reactions
