# -*- coding: utf-8 -*-

#
# stabbybot comm
# https://github.com/vesche/stabbybot
#

import log


EVENTS = {
    '01': '01',
    '02': '02',
    '03': 'login',
    '04': '04',
    '05': 'perception',
    '06': '06',
    '07': 'move',
    '08': '08',
    '09': '09',
    '10': 'kill',
    '13': 'killed_by',
    '14': 'kill_info',
    '15': 'stats',
    '18': 'target'
}


def incoming(gs, raw_data):
    """Handle incoming game data."""

    event_code = raw_data[:2]
    # tmp until I have all event codes mapped out
    try:
        event_type = EVENTS[event_code]
    except: return
    data = raw_data[2:]

    if event_type == 'perception':
        gs.perception(data)
    elif event_type == 'kill_info':
        gs.kill_info(data)
    elif event_type == 'killed_by':
        gs.killed_by(data)
    elif event_type == 'stats':
        gs.stats(data)
    elif event_type == 'target':
        gs.target(data)
    # uncomment this to see unknown events
    # else:
    #     log.unknown(event_type, data)


class Outgoing(object):
    """Handle outgoing game data."""

    def __init__(self, ws):
        self.ws = ws
    
    def begin(self, game_ver):
        self.ws.send('%s' % game_ver)
        self.ws.pong('')

    def kill(self, uid):
        self.ws.send('%s%s' % ('10', uid))

    def move(self, x, y):
        x = x.split('.')[0]
        y = y.split('.')[0]
        self.ws.send('%s%s,%s' % ('07', x, y))

    def setname(self, username):
        self.ws.send('%s%s' % ('03', username))
