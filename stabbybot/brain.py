# -*- coding: utf-8 -*-

"""
stabbybot brain
https://github.com/vesche/stabbybot
"""

import collections
import random

from scipy import spatial

import log


class GenTwo(object):
    """Generation 2 of stabbybot."""

    def __init__(self, outgoing):
        self.outgoing = outgoing
        self.kill_info = {'uid': None, 'x': None, 'y': None, 'killer': None}
        self.kill_lock = False
        self.walk_lock = False
        self.walk_count = 0
        self.max_step_count = 600
        self.kill_delta = 20

    def main(self, game_state):
        # by priority
        self.go_for_kill(game_state)
        self.random_walk(game_state)

    def is_locked(self):
        if (self.walk_lock): # put other locks here
            return True
        return False

    def go_for_kill(self, game_state):
        if self.kill_info != game_state['kill_info']:
            self.kill_info = game_state['kill_info']
            self.kill_lock = True

            kill_x = float(game_state['kill_info']['x'])
            kill_y = float(game_state['kill_info']['y'])

            player_coords = collections.OrderedDict()
            for i in game_state['perception']:
                player_x = float(i['x'])
                player_y = float(i['y'])
                player_uid = i['uid']
                player_coords[player_uid] = (player_x, player_y)

            # get player closest to kill coordinates
            tree = spatial.KDTree(list(player_coords.values()))
            distance, index = tree.query([(kill_x, kill_y)])

            # go for kill if a player was close enough to the kill
            if distance < 10:
                kill_uid = list(player_coords.keys())[int(index)]
                self.outgoing.kill(kill_uid)
                log.assassinating(kill_uid)

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


class GenOne(object):
    """Generation 1 of stabbybot."""

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

