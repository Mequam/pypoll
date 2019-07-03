#!/bin/python
import discord
from discord.ext import commands
from time import sleep
import DGui
print(discord.version_info)

def sortDict(dicti):
	#this is a generic function that returns a sorted dictionary of a given dictionary
	#it is designed to be used with the array of emojis inside of the poll class
	ret_arr = []
	for word in dicti:
		ret_arr.append((dicti[word],word))	
	ret_arr.sort(reverse=True)
	return ret_arr

class poll(DGui.gui):
	polls = []
	def __init__(self,name,question,options):	
		self.name = name
		self.question = question

		#options is a list of tuples where the first tupple is the text you want to vote for
		#and the second is the reaction emoji that you use
		self.options = options	
		self.votes = {}
		for emoji in options:
			#initilize the voting options
			self.votes[emoji] = 0
		
		emojiL = []
		for emoji in options:
			emojiL.append(emoji)
		#run the main init of the gui class for the poll
		DGui.gui.__init__(self,emojiL)	
		self.voters = []
		self.windows += [poll.promptWind,poll.listVotes]
		self.revote = True

		poll.polls.append(self)

	def promptWind(self):
		ret_val = ''
		if self.name != None:
			ret_val += self.name + ':\n\n'
		ret_val += self.question
		return ret_val
	def listVotes(self):
		#this is a window function that displays the things to vote for 
		ret_val = 'votes:\n'	
		votes = sortDict(self.votes)
		for vote in votes:
			ret_val += self.options[vote[1]] + ':' + vote[1] + ' ' + str(vote[0]) + '\n'
		return ret_val[:-1]
	def toStr(self):
		#this will need to be replaced with the window function
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
		for i in range(0,len(self.voters)):
			if self.voters[i][0] == author_id:
				if self.voters[i][1] == emoji:
					#they attempted to vote for the same thing twice
					return False
				elif self.revote == True:
					self.votes[emoji] += 1
					self.votes[self.voters[i][1]] -= 1
					self.voters[i][1] = emoji
					return True
		if emoji in self.votes:
			print('[*] voting as ' + str(author_id))
			self.votes[emoji] += 1
			print('[*] ' + str(self.votes))
			self.voters.append([author_id,emoji])
			return True
		else:
			return False
	def update(self,reaction,user):
		#on update add the given vote to the user
		return self.addVote(reaction.emoji,user.id)
	def getPollName(name):
		for p in poll.polls:
			if p.name == name:
				return p
		return None
class Lister(DGui.gui):
	def __init__(self,emojiL):
		DGui.gui.__init__(self,emojiL)	
		self.index = 0
		self.windows.append(Lister.listpolls)
	def listpolls(self):
		ret_val = ''
		sl = poll.polls[self.index:self.index+5]
		for i in range(0,len(sl)):
			ret_val +=  str(i+1) + ':' + sl[i].name + '\n'
		return ret_val[:-1]
	def update(self,reaction,user):
		if reaction.emoji == '➕':
			#they want to incriment the index
			self.index = (self.index + 5) % len(poll.polls)
		elif reaction.emoji == '1⃣':
			print('update returning ' + str(poll.polls[self.index].Id))			
			return poll.polls[self.index].Id		
lister = Lister(['1⃣','2⃣','3⃣','4⃣','5⃣','➕'])
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
	fields = {}
	for arg in args[2:]:
		split_a = arg.split(':')
		if len(split_a) > 1:
			fields[split_a[1]] = split_a[0]
	p = poll(args[0],args[1],fields)
	await p.addSelf(ctx)	
@bot.command()
async def listPolls(ctx,*args):
	await lister.add(ctx)
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
	#check the gui	
	print(reaction.emoji)
	await DGui.checkGui(clientId,reaction,user)
bot.run(get_token())
#we need to find a way to allow ppl to chose with reactions
