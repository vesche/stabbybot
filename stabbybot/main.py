#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# stabbybot main
# https://github.com/vesche/stabbybot
#

import argparse
import websocket

import state
import comm
import brain
import log


# SERVER = '45.77.80.61'
GAME_URL = 'http://stabby.io'
GAME_VER = '000.0.4.3'


def get_parser():
    parser = argparse.ArgumentParser(description='stabbybot')
    parser.add_argument('-s', '--server',
                        help='server ip', required=True, type=str)
    parser.add_argument('-u', '--username',
                        help='username', default='sb', type=str)
    return parser


def main():
    parser = get_parser()
    args = vars(parser.parse_args())
    server = args['server']
    username = args['username']

    ws = websocket.WebSocket()
    ws.settimeout(1)
    ws.connect('ws://%s:443' % server, origin=GAME_URL)

    # instantiate classes
    gs = state.GameState()
    outgoing = comm.Outgoing(ws)
    bot = brain.GenTwo(outgoing)

    # init comms
    outgoing.begin(GAME_VER)
    outgoing.setname(username)

    try:
        while True:
            raw_data = ws.recv()
            comm.incoming(gs, raw_data)

            if gs.game_state['dead']:
                break
            
            bot.main(gs.game_state)
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(e)

    ws.close()


if __name__ == '__main__':
    main()
