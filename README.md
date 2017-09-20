# dcc-trusted

This is a python-based plugin for the Hexchat IRC client that adds simple commands to whitelist other users (usually bots) for DCC file transfer offers. With this whitelist, users can set Hexchat auto accept DCC offers without fear of being sent files by random users.

### Commands

There are three simple commands:

1. /TRUST username - allows file requests from the username. Username is formatted as nickname!username@host.name
Example:
> /trust coolnick!botname@i.am.a.bot
2. /UNTRUST username - removes a user from the trusted list. Use this just like /TRUST
3. /TRUST LIST - Lists all users currently trusted
