import os
import sys
from utils import *
#Perms
#These are to allow only very specific users to run "backend commands"
dev_IDs=['398022816408141854']
#Util stuff
script_dir = os.path.dirname(sys.executable) if getattr(sys,'frozen',False) else os.path.dirname(__file__)
isExecutable = getattr(sys,'frozen',False)
#Defaults
defaultCommandPrefix='&'
defaultLogChannelName='logs'
defaultHelpText="""***BotInABox Helpfile, v1.0.0***
**<=======================================================>**
$generalCommands$
$adminCommands$
$customCommands$
$devCommands$
**<=======================================================>**"""
defaultMotd="""**/\\/\\/\\$serverName$ Message Of The Day $date$/\\/\\/\\**
**<======================================================>**
Remember to always keep as __positive__ as possible!"""