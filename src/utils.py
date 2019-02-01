import json
import os
from wolfinaboxutils.system import script_dir
# Perms
# These are to allow only very specific users to run "backend commands"
dev_IDs = ['398022816408141854']
# Defaults
defaultCommandPrefix = '&'
# defaultLogChannelName='logs'

defaultHelpText = """***$bot_name$ Helpfile, v2.0.0***
**<===================================================================>**
*Either use the command prefix ("$comm_prefix$help"), or mention me ("$bot_mention$ help")to run a command!*
$general_commands$
$admin_commands$
$dev_commands$
$custom_commands$
**<===================================================================>**"""
defaultMotd = """**/\\/\\/\\$serverName$ Message Of The Day $date$/\\/\\/\\**
**<======================================================>**
Have a fantastic day!"""

default_config = {'token': 'bot_token_here','status':'Mention me for help!'}
# Functions


def loadConfig(location: str = os.path.join(script_dir(), 'config.json')):
    """
    Loads the bot's config from the supplied config json file.
    :returns: The loaded config object
    :throws: FileNotFoundError, if token.txt file not found
    """
    return json.load(open(location))


def format_replace(s, **kwargs):
    """
    Format strings to replace inset variables (eg: "$bot_name$" -> "Botinabox")\n
    <s> : String to format\n
    <**kwargs> : A dictionary of variable:replacement pairs.\n
    Default replacements: $bot_name$, $bot_mention$, $general_command$, $admin_commands$, $custom_commands$, $dev_commands$, $comm_prefix$
    """
    replaced = -1
    while replaced != 0:
        replaced = 0
        for key, val in kwargs.items():
            replaced += ('$'+key+'$' in s)
            s = s.replace('$'+key+'$', val)
    return s


def case_insens_replace(string: str, search: str, replacement: str):
    """
    Replace any instance of <search> in <string> with <replacement>, regardless of case.\n
    <string> The string to search in\n
    <search> The string to replace
    <replacement> The string to replace with.\n
    If <replacement> contains $orig$, $orig$ will be substituted for the original string found.
    """
    from pyparsing import CaselessLiteral, originalTextFor
    expr = CaselessLiteral(search)
    res = originalTextFor(expr, asString=True).searchString(string)
    for r in res:
        repl = format_replace(replacement, orig=r[0])
        string = string.replace(r[0], repl)
    return string


def alias_get(alias,dictionary:dict):
    """
    For a dictionary with tuples as keys, get the value at the key that contains the given alias.\n
    <alias> The alias to search for\n
    <dictionary> The dict to search through
    """
    for key,val in dictionary.items():
        if alias in key:
            return val