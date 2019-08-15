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
		self.revote = False
		
		self.perc = False	
		self.noName = True
		poll.polls.append(self)
		
	def promptWind(self):
		ret_val = ''
		if not self.noName:
			ret_val += self.name + ':\n\n'
		ret_val += self.question
		return ret_val
	def showVoters(self):
		ret_val = 'these people have voted\n\n'
		for name in self.voters:
			ret_val += name[2] + ' '		
		return ret_val

	def listVotes(self):
		#this is a window function that displays the things to vote for 
		ret_val = 'votes:\n'
		print(self.votes)	
		votes = sortDict(self.votes)
		if self.perc:
			total = 0
			for vote in votes:
				total += vote[0]
		
		for vote in votes:
			ret_val += self.options[vote[1]] + ':' + vote[1] + ' '
			if self.perc:
				if total == 0:
					ret_val += '0%'
				else:
					ret_val += str((vote[0]/total)*100) + '%'
			else:
				ret_val += str(vote[0])
			ret_val += '\n'
		return ret_val[:-1]
	def addVote(self,emoji,author_id,username=None):
		#this function takes an emoji and mapps it to the votes	
		for i in range(0,len(self.voters)):
			print(self.voters)
			if self.voters[i][0] == author_id:
				if self.voters[i][1] == emoji:
					#they attempted to vote for the same thing twice
					return False
				elif self.revote == True:
					self.votes[emoji] += 1
					self.votes[self.voters[i][1]] -= 1
					self.voters[i][1] = emoji
					return True
				#their not allowed to revote
				return False
		if emoji in self.votes:
			print('[*] voting as ' + str(author_id))
			self.votes[emoji] += 1
			print('[*] ' + str(self.votes))
			self.voters.append([author_id,emoji,username])
			return True
		else:
			return False
	def update(self,reaction,user):
		#on update add the given vote to the user
		return self.addVote(reaction.emoji,user.id,user.name)
	def getPollName(name):
		for p in poll.polls:
			if p.name == name:
				return p
		return None
class Lister(DGui.gui):
	def __init__(self,emojiL):
		DGui.gui.__init__(self,emojiL)	
		self.index = 0
		self.id = 0
		self.windows.append(Lister.listpolls)
	def listpolls(self):
		ret_val = ''
		sl = poll.polls[self.index:self.index+5]
		for i in range(0,len(sl)):
			ret_val +=  str(i+1) + ':' + sl[i].name + '\n'
		return ret_val[:-1]
	def update(self,reaction,user):
		if user.id != self.id:
			return True
		if reaction.emoji == '➡':
			#they want to incriment the index
			self.index += 5
			if self.index > len(poll.polls):
				#start around at the begining if we go over
				self.index = 0
			return True
		elif reaction.emoji == '⬅':
			self.index -= 5
			if self.index < 0:
				self.index = len(poll.polls) - 1
			return True
		elif reaction.emoji == '1⃣':
			print('update returning ' + str(poll.polls[self.index].Id))			
			return poll.polls[self.index].Id
		elif reaction.emoji == '2⃣':
			return poll.polls[self.index+1].Id
		elif reaction.emoji == '3⃣':
			return poll.polls[self.index+2].Id
		elif reaction.emoji == '4⃣':
			return poll.polls[self.index+3].Id
		elif reaction.emoji =='5⃣':
			return poll.polls[self.index+4].Id	
		else:
			return True
class Helper(DGui.gui):
	def __init__(self,emojiL):
		Lister.__init__(self,emojiL)
		self.index = 0

		#this is the index of the help page that we want to view
		self.page = 0
		self.windows = [Helper.listpages,Helper.showPage]
		self.pages = []
	def listpages(self):
		ret_val = ''
		sl = self.pages[self.index:self.index+5]
		for i in range(0,len(sl)):
			ret_val +=  str(i+1) + ':' + sl[i][0] + '\n'
		return ret_val[:-1]
	def showPage(self):
		ret_val = (' ' * 2) + self.pages[self.page][0] + '\n' + (' - ' * 6) + '\n'
		ret_val += self.pages[self.page][1]
		return ret_val
	def update(self,reaction,user):
		if reaction.emoji == '➡':
			#they want to incriment the index
			self.index += 5
			if self.index > len(self.pages):
				#start around at the begining if we go over
				self.index = 0
			return True
		elif reaction.emoji == '⬅':
			self.index -= 5
			if self.index < 0:
				self.index = len(self.pages) - 1
			return True
		elif reaction.emoji == '1⃣':
			self.page = self.index
		elif reaction.emoji == '2⃣':
			if self.index + 1 < len(self.pages):
				self.page = self.index+1
		elif reaction.emoji == '3⃣':
			if self.index + 2 < len(self.pages):
				self.page = self.index+2
		elif reaction.emoji == '4⃣':
			if self.index + 3 < len(self.pages):
				self.page = self.index+3
		elif reaction.emoji =='5⃣':
			if self.index + 4 < len(self.pages):
				self.page = self.index+4	
		return True
