__module_name__ = "./addons/dcc_trusted.txt"
__module_version__ = "1.0"
__module_description__ = "Trusted list for DCC requests."

import hexchat

DEBUG = False

helptext = ("/TRUST   nick!user@host add a user to the trusted list.\n"
            "/UNTRUST nick!user@host remove a user from the trusted list.\n"
            "/TRUST   LIST        print a list of all trusted users.")

def trust_cb(word, word_eol, userdata):
    """Adds a nick to the trusted list."""
    try:
        if word[1].upper() == "LIST":
            print_list()
        else:
            trust(word[1])
        return hexchat.EAT_ALL
    except Exception as e:
        if DEBUG:
            hexchat.prnt("[DEBUG] trust_cb error: " + str(e))
        hexchat.emit_print("Notice", "DCC Trusted", helptext)
        return hexchat.EAT_ALL
        
def untrust_cb(word, word_eol, userdata):
    """Removes a nick from the trusted list."""
    try:
        if untrust(word[1]) == 0:
            hexchat.emit_print("Notice", "DCC Trusted", word[1] + " is no longer trusted.")
            return hexchat.EAT_ALL
        else:
            hexchat.emit_print("Notice", "DCC Trusted", word[1] + " was not found in the list.")
            return hexchat.EAT_ALL
    except Exception as e:
        if DEBUG:
            hexchat.prnt("[DEBUG] untrust_cb error: " + str(e))
        hexchat.emit_print("Notice", "DCC Trusted", helptext)
        return hexchat.EAT_ALL
        
def dcc_check_cb(word, word_eol, userdata):
    """Intercepts DCC requests and only allows trusted nicks through."""
    try:
        if not word[3] == ":DCC":  # DCC offer text
            return hexchat.EAT_NONE
        hexchat.emit_print("Notice", "DCC Trusted", "Offer received. Checking nick...")
        nick = word[0][1:]
        if is_trusted(nick):
            hexchat.prnt("\00303TRUSTED. Allowing offer.")
            return hexchat.EAT_NONE
        else:
            hexchat.prnt("\00304UNTRUSTED. Blocking offer.")
            nick = word[0][1:].split("!")[0] # Strip host name for reply
            hexchat.command("MSG " + nick + " XDCC CANCEL")
            return hexchat.EAT_ALL
    except Exception as e:
        if DEBUG:
            hexchat.prnt("[DEBUG] dcc_check_cb error: " + str(e))
        return hexchat.EAT_NONE
        
def trust(nick):
    """Adds a nick to the trusted list."""
    try:
        nick = nick.lower()
        if DEBUG:
            hexchat.prnt("[DEBUG] Trusting " + nick)
        if is_trusted(nick):
            hexchat.emit_print("Notice", "DCC Trusted", nick + " is already trusted.")
            return
        else:
            f = open("./addons/dcc_trusted.txt", 'a')
            f.write(nick + '\n')
            hexchat.emit_print("Notice", "DCC Trusted", nick + " is now trusted.")
            f.close()
            return
    except Exception as e:
        if DEBUG:
            hexchat.prnt("[DEBUG] trust error: " + str(e))
        hexchat.emit_print("Notice", "DCC Trusted", helptext)
        return
        
def untrust(nick):
    """Removes a nick from the trusted list."""
    try:
        nick = nick.lower()
        if DEBUG:
            hexchat.prnt("[DEBUG] Untrusting " + nick)
        f = open("./addons/dcc_trusted.txt", 'r')
        lines = f.readlines()
        f.close()
        if not (nick + '\n') in lines:
            return 1
        f = open("./addons/dcc_trusted.txt", 'w')
        for line in lines:
            if not line == (nick + '\n'):
                f.write(line)
        f.close()
        return 0
    except Exception as e:
        if DEBUG:
            hexchat.prnt("[DEBUG] untrust error: " + str(e))
        hexchat.emit_print("Notice", "DCC Trusted", helptext)
        return -1
        
def is_trusted(nick):
    """Checks trusted list for a given nick."""
    nick = nick.lower()
    try:
        f = open("./addons/dcc_trusted.txt", 'r')
        if (nick + '\n') in list(f):
            f.close()
            return True
        else:
            f.close()
            return False 
    except Exception as e:
        if DEBUG:
            hexchat.prnt("[DEBUG] is_trusted error: " + str(e))
        return True
        
def print_list():
    """Prints the current trusted list to the client."""
    try:
        f = open("./addons/dcc_trusted.txt", 'r')
        hexchat.emit_print("Notice", "DCC Trusted", "=========TRUSTED=========")
        for line in list(f):
            hexchat.prnt(line)
        hexchat.prnt("=========================")
        f.close()
        return
    except Exception as e:
        if DEBUG:
            hexchat.prnt("[DEBUG] print_list error: " + str(e))
        return
        
def unload_cb(userdata):
    """Prints a message when the plugin is unloaded."""
    hexchat.prnt("Unloading DCC trusted list")
    return hexchat.EAT_NONE
        
def server_all_cb(word, word_eol, userdata):
    hexstr = ""
    for x in word:
        hexstr = hexstr + x + '\t'
    hexchat.prnt(hexstr)
    return hexchat.EAT_NONE
    
hexchat.hook_command("TRUST", trust_cb, help=helptext)
hexchat.hook_command("UNTRUST", untrust_cb, help=helptext)
hexchat.hook_server("PRIVMSG", dcc_check_cb)
hexchat.hook_unload(unload_cb)
if DEBUG:
    hexchat.hook_server("RAW LINE", server_all_cb)

hexchat.prnt("DCC trusted plugin loaded")