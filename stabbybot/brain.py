# -*- coding: utf-8 -*-

#
# stabbybot brain
# https://github.com/vesche/stabbybot
#

import random

import log

# notes:
# it takes roughly 600 events for the longest move
# maybe should do this by seconds instead of by events...
# longest move is about 15 seconds

class GenTwo(object):
    def __init__(self, outgoing):
        self.outgoing = outgoing
        self.kill_info = {'uid': None, 'x': None, 'y': None, 'killer': None}
        self.kill_lock = False
        self.walk_lock = False
        self.walk_count = 0
        self.max_step_count = 600
    
    def main(self, game_state):
        # by priority
        self.go_for_kill(game_state)
        self.random_walk(game_state)
    
    def is_locked(self):
        if (self.walk_lock): # or ...
            return True
        return False
    
    def go_for_kill(self, game_state):
        if self.kill_info != game_state['kill_info']:
            self.kill_info = game_state['kill_info']
            #for i in game_state['perception']:
            # act on kill here
    
    def random_walk(self, game_state):
        if not self.is_locked():
            rand_x = random.randint(40, 400)
            rand_y = random.randint(40, 400)
            log.move(rand_x, rand_y)
            self.outgoing.move(str(rand_x), str(rand_y))
            self.walk_lock = True
            
        if self.max_step_count < self.walk_count:
            self.walk_lock = False
            self.walk_count = 0
        
        self.walk_count += 1


'''
class GenOne(object):
    """Generation 1 of the stabbybot. He's pretty dumb at the moment lol."""
    def __init__(self, outgoing):
        self.outgoing = outgoing
        self.kill_info = {'uid': None, 'x': None, 'y': None, 'killer': None}

    def testA(self, game_state):
        """Walks to the spot last player died."""
        if self.kill_info != game_state['kill_info']:
            self.kill_info = game_state['kill_info']
        
            if self.kill_info['killer']:
                print('New kill by %s! On the way to (%s, %s)!'
                    % (self.kill_info['killer'], self.kill_info['x'], self.kill_info['y']))
                self.outgoing.move(self.kill_info['x'], self.kill_info['y'])

    def testB(self, game_state):
        """Randomly kills a player roughly every 300 events."""
        if random.randint(0,300) == 27:
            uid = game_state['perception'][0]['uid']
            print('killing %s' % uid)
            self.outgoing.kill(uid)
    
    def testC(self, game_state):
        """I wonder... a nope"""
        if self.kill_info != game_state['kill_info']:
            self.kill_info = game_state['kill_info']
            print(self.kill_info)
        
            if self.kill_info['uid']:
                print(self.kill_info['uid'])
                #print('New kill by %s! On the way to (%s, %s)!'
                #    % (self.kill_info['killer'], self.kill_info['x'], self.kill_info['y']))
                #self.outgoing.move(self.kill_info['x'], self.kill_info['y'])
                self.outgoing.kill(self.kill_info['uid'])
'''