import discord
import asyncio
from functools import partial
import random
from utils import format_replace, defaultHelpText, case_insens_replace, dev_IDs
from storage import CommUsage
from wolfinaboxutils.misc import is_int
from wolfinaboxutils.searches import any_in
commands = {}


# Ping Command
async def gen_comm_ping(client: discord.Client, message: discord.Message, **kwargs):
    await client.send_message(message.channel, 'Pong! ^-^')
commands['ping'] = {'function': partial(gen_comm_ping),
                    'usage': 'Ping to pong!', 'type': 'general'}


# Help Command
async def gen_comm_help(client: discord.Client, message, sClass, commandDict, **kwargs):
    helptext = format_replace(defaultHelpText, bot_name=client.user.name, bot_mention=client.user.mention, comm_prefix=sClass.commandPrefix,
                              general_commands='**General Commands:**\n' +
                              '\n'.join([('`'+sClass.commandPrefix+key+'`: '+info['usage']) for key,
                                         info in commandDict.items() if commandDict[key]['type'] == 'general']),
                              admin_commands='**Admin Commands:**\n' +
                              '\n'.join([('`'+sClass.commandPrefix+key+'`: '+info['usage'])
                                         for key, info in commandDict.items() if commandDict[key]['type'] == 'admin']),
                              dev_commands=('**DEV Commands:**\n' +
                                            '\n'.join([('`'+sClass.commandPrefix+key+'`: '+info['usage'])
                                                       for key, info in commandDict.items() if commandDict[key]['type'] == 'dev'])) if message.author.id in dev_IDs else ''
                              )
    msg = ''
    strings = message.content.split()
    if len(strings) > 1:
        searchText = strings[1].strip()
        for comm, info in commandDict.items():
            if searchText.lower() in comm.lower() or searchText.lower() in info['usage'].lower():
                msg += ('`'+sClass.commandPrefix+comm+'`: ' +
                        case_insens_replace(info['usage'], searchText, '__$orig$__'))
        if not msg:
            msg = 'No results in helptext containing "'+searchText+'"'
    else:
        msg = helptext
    # temp
    await client.send_message(message.channel, msg)
commands['help'] = {'function': partial(gen_comm_help),
                    'usage': '**<search text>**Displays this helptext. Optionally, search helptext for keyword', 'type': 'general'}


# Random Number Command
async def gen_comm_random(client: discord.Client, message: discord.Message, **kwargs):
    formats = ['I choose number **{0}**!', '**{0}** seems good.',
               'Hmmm... What about **{0}**?', 'RANDOM_NUMBER_CHOSEN: #**{0}** (beep boop)']
    strings = message.content.split()
    if len(strings) < 3 or not is_int(strings[1]) or not is_int(strings[2]):
        raise CommUsage(strings[0])
    randNum = random.randint(int(strings[1]), int(strings[2]))
    msg = random.choice(formats).format(str(randNum))
    await client.send_message(message.channel, msg)
commands['random'] = {'function': partial(gen_comm_random),
                      'usage': '**<high> <low>** Generate a random number between high and low', 'type': 'general'}


# Random Choice Command
async def gen_comm_choose(client: discord.Client, message: discord.Message, **kwargs):
    formats = ['I pick "{0}"!', '"{0}" seems good.',
               'Hmmm... What about "{0}"?', 'RANDOM_OPTION_CHOSEN: "{0}" (beep boop)']
    strings = message.content.split(None, 1)
    if len(strings) < 2:
        raise CommUsage(strings[0])
    options = strings[1].split('|')
    if len(options) < 1:
        raise CommUsage(strings[0])
    choice = random.choice(options)
    msg = random.choice(formats).format(choice)
    await client.send_message(message.channel, msg)
commands['choose'] = {'function': partial(gen_comm_choose),
                      'usage': '**<choice1|choice2|choice3|...>** Chooses randomly from the given options', 'type': 'general'}


#Server Stats Command
async def gen_comm_server_stats(client:discord.Client,message:discord.Message,server:discord.Server,**kwargs):
    msg = '**Stats for ' + server.name + ':**\n'