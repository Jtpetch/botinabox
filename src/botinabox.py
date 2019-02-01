import discord
import asyncio
import sys
import os
from datetime import datetime
import json
import random
from wolfinaboxutils.system import script_dir
from wolfinaboxutils.formatting import truncate
from utils import loadConfig, default_config, alias_get
from storage import *
from general_commands import commands as g_commands
#GLOBALS===========================#
client = None
clientID = 'id_here'
sClasses = {}
config = {}
commandDict = {**g_commands}
responses = {('thanks', 'thank', 'thx', 'tnx', 'thnx'):
             ('You\'re quite welcome!', 'Aw, no prob!', '\:)'),
             ('sad', ':(', '\:('):
             ('Awh, I\'m sorry \\:(')}


class Client(discord.Client):
    # When the bot starts
    async def on_ready(self: discord.Client):
        print('Succesfully logged in:')
        print('Name: '+self.user.name)
        print('ID: '+self.user.id)
        await self.change_presence(status=discord.Status.online, game=discord.Game(name=config['status']))
        print('Status set to: \"' + config['status'] + '\"')
        # Opus
        if discord.opus.is_loaded():
            print('Opus Codecs Loaded Successfully!')
        else:
            print('WARN: Opus Codecs Not Loaded!')
        # JSON Path
        if not os.path.exists(os.path.join(script_dir(), 'resources', 'servers')):
            print('Creating resources directory...')
            os.makedirs(os.path.join(script_dir(), 'resources', 'servers'))

        # Set up servers
        print('Servers:')
        # For every server the client is on

        for server in self.servers:
            # Try to load it
            temp = load_server(server.id)
            # If it was loaded
            if temp:
                sClasses[server.id] = temp
                print('  Loaded: "'+server.name+'", '+server.id)
            # Otherwise, make a new server class
            else:
                sClasses[server.id] = ServerClass(
                    server.id)  # Make association
                print('  Created: "'+server.name+'", '+server.id)

            print('    Members: '+str(server.member_count))
            save_server(sClasses[server.id])
            # saveServer(sClasses[server.id])
            print('------')

        elapsedTime = datetime.now() - startTime
        print('Bot started successfully! Took ' + str(elapsedTime.seconds) +
              '.' + truncate(str(elapsedTime.microseconds), 2) + ' seconds')
        print('------------------')

    # When we get a message
    async def on_message(self: discord.Client, message: discord.message.Message):
        beginTime = datetime.now()

        # If the message belongs to the bot, ignore it
        if message.author == self.user:
            return

        # We can't handle PM's just yet, so any message with no server should be
        # given a default response
        if message.server is None:
            await client.send_typing(message.channel)
            await self.send_message(message.channel,
                                    'Hi there '+message.author.name+'!\nI can\'t respond to direct messages right now \\:( so just mention me on a server I\'m in!')
            return

        # Parse the message
        sClass: ServerClass = sClasses[message.server.id]
        try:

            # If it's address to us
            if message.content.strip().startswith(sClass.commandPrefix) or self.user.mentioned_in(message):
                # Send typing so we're "thinking"
                await client.send_typing(message.channel)
                # Remove the command character and/or our mention
                message.content = (message.content.replace(
                    self.user.mention, '', 1).replace(sClass.commandPrefix, '', 1)).strip()
                # If there were no arguments
                if len(message.content.split()) == 0:
                    await commandDict['help']['function'](client=self, message=message, sClass=sClass, commandDict=commandDict)
                    return
                command = message.content.split()[0]
                # Try to get a talking response (if possible)
                try_alias_response = None
                for s in message.content.split():
                    r = alias_get(s, responses)
                    if r is not None:
                        try_alias_response = r
                        break

                # It's a regular command (may or may not be valid)
                if command in commandDict.keys():
                    await commandDict[command]['function'](client=self, message=message, sClass=sClass, commandDict=commandDict)
                # They're "talking" to the bot (give a cheeky response)
                elif self.user.mentioned_in(message) and try_alias_response is not None:
                    await client.send_message(message.channel, random.choice([try_alias_response] if type(try_alias_response) not in (list,tuple,set) else try_alias_response))

        except CommUsage as e:
            usage_msg = '`'+sClass.commandPrefix + \
                command+'`'+commandDict[command]['usage']
            await client.send_message(message.channel, usage_msg)


# Start bot
startTime = datetime.now()
try:
    # load Config
    config = loadConfig()
    client = Client()
    client.run(config['token'])
except discord.LoginFailure as e:
    client.logout()
    print('The bot token in "config.json" appears to be incorrect. Please double-check that you used the correct\nbot id from https://discordapp.com/developers/applications/.')
    input('Press return to exit...')
    sys.exit(-1)
except FileNotFoundError as e:
    client.logout()
    print("Couldn\'t  open config file. (If this is the first run, that\'s okay!)\nPlease edit \"config.json\", and set the token to your bot token acquired from:\nhttps://discordapp.com/developers/applications/\nThen restart the script.")
    json.dump(default_config, open(os.path.join(
        script_dir(), 'config.json'), 'w'), indent=4)
    input('Press return to exit...')
    sys.exit(-1)
except Exception as e:
    client.logout()
    print('I can\'t connect to the Discord servers right now, sorry! :(\nCheck your internet connection, and then https://twitter.com/discordapp for Discord downtimes,\n and then try again later.')
    input('Press return to exit...')
    sys.exit(-1)
# END DISCORD CODE
