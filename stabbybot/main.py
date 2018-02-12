#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# stabbybot
# https://github.com/vesche/stabbybot
#

import time
import websocket


SERVER = '45.77.80.61:443'
GAME_URL = 'http://stabby.io'
GAME_VER = '000.0.4.3'
USERNAME = 'sb'

EXTRA_HEADERS = [
    ('User-Agent', 'Mozilla/5.0 (X11; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'),
    ('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'),
    ('Accept-Language', 'en-US,en;q=0.5'),
    ('Accept-Encoding', 'gzip, deflate'),
    ('Sec-WebSocket-Extensions', 'permessage-deflate'),
    ('Pragma', 'no-cache'),
    ('Cache-Control', 'no-cache')
]

EVENTS = {
    'Login':      '03',
    'Perception': '05',
    'Movement':   '07',
    'Unknown':    '08',
    'Kill':       '10',
    'KilledBy':   '13',
    'KillInfo':   '14',
    'Stats':      '15',
    'Target':     '18'
}

#kill_mode = False
#kmx = 0
#kmy = 0

def incoming(data, ws):
    #global kill_mode, kmx, kmy
    event_code = data[:2]
    data = data[2:]

    if event_code == EVENTS['Perception']:
        # print('[+] Perception (03)')
        for i in data.split('|'):
            try:
                cid, x, y, status, direction = i.split(',')
                #print('\tcid: %s x: %s y: %s status: %s direction: %s' %
                #    (cid, x, y, status, direction))
                
                # tmp, kill around
                #if kill_mode:
                #    if (kmx+30 > int(float(x)) > kmx-30) and (kmy+30 > int(float(y)) > kmy-30):
                #        ws.send('10%s' % cid)
                #        kill_mode = False
            except ValueError:
                pass
            except Exception as e:
                print(e)

    elif event_code == EVENTS['KillInfo']:
        print('[+] KillInfo (14)')
        cid, x, y, killer = data.split(',')
        print('\tkilled: %s x: %s y: %s killer: %s' %
            (cid, x, y, killer))
        
        # tmp, move to killer
        #kill_mode = True
        _#, x, y, _ = data.split(',')
        #x = x.split('.')[0]
        #y = y.split('.')[0]
        #ws.send('07{},{}'.format(x, y))
        ws.send('070,0')
        #kmx, kmy = int(float(x)), int(float(y))

'''
    elif event_code == EVENTS['Unknown']:
        print('[+] Unknown (08)')
        print('\t' + data)

    elif event_code == EVENTS['KilledBy']:
        print('[+] KilledBy (13)')
        print('\t' + data)
'''
'''
    elif event_code == EVENTS['Stats']:
        print('[+] Stats (15)')
        print('\t' + data)

    elif event_code == EVENTS['Target']:
        print('[+] Target (18)')
        #foo, target, distance = data.split(',')
        #print('\tfoo: %s target: %s distance %s' %
        #    (foo, target, distance))
        print('\t' + data) # no target ?

    else:
        # dump unknowns to file
        with open('newcodes.txt', 'a') as f:
            f.write(event_code + data + '\n')
'''

def main():
    ws = websocket.WebSocket()

    ws.settimeout(1)
    ws.connect('ws://%s' % SERVER, origin=GAME_URL)

    ws.send(GAME_VER)
    ws.pong('')
    ws.send('03%s' % USERNAME)

    #time.sleep(2)
    #print('moving to TOP LEFT')
    #ws.send('07%s' % '0,0')

    #time.sleep(20)
    #print('moving to TOP RIGHT')
    #ws.send('07%s' % '350,0')

    #time.sleep(20)
    #print('killing random...')
    #ws.send('10+58260')

    try:
        while True:
            data = ws.recv()
            incoming(data, ws)
    except Exception as e:
        print(e)
        ws.close()
        return
    except KeyboardInterrupt:
        ws.close()
        return

    # connect and send: 000.0.4. 3
    # then username: 03username

    # 0x30 0x30 - ? server version
    # 30 30 30 2e 30 2e 34 2e 33
    # 0x30 0x33 - username

    # send handshake? start listen?
    ws.close()


if __name__ == '__main__':
    main()