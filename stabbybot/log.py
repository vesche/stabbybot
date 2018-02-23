# -*- coding: utf-8 -*-

#
# stabbybot log
# https://github.com/vesche/stabbybot
#

def log_info(message):
    print("[+] %s" % message)

def log_warn(message):
    print("[!] %s" % message)

def log_bad(message):
    print("[-] %s" % message)

###

def unknown(event_type, data):
    log_warn("UNKN: %s - %s" % (event_type, data))

def move(x, y):
    log_info("MOVE: (%s, %s)" % (x, y))

def kill(killer, x, y):
    log_info("KILL: %s (%s, %s)" % (killer, x, y))

def dead():
    log_bad("You have been killed.")
