# -*- coding: utf-8 -*-

#
# stabbybot comm
# https://github.com/vesche/stabbybot
#

EVENTS = {
    '03': 'login',
    '05': 'perception',
    '07': 'move',
    '08': '?',
    '10': 'kill',
    '13': 'killed_by',
    '14': 'kill_info',
    '15': 'stats',
    '18': 'target'
}


def incoming(gs, raw_data):
    event_code = raw_data[:2]
    # tmp
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

'''
class Incoming():
    """Handle incoming game data."""

    def __init__(self):
        self.game_state = {
            'perception': [],
            'kill_info': {'uid': None, 'x': None, 'y': None, 'killer': None},
            'dead': False
        }

    def process(self, data):
        """Process raw game data into game_state dict."""
        event_code = data[:2]
        # tmp
        try:
            event_type = EVENTS[event_code]
        except: return
        data = data[2:]

        if event_type == 'perception':
            self.game_state['perception'] = []

            data = data.split('|')
            data.pop()
            for i in data:
                uid, x, y, status, direction = i.split(',')
                self.game_state['perception'].append(
                    {'uid': uid, 'x': x, 'y': y, 'status': status, 'direction': direction}
                )

        elif event_type == 'kill_info':
            uid, x, y, killer = data.split(',')
            self.game_state['kill_info'] = {'uid': uid, 'x': x, 'y': y, 'killer': killer}

        elif event_type == 'killed_by':
            self.game_state['dead'] = True
'''

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
        