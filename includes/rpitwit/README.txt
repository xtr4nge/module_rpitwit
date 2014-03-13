======================================================================
RPITwit - The (very simple) Raspberry PI Remote Controller for Tweeter
======================================================================

RPITwit is a really simple script to execute remote shell commands on
your RaspberryPI using your twitter account.

Just write a status on your twitter account using the following format::

    #RPITwit script command

The scripts are saved on **"~/rpitwit_commands/scripts"**. you can use
shell or python scripts. In the case of python scripts do not include
the **".py"** extension when calling the command on twitter.

Installing RPITwit
==================

Just extract the package and run::

    sudo python setup.py install

Running on Raspberry PI
=======================

(Never run the rpitwit-daemon as root)

Execute the following command::

   rpitwit

And follow the instructions.

To stop press **Ctrl+C**

Changing the list of authorized users:
======================================

Just start rpitwit with the '--ask-follow' parameter::

   rpitwit --ask-follow

Configuration
=============
The firs time that you run rpitwit is going to ask you for
authorization on twitter, follow the instructions.

The script is going to ask you for the twitter usernames
who are going to be able to execute scripts. Don't allow
access to unknown people.

The configuration options are stored in **~/.rpitwit_config**

You can modify the following options:

   **magicword**: keyword used to run commands, this must be
     the first word on your tweet.

   **follow**: list of twitter user IDs that who are going
     to be able to execute commands.

   **AppName**: Name of the application on Twitter. Do not
     modify unless you are using your own keys.

   **oauth_token**: generated automatically. Do not modify.

   **oauth_secret**: generated automatically. Do not modify.

If you are using your own application keys you must add
this tree lines to your **~./rpitwit_config** file::

   AppName=<your twitter application name>
   CONSUMER_KEY=<your twitter application key>
   CONSUMER_SECRET=<your twitter application secret>

Now yo need to start rpiwit with the "--reload-tokens" argument::

   rpitwit --reload-tokens

For more info about generating your application keys look
in the documentation directory.

Warning
=======

This very simple tool that justs execute shell and python
scripts contained within the script directory.

It doesn't limit what the commands can do to your system.

Be really carefull, don't put dangerous commands or scripts
from untrusted sources inside the command directory.

Changelog from 0.1.0 to 0.2.0
=============================

* The script now captures SIGINT and SIGTERM and closes
  without giving errors   when you press CTRL-C or using the kill command.
* Added the "--about" argument to show copyright info.
* Added the "--help" with a really small help text.
* Added the "--load-defaults" argument to load the default config.
  If you screw up the configuration try with this argument.
* Added the "--reload-tokens" argument to update the oAuth tokens
  in case of using custom application keys.
* Added the "--ask-follow' argument to change the list
  of users that rpitwit follows after the first run.
* A lot of code cleanup. Comments added. Now it's more
  easy to read and understand.

Credits and more Info
=====================

This software uses functions from the Python Twitter Tools
by Mike Verdone (mike.verdone.ca)

RPiTwit maintainer:
  Mario Gomez <rpitwit@teubi.co>
  (http://fuenteabierta.teubi.co/)

A more detailed explanation of usage and examples:

    http://fuenteabierta.teubi.co/2013/01/controlling-raspberry-pi-via-twitter.html
