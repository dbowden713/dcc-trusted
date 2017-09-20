# dcc-trusted

This is a python-based plugin for the Hexchat IRC client that adds simple commands to whitelist other users (usually bots) for DCC file transfer offers. With this whitelist, users can set Hexchat to auto accept DCC offers without fear of being sent files by random users.

### Installation

For this plugin to work, make sure Hexchat is installed with the Python plugin (both 2 and 3 supported).  
With Hexchat installed, dcc-trusted can be installed by placing it in the addons folder. By default, this is located:

On Windows: `%APPDATA%\HexChat\addons`  
On Unix: `~/.config/hexchat/addons`

The plugin will now load by default when Hexchat is started. Look for `DCC trusted plugin loaded` in Hexchat's main window!

### Commands

There are three simple commands:

1. /TRUST username - allows file requests from a user. Format is `nickname!username@host.name` (use /whois to check)
2. /UNTRUST username - removes a user from the trusted list. Use this just like /TRUST
3. /TRUST LIST - Lists all users currently trusted

### Credits
[dbowden713](https://github.com/dbowden713)
