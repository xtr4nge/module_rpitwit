"""
    The (very simple) Raspberry PI Remote Controller for Tweeter
    Version 0.2.0
    Copyright (C) 2013  Mario Gomez (fuenteabierta.teubi.co)

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""


def load_config(source,fromString=False):
  """
    Loads a config file with configuration lines in the form:
       key=value
    And returns a dictionary with the format:
       {
         'key':'value'
       }
    The config file must exist or it will generate an assertion
    error.
    If you specify fromString=True it just parses the lines from
    the script provided as parameter on "source"
    
    Warning: This function can read empty files and will return
    empty dictionaires, also if you have two lines with the same 
    key it will overwrite the previous value with the last value
    found in the file.
  """
  contents = ''
  if not fromString:
    import os
    assert os.path.exists(source)
    f = open(source,'r')
    contents = f.read()
    f.close()
  else:
    contents = source
 
  config_vars = {}

  lines = contents.split('\n')
  for line in lines:
    config_pair = line.split('=')
    if(len(config_pair)==2):
      config_vars[config_pair[0].strip()] = config_pair[1].strip()
  return config_vars

def write_config(config_vars,destination):
  """
    Writes a dictionary as a config file
    returns True if write was successful
    False if not
  """
  assert type(config_vars)==dict
  result = True
  try:
    f = open(destination,'w')
    for key,value in config_vars.iteritems():
      f.write(key)
      f.write('=')
      f.write(value)
      f.write('\n')
    f.close()
  except:
    result = result and False
  return result

def build_secret():
  """
  build_secret()
  Decodes the application key and secret for RPiTwit,
  this function is here only to comply with tweeter 
  application keys usage guidelines, that require me
  to not distribuite the keys in plain text.
  
  It's very trivial to recover the keys, but I warn
  you: this keys had "read only" access to the Twitter
  API, you must generate your own keys if you want to
  add more features that require a higher access level.
  
  You can generate your own keys following the instructions
  included with the documentation.
  """
  import base64
  keys = '\
Q09OU1VNRVJfS0VZID0gZFE0ZHQ1SFdH\
Z09XNGJTdjNjTjV3IApDT05TVU1FUl9T\
RUNSRVQgPSA3aU5zM3pKM0pFdVpaNWhi\
NTNUbldNSXFERUlzZ3k2aGVqaU9OQmFF\
WQ=='
  return base64.b64decode(keys)

def find_userids(twitter_handler,message=None):
  """
  This function asks for twitter usernames
  and returns a string with the user ids
  separated by commas.
  """
  newUsers = ''
  while(newUsers==''):
    if message == None:
      print "\nPlease enter the username(s) who you want to allow"
      print "to execute commands (separated by commas). You can"
      print "change this later using the '--ask-follow' parameter"
    else:
      print message
    users = raw_input("> ")
    users = users.split(',')
    for user in users:
      try:
        print "\n Trying to get the user ID for "+user+"..."
        data = twitter_handler.users.show(screen_name=user.strip())
        if newUsers=='':
          newUsers = str(data['id'])
        else:
          newUsers = newUsers+','+str(data['id'])
        print "User @"+user+" added to the list."
      except:
        print "Error: Failed to add "+user+" to the list."
  return newUsers

def use_defaults_and_create(CONFIG_FILE):
  """
  This functions set the default options and generates
  a simple configuration file. The default application
  key and secret is not written on the generated config
  file, this forces this function to decode the keys on
  each call to the script.
  """
  config_vars = {
    'magicword' : '#rpitwit',
    'AppName' : 'RPiTwit'
  }

  keys = load_config(build_secret(),fromString=True)
  
  import twitter
  config_vars['oauth_token'],config_vars['oauth_secret'] = \
    twitter.oauth_dance(
      config_vars['AppName'],
      keys['CONSUMER_KEY'],
      keys['CONSUMER_SECRET']
    )

  twitter_handler = twitter.Twitter(
    auth=twitter.OAuth(
      config_vars['oauth_token'],
      config_vars['oauth_secret'],
      keys['CONSUMER_KEY'],
      keys['CONSUMER_SECRET']
    )
  )

  config_vars['follow'] = find_userids(twitter_handler)

  write_config(config_vars,CONFIG_FILE)
  
  config_vars = dict(config_vars.items() + keys.items())

  return config_vars

def load_and_verify_settings(CONFIG_FILE,args):
  """
  This function tries to load the config
  file and verify if the settings are set.
  Important: This function assumes that
  the config file exists.
  If not it uses the defaults.
  Returns the configuration options in a
  dictionary.
  Note: This function automaticaly writes
  the config.
  """
  # Config file exist, try to load it and
  # check for if the basic exists, if not
  # return them to defaults.
  config_vars = load_config(CONFIG_FILE)

  # magicword
  if not config_vars.get('magicword'):
    config_vars['magicword'] = '#rpitwit'

  # Check if we are using the hardcoded credentials or
  # custom user credentials.
  keys = {}
  usesDefaultKey = False
  # AppName, CONSUMER_KEY and CONSUMER_SECRET go together
  # if any of them is missing we return to default credentials.
  if not config_vars.get('AppName') or \
      not config_vars.get('CONSUMER_KEY') or \
      not config_vars.get('CONSUMER_SECRET'):
    useDefaultKey = True
    keys = load_config(build_secret(),fromString=True)
    config_vars['AppName'] = 'RPiTwit'
  else:
    keys['CONSUMER_KEY'] = config_vars['CONSUMER_KEY']
    keys['CONSUMER_SECRET'] = config_vars['CONSUMER_SECRET']

  # User requested reload oauth tokens
  if '--reload-tokens' in args:
    if usesDefaultKey:
      print "\nUsing default application credentials."
    else:
      print "\nUsing custom application credentials."
    
    import twitter
    config_vars['oauth_token'], config_vars['oauth_secret'] = \
      twitter.oauth_dance(
        config_vars['AppName'],
        keys['CONSUMER_KEY'],
        keys['CONSUMER_SECRET']
      )

  # User requested change of follow list
  if not config_vars.get('follow') or \
      '--ask-follow' in args:
    import twitter
    twitter_handler = twitter.Twitter(
      auth=twitter.OAuth(
        config_vars['oauth_token'],
        config_vars['oauth_secret'],
        keys['CONSUMER_KEY'],
        keys['CONSUMER_SECRET']
      )
    )

    config_vars['follow'] = find_userids(twitter_handler)

  # We checked everything, at this point we can
  # save the settings.
  write_config(config_vars,CONFIG_FILE)

  # We keep the hardcoded keys in a separate dictionary
  # because writing them to the config file in plain
  # text would be against the Twitter key usage guidelines.
  config_vars = dict(config_vars.items() + keys.items())

  return config_vars

def print_about():
  print "\n\
RPiTwit v0.2.0\n\
The (very simple) Raspberry PI Remote Controller for Tweeter\n\
http://pypi.python.org/pypi/rpitwit\n\
Copyright (C) 2013  Mario Gomez (fuenteabierta.teubi.co) \n\
\n\
This program is free software: you can redistribute it and/or modify \n\
it under the terms of the GNU General Public License as published by \n\
the Free Software Foundation, either version 3 of the License, or \n\
(at your option) any later version. \n\
\n\
This program is distributed in the hope that it will be useful, \n\
but WITHOUT ANY WARRANTY; without even the implied warranty of \n\
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the \n\
GNU General Public License for more details. \n\
\n\
You should have received a copy of the GNU General Public License \n\
along with this program.  If not, see <http://www.gnu.org/licenses/>.\n"

def print_help():
  print "\n\
Welcome to RPiTwit, a really simple tool to run commands on your\n\
Linux box using Twitter. \n\
\n\
How to use?\n\
Just write \"rpitwit\" on the command line and follow the instructions.\n\
\n\
Put your python scripts on ~/rpitwit_commands, just remember to\n\
change the permissions to +755 if you are using shell scripts.\n\
You can also use binary executables if you need to run more\n\
complicated things.\n\
\n\
To run commands from twitter just update your status\n\
in the following format:\n\
\n\
    #rpitwit <command> [arguments]\n\
\n\
RPiTwit is going to try to find the command with the specified name on\n\
your command directory and it's going to execute it on your Linux box.\n\
\n\
There is a couple of useful parameters that you can use when\n\
calling rpitwit from the command line.\n\
\n\
    -l , --load-defaults :	Load default configuration options\n\
         --ask-follow : 	This asks you for the usernames allowed to run\n\
				commands.\n\
         --reload-tokens : 	This reloads the oAuth tokens, try to use this\n\
				if rpitwit ends with error messages. Or if you are using\n\
				your custom Twitter application keys.\n\
    -a , --about : 		Copyright info.\n\
    -h , --help : 		This help.\n\
    -f , --config-file :	rpitwit_config file path. ( -f <file_path> )\n\
    -d , --commands-dir :	rpitwit_commands folder path. ( -d <dir_path> )\n\
\n\
For more info check the documentation directory on the PyPI\n\
distribution package.\n\
\n\
Have fun!\n"


