# -*- coding: utf-8 -*-

#
# stabbybot log
# https://github.com/vesche/stabbybot
#

# log types

def log_info(message):
    print("[+] %s" % message)

def log_warn(message):
    print("[!] %s" % message)

def log_bad(message):
    print("[-] %s" % message)

# log events

def unknown(event_type, data):
    log_warn("UNKN: %s - %s" % (event_type, data))

def move(x, y):
    log_info("MOVE: (%s, %s)" % (x, y))

def kill(killer, x, y):
    log_info("KILL: %s (%s, %s)" % (killer, x, y))

def assassinating(uid):
    log_info("ASSA: %s" % uid)

def dead():
    log_bad("You have been killed.")

def stats(li):
    log_info("STAT: {}".format(li))

def tod(data):
    log_info("TOD: {}".format(data))