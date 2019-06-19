import sys
#we can make this WAAAY better in the future, we can add bit math to it and use the argparse library to get some nice smooth parsing
#but for now this is not the problem we are trying to solve, so add a quick fix to save time in the future
print('https://discordapp.com/oauth2/authorize?client_id='+sys.argv[1] + '&scope=bot&permissions=' + sys.argv[2])
