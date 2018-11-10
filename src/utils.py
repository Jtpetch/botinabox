import os
import json
from datetime import datetime
from difflib import SequenceMatcher 
from bGlobals import *
from serverclass import *
#GLOBALS===========================#
max_logs=150
#==================================#
def update_bot():
    #NOT WORKING YET
    def update_script(git_repo:str,clone_to:str,source_file_location:str,base_dir:str):
        def on_rm_error( func, path, exc_info):
            # path contains the path of the file that couldn't be removed
            # let's just assume that it's read-only and unlink it.
            os.chmod( path, stat.S_IWRITE )
            os.unlink( path )

        def copytree(src, dst, symlinks=False, ignore=None):
            for item in os.listdir(src):
                s = os.path.join(src, item)
                d = os.path.join(dst, item)
                if os.path.isdir(s):
                    shutil.copytree(s, d, symlinks, ignore)  
                else:
                    shutil.copy2(s, d)

        def rmtree(src):
            if not os.path.exists(src): return
            while (True):
                try:
                    if os.path.isdir(src):
                        shutil.rmtree(src,onerror=on_rm_error)
                    else: 
                        os.remove(src)
                    break
                except Exception as e:
                    print(e)
                    time.sleep(0.1)
        
        #Clone Repo
        if os.path.isdir(clone_to):rmtree(clone_to)
        Repo.clone_from(git_repo,clone_to).close()
        #Get files to delete
        for item in os.listdir(os.path.join(clone_to,source_file_location)): rmtree(item)
        
        #Copy new source files to current dir
        copytree(os.path.join(clone_to,source_file_location),base_dir)
        time.sleep(0.01)
        rmtree(clone_to)
    git_repo='https://github.com/wolfinabox/botinabox.git'
    clone_to=os.path.join(script_dir,'botinabox_update')
    source_file_location='src'
    update_script(git_repo,clone_to,source_file_location,base_dir=script_dir)
    os.execv(os.path.join(script_dir,'botinabox.py'), sys.argv)

def loadID(location:str=os.path.join(script_dir, 'token.txt')):
    """
    Loads the bot's client ID from the "token.txt" file
    :returns: The loaded ID
    :throws: FileNotFoundError, if token.txt file not found
    """
    file = open(location)
    id=file.readline().strip()
    return id

def pLog(message:str,logFilePath:str=os.path.join(script_dir, 'log.txt')):
    """
    Prints and logs the given message to file
    :param message: The message to print/log
    :param logFilePath: The path to the logging file
    """
    print(message)
    log(message,logFilePath)

def log(message:str,logFilePath:str=os.path.join(script_dir, 'log.txt')):
    """
    Logs the given message to file
    :param message: The message to log
    :param logFilePath: The path to the logging file
    """
    message=message.replace('\n',' ').replace('\r',' ')
    try:
        num_lines = sum(1 for line in open(logFilePath))
        if num_lines>=max_logs:
            lines=open(logFilePath, 'r').readlines()
            del lines[0]
            lines.append(datetime.now().strftime('[%m/%d/%Y-%H:%M:%S]: ')+message+'\n')
            with open(logFilePath,'w') as file:
                file.writelines(lines)
        else:
            with open(logFilePath,'a') as file:
                file.write(datetime.now().strftime('[%m/%d/%Y-%H:%M:%S]: ')+message+'\n')
    except IOError:
        with open(logFilePath,'w') as file:
            file.write(datetime.now().strftime('[%m/%d/%Y-%H:%M:%S]: ')+message+'\n')

def truncate(data:str,length:int,append:str=''):
    """
    Truncates a string to the given length
    :param data: The string to truncate
    :param length: The length to truncate to
    :param append: Text to append to the end of truncated string
    """
    return (data[:length]+append) if len(data)>length else data

def isInt(s:str):
    try: 
        int(s)
        return True
    except ValueError:
        return False

def timeToSec(s:str):
    #Format: 00:00:00 (hour:minute:second)
    seconds=0
    strings=s.split(':')
    if len(strings)>3: raise ValueError()
    multiplier=1
    for string in strings[::-1]:
        if not isInt(string): raise ValueError()
        seconds+=(int(string)*multiplier)
        multiplier*=60
    return seconds

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

def any_in(a, b):
  return not set(a).isdisjoint(b)

def loadServer(id,folderPath=os.path.join(script_dir,'resources','servers')):
    path=os.path.join(folderPath,id+'.json')
    #If the file does not exist
    if not os.path.isfile(path): return None
    temp={}
    with open(path,'r') as f:
        temp=json.load(f)
    sClass=serverClass(temp['id'])
    sClass.commandPrefix=(temp['commandPrefix'] if 'commandPrefix' in temp else defaultCommandPrefix )
    sClass.customCommands=(temp['customCommands'] if 'customCommands' in temp else [])
    return sClass

def saveServer(serverClass,folderPath=os.path.join(script_dir,'resources','servers')):
    path=os.path.join(folderPath,serverClass.id+'.json')
    data={'id':serverClass.id,'commandPrefix':serverClass.commandPrefix,'customCommands':serverClass.customCommands}
    with open(path,'w') as f:
        json.dump(data,f,indent=4)
    

class CommUsage(Exception):
    def __init__(self,arg):
        self.sterror = arg
        self.args = {arg}

class NoPerm(Exception):
    def __init__(self,arg):
        self.sterror = arg
        self.args = {arg}