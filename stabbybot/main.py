#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# stabbybot main
# https://github.com/vesche/stabbybot
#

import websocket

import comm
import brain


SERVER = '45.77.80.61:443'
GAME_URL = 'http://stabby.io'
GAME_VER = '000.0.4.3'
USERNAME = 'sb'


def main():
    ws = websocket.WebSocket()
    ws.settimeout(1)
    ws.connect('ws://%s' % SERVER, origin=GAME_URL)

    # instantiate classes
    incoming = comm.Incoming()
    outgoing = comm.Outgoing(ws)
    bot = brain.GenOne(outgoing)

    # init comms
    outgoing.begin(GAME_VER)
    outgoing.setname(USERNAME)

    while True:
        data = ws.recv()
        incoming.process(data)

        # tmp, need some sort of logging
        if incoming.game_state['dead']:
            print('[-] You have been killed.')
            break

        bot.testC(incoming.game_state)

    #try:
    #    pass
    #except Exception as e:
    #    print(e)
    #    ws.close()
    #    return
    #except KeyboardInterrupt:
    #    ws.close()
    #    return

    ws.close()


if __name__ == '__main__':
    main()