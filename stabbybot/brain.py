# -*- coding: utf-8 -*-

#
# stabbybot brain
# https://github.com/vesche/stabbybot
#

import random

class GenOne(object):
    """Walks to the spot last player died."""
    def __init__(self, outgoing):
        self.outgoing = outgoing
        self.kill_info = {'uid': None, 'x': None, 'y': None, 'killer': None}

    def testA(self, game_state):
        if self.kill_info != game_state['kill_info']:
            self.kill_info = game_state['kill_info']
        
            if self.kill_info['killer']:
                print('New kill by %s! On the way to (%s, %s)!'
                    % (self.kill_info['killer'], self.kill_info['x'], self.kill_info['y']))
                self.outgoing.move(self.kill_info['x'], self.kill_info['y'])

    def testB(self, game_state):
        if random.randint(0,300) == 27:
            uid = game_state['perception'][0]['uid']
            print('killing %s' % uid)
            self.outgoing.kill(uid)