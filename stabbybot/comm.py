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


class Incoming():
    """Handle incoming game data."""

    def __init__(self):
        self.game_data = {
            'perception': [],
            'kill_info': {}
        }

    def process(self, data):
        """Process raw game data into game_data dict."""
        event_code = data[:2]
        # tmp
        try:
            event_type = EVENTS[event_code]
        except: return
        data = data[2:]

        if event_type == 'perception':
            self.game_data['perception'] = []

            data = data.split('|')
            data.pop()
            
            for i in data:
                uid, x, y, status, direction = i.split(',')
                self.game_data['perception'].append(
                    {'uid': uid, 'x': x, 'y': y, 'status': status, 'direction': direction}
                )

        elif event_type == 'kill_info':
            uid, x, y, killer = data.split(',')
            self.game_data['kill_info'] = {'uid': uid, 'x': x, 'y': y, 'killer': killer}


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
        self.ws.send('%s%s%s' % ('07', x, y))

    def setname(self, username):
        self.ws.send('%s%s' % ('03', username))
        