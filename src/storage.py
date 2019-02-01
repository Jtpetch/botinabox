import json
import os
from utils import defaultCommandPrefix
from utils import script_dir


class ServerClass():
    def __init__(self, id):
        self.id = id
        self.commandPrefix = defaultCommandPrefix
        #self.logChannelName = defaultLogChannelName
        #self.users = {}
        self.customCommands = {}
        #self.logChannel = None


def load_server(id, path: str = os.path.join(script_dir(), 'resources', 'servers')):
    path = os.path.join(path, id+'.json')
    if not os.path.isfile(path):
        return None
    temp = {}
    with open(path, 'r') as f:
        temp = json.load(f)
    sClass = ServerClass(temp['id'])
    sClass.commandPrefix = (
        temp['commandPrefix'] if 'commandPrefix' in temp else defaultCommandPrefix)
    sClass.customCommands = (
        temp['customCommands'] if 'customCommands' in temp else [])
    return sClass


def save_server(serverClass, path=os.path.join(script_dir(), 'resources', 'servers')):
    path = os.path.join(path, serverClass.id+'.json')
    data = {'id': serverClass.id, 'commandPrefix': serverClass.commandPrefix,
            'customCommands': serverClass.customCommands}
    with open(path, 'w') as f:
        json.dump(data, f, indent=4)


class CommUsage(Exception):
    def __init__(self, arg):
        self.sterror = arg
        self.args = {arg}
