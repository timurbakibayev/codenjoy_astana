#!/usr/bin/env python
# -*- coding: utf-8 -*-

import websocket
import math
try:
    import thread
except ImportError:
    import _thread as thread
import time

def on_message(ws, message):
    print(message)

    ws.send("DOWN")


def on_error(ws, error):
    print(error)

def on_close(ws):
    print("### closed ###")

def on_open(ws):
    pass


if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("ws://codenjoy.astanajug.net:8080/contest/ws?user=AlmaU@gmail.com&code=11488134331889285721",
                              on_message = on_message,
                              on_error = on_error,
                              on_close = on_close)

    ws.on_open = on_open
    ws.run_forever()

