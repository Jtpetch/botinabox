import discord
from discord.ext import commands
import json
from wolfinaboxutils.system import script_dir
import os
import sys
from typing import Union
import traceback
default_config = {
    "token": "bot token here",
    "status": "Mention me for help! https://git.io/fhSTM",
    "website":"",
    "extensions": []
}

class Client(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=self.get_prefix,case_insensitive=False)
        self.config = None

    def load_config(self, path: str) -> Union[dict, None]:
        """
        Try to load the bot config file from the given path.\n
        If it doesn't exist, a default config will be created there.\n
        `path` - The path to load from.\n
        `returns` - The loaded config dict, or None.
        """
        try:
            return json.load(open(path, 'r'))
        except FileNotFoundError:
            print(
                f'Couldn\'t load "{path}"!\nIf this is the first run, that\'s okay! Configure the newly created config.json and restart.')
            json.dump(default_config, open(path, 'w'), indent=4)
            return None

    def initialize(self, config_path: str = os.path.join(script_dir(), 'config.json')):
        """
        Initialize the bot. Tries to load the config file from `config_path`, and if successful, runs the bot.\n
        `config_path` - Path to the config.json file.
        """
        self.config = self.load_config(config_path)
        if self.config != None:
            self.load_cogs()
            try:
                self.run(self.config['token'])
            except discord.LoginFailure as e:
                raise Exception(
                    'The bot token in "config.json" appears to be incorrect. Please double-check that you used the correct\nbot id from https://discordapp.com/developers/applications/.')
            except Exception as e:
                raise Exception(
                    'I can\'t connect to the Discord servers right now, sorry! :(\nCheck your internet connection, and then https://twitter.com/discordapp for Discord downtimes,\n and then try again later.')

    def load_cogs(self):
        for extension in self.config['extensions']:
            try:
                self.load_extension(extension)
            except Exception as e:
                print(f'Failed to load extension {extension}. ({str(e)})')
    
    async def get_prefix(self, message: discord.Message):
        # Temp
        char_prefixes = ('&', '!', '?',)
        prefixes=commands.when_mentioned_or(*char_prefixes)(self, message)
        return prefixes

    async def get_context(self, message, *, cls=commands.Context):
            r"""|coro|

            Returns the invocation context from the message.

            This is a more low-level counter-part for :meth:`.process_commands`
            to allow users more fine grained control over the processing.

            The returned context is not guaranteed to be a valid invocation
            context, :attr:`.Context.valid` must be checked to make sure it is.
            If the context is not valid then it is not a valid candidate to be
            invoked under :meth:`~.Bot.invoke`.

            Parameters
            -----------
            message: :class:`discord.Message`
                The message to get the invocation context from.
            cls
                The factory class that will be used to create the context.
                By default, this is :class:`.Context`. Should a custom
                class be provided, it must be similar enough to :class:`.Context`\'s
                interface.

            Returns
            --------
            :class:`.Context`
                The invocation context. The type of this can change via the
                ``cls`` parameter.
            """
            #ALL OF THIS CODE IS FROM THE ORIGINAL DISCORD.PY CODE.
            #I JUST ADDED THE "view.skip_ws()" BELOW TO SUIT IT TO ME.
            view = commands.view.StringView(message.content)
            ctx = cls(prefix=None, view=view, bot=self, message=message)

            if self._skip_check(message.author.id, self.user.id):
                return ctx

            prefix = await self.get_prefix(message)
            invoked_prefix = prefix

            if isinstance(prefix, str):
                if not view.skip_string(prefix):
                    return ctx
            else:
                try:
                    # if the context class' __init__ consumes something from the view this
                    # will be wrong.  That seems unreasonable though.
                    if message.content.startswith(tuple(prefix)):
                        invoked_prefix = discord.utils.find(view.skip_string, prefix)
                    else:
                        return ctx

                except TypeError:
                    if not isinstance(prefix, list):
                        raise TypeError("get_prefix must return either a string or a list of string, "
                                        "not {}".format(prefix.__class__.__name__))

                    # It's possible a bad command_prefix got us here.
                    for value in prefix:
                        if not isinstance(value, str):
                            raise TypeError("Iterable command_prefix or list returned from get_prefix must "
                                            "contain only strings, not {}".format(value.__class__.__name__))

                    # Getting here shouldn't happen
                    raise
            view.skip_ws() #ADDED THIS
            invoker = view.get_word()
            ctx.invoked_with = invoker
            ctx.prefix = invoked_prefix
            ctx.command = self.all_commands.get(invoker)
            return ctx

    async def on_ready(self):
        # Bot Info
        
        print(f'Logged in as: {self.user.name} ({self.user.id})')
        print(f'Active in: {len(self.guilds)} guilds, for {len(self.users)} users.')
        print('Opus Codecs Loaded Successfully!' if discord.opus.is_loaded() else 'WARN: Opus Codecs Not Loaded!')
        await self.is_owner(self.user) #Force the bot to find its owner
        self.description=f'{self.user.name} - a bot by {self.get_user(self.owner_id).name}'+('\n'+self.config["website"]) if self.config["website"] else ""
        print('Description set to:\n"'+self.description+'"')
        if not os.path.exists(os.path.join(script_dir(), 'resources', 'servers')):
            print('Creating resources directory...')
            os.makedirs(os.path.join(script_dir(), 'resources', 'servers'))
        print(f'Cogs ({len(self.extensions.keys())}): {",".join([m.__name__.replace("cogs.","") for m in self.extensions.values()])}')
        
    async def on_command_error(self,ctx:commands.Context,error:commands.CommandError):
        print(str(error))
        await ctx.send('ERROR: '+str(error))

    async def on_command(self,ctx:commands.Context):
        await ctx.trigger_typing()
        
        
client = Client()
try:
    client.initialize()
except Exception as e:
    print(str(e))
    sys.exit(-1)