lister = Lister(['⬅','1⃣','2⃣','3⃣','4⃣','5⃣','➡'])
helper = Helper(['⬅','1⃣','2⃣','3⃣','4⃣','5⃣','➡'])
helper.pages.append(['help - summon this help page','click the number you want to select and the arrows to move around\nits that simple! '])
helper.pages.append(['addpoll - add a poll to the list of active polls',
'''
general:
	this command takes a list of flags for how the poll should be conducted
	followed by the question that the poll wants to ask and a list of options and emojies
	people to vote on
syntax:
	addpoll [flags] <"poll text"> [option:emoji [option:emoji [option:emoji...]]]
	
	flags
	----------
	-name		set the poll name for the poll list, defaults to the desc if not specified
	-perc		toggles percentile output for the votes
	-revote		allows voters to change their vote
	-showvote	shows who voted (but not for what)

examples:
	say we want to make a poll where we vote on everyones favorite apple
	we could use the following example:
	
		addpoll "what is your favorite apple color" green::green_apple: red::apple:
	
	now anyone can vote for an apple color, but be careful! once you vote with
	this poll you cannot change your vote! 
	
	since apples are really no big deal, and it wont hurt anything to let people 
	change their vote after the fact we'll add the following flag to our command
		
		addpoll -revote "what is your favorite apple color" green::green_apple: red::apple:
	
	so now that flags effect takes place on the vote and any person who wants to change their vote 
	can go ahead and do that

	any of the flags listed above can be added this way (and any number of them too!) 
	so long as they are placed BEFORE the text description of the vote
'''])
helper.pages.append(['listpolls - list and summon polls',
'''general:
	this command is used to list the polls that are currently active
	and to pull up their gui so you can still vote on them even if you were not
	their when they were made
syntax:
	listpolls
	
	once you have the gui their simply use the numbers to select the poll that you want
	and the arrows to scroll between polls that exist

NOTE: once a poll is selected it will replace the list gui 
'''])
helper.pages.append(['ping - ping the bot','make sure the bot is online with a friendly game of ping pong'])
def get_token(fname='discord_token.txt'):
	f = open(fname,'r')
	token = f.readline()
	f.close()
	return token[:-1]
	
bot = commands.Bot(command_prefix='pypoll ')
bot.remove_command('help')
clientId = int(get_token('client.txt'))

@bot.command()
async def addpoll(ctx,*args):
	#the next command will be the message to place

	#these are flags this command accepts
	flags = ['-name','-revote','-showvote','-perc']
	name = None
	perc = False
	showvote = False
	revote = False
	i = 0
	while i < len(args):
		#make a custom for loop so we can skip values we find
		if args[i] not in flags:
			#we found the question, leave our lovely little loop
			question = args[i]
			break
		elif args[i] == '-name':
			#print('[DEBUG] found -name')
			if len(args) > i + 1:
				name = args[i + 1]
			#	print('[DEBUG] incrimenting i')
				i += 1
		elif args[i] == '-revote':
				revote = True
		elif args[i] == '-showvote':
				showvote = True
		elif args[i] == '-perc':
				perc = True
		i+= 1
	noName = False
	if name == None:
		name = question.split('\n')[0]
		noName = True
	fields = {}
	for arg in args[i:]:
		split_a = arg.split(':')
		if len(split_a) > 1:
			fields[split_a[1]] = split_a[0]
	p = poll(name,question,fields)
	p.revote = revote
	print(p.revote)
	if showvote:
		p.windows.append(poll.showVoters)
	p.perc = perc
	p.noName = noName
	await p.addSelf(ctx)	
@bot.command()
async def listpolls(ctx,*args):
	lister.id = ctx.author.id
	await lister.add(ctx)
@bot.command()
async def help(ctx,*args):
	helper.id = ctx.author.id
	await helper.add(ctx)
@bot.command()
async def ping(ctx):
	await ctx.send('pong')
@bot.event
async def on_ready():
	print('[*] connected to discord!')
@bot.event
async def on_reaction_add(reaction, user):
	#check the gui	
	print(reaction.emoji)
	await DGui.checkGui(clientId,reaction,user)
bot.run(get_token())
