#!/usr/bin/env python
# -*- coding: utf-8 -*-

import websocket
import math
import json
import numpy as np
import msvcrt

try:
    import thread
except ImportError:
    import _thread as thread
import time

global_reply = ""


def simulate(a,figure,x):
    result = ""
    b = []
    for i in range(len(a)):
        b += [[]]
        for j in range(len(a[i])):
            b[i] += [a[i][j]]

    intersection = False
    y = -1
    while not intersection:
        y += 1
        for i in range(4):
            for j in range(4):
                if figure[i][j]:
                    if i + y > 15 or x + j > 15 or x + j < 0 or (b[i+y][j+x] != " " and b[i+y][j+x] == b[i+y][j+x].upper()):
                        intersection = True
    y -= 1
    for i in range(4):
        for j in range(4):
            if figure[i][j]:
                if i+y < 0 or i+y > 15 or j+x < 0 or j+x > 15:
                    return 100, b
                b[i + y][j + x] = "x"

    result = 0
    for i in range(4):
        for j in range(4):
            if figure[i][j]:
                d = 0
                for k in range(i + y, 16):
                    if b[k][j + x] == " " and (i+d > len(figure)-1 or not(figure[i+d][j])):
                        result += 2
                    d += 1
    for i in range(16):
        full = True
        for j in range(16):
            if b[i][j] == " ":
                full = False
        if full:
            result -= 10
    result += 15-y
    return result, b

def preprocess(field, x, y, current):

    global global_reply

    keypress = True
    while keypress:
        keypress = False
        key = msvcrt.kbhit()
        if key:
            ret = ord(msvcrt.getch())
            if ret == 75:
                global_reply = "LEFT"
            if ret == 77:
                global_reply = "RIGHT"
            if ret == 72:
                global_reply = "ACT"
            if ret == 32:
                global_reply = "DOWN"
            keypress = True
            print(ret)

    a = []
    for i in range(16):
        new_line = []
        for j in range(16):
            if y == 15 - i and x == j:
                new_line.append(field[i * 16 + j].lower())
            else:
                new_line.append(field[i * 16 + j])
        a.append(new_line)
    changes = True
    x1 = x
    y1 = 15-y
    x2 = x
    y2 = 15-y
    while changes:
        changes = False
        for i in range(16):
            for j in range(16):
                if a[i][j] != " ":
                    if i > 0 and a[i - 1][j].upper() == a[i][j] and a[i - 1][j] != a[i][j]:
                        a[i][j] = a[i - 1][j].lower()
                        if x1 > j:
                            x1 = j
                        if y1 > i:
                            y1 = i
                        if x2 < j:
                            x2 = j
                        if y2 < i:
                            y2 = i
                        changes = True
                    if i < 15 and a[i + 1][j].upper() == a[i][j] and a[i + 1][j] != a[i][j]:
                        a[i][j] = a[i + 1][j].lower()
                        if x1 > j:
                            x1 = j
                        if y1 > i:
                            y1 = i
                        if x2 < j:
                            x2 = j
                        if y2 < i:
                            y2 = i
                        changes = True
                    if j > 0 and a[i][j - 1].upper() == a[i][j] and a[i][j - 1] != a[i][j]:
                        a[i][j] = a[i][j - 1].lower()
                        if x1 > j:
                            x1 = j
                        if y1 > i:
                            y1 = i
                        if x2 < j:
                            x2 = j
                        if y2 < i:
                            y2 = i
                        changes = True
                    if j < 15 and a[i][j + 1].upper() == a[i][j] and a[i][j + 1] != a[i][j]:
                        a[i][j] = a[i][j + 1].lower()
                        if x1 > j:
                            x1 = j
                        if y1 > i:
                            y1 = i
                        if x2 < j:
                            x2 = j
                        if y2 < i:
                            y2 = i
                        changes = True
    f = []
    full = 0
    for i in range(y1,y2 + 1):
        new_line = []
        for j in range(x1,x2 + 1):
            if a[i][j] != " " and a[i][j] == a[i][j].lower():
                new_line.append(1)
                full += 1
            else:
                new_line.append(0)
        while len(new_line) < 4:
            new_line.append(0)
        f.append(new_line)
    while len(f) < 4:
        f.append([0,0,0,0])

    if full < 4:
        return

    r = [np.array(f)]
    print(r[0])
    max_rotations = {"i": 1, "j": 3, "l": 3, "o": 0, "s": 1, "t":3, "z": 2}
    for i in range(max_rotations[current.lower()]):
        try:
            r.append(np.rot90(np.rot90(np.rot90(r[i]))))
            print(r[i + 1])
        except:
            pass

    results = []

    rotated = 0
    for figure in r:
        for j in range(-3,16):
            result, sim = simulate(a,figure,j)
            results.append({"error": result, "sim": sim, "rotated": rotated})
        rotated += 1


    if len(results) == 0:
        print("!!!!!!!!!!!!!!!!! PROBLEM, EMPTY RESULTS")
        global_reply = ""
        return

    best = results[0]["error"]
    sim = results[0]["sim"]
    rotated = results[0]["rotated"]
    for result in results:
        if best >= result["error"]:# and not ((rotated == 0) and result["rotated"] > 0):
            best = result["error"]
            sim = result["sim"]
            rotated = result["rotated"]

    if rotated > 0:
        global_reply = "ACT"
    else:
        found_x = False
        found_i = False
        x_pos = 0
        i_pos = 0
        for i in range(16):
            for j in range(16):
                if sim[i][j] == "x":
                    if not found_x:
                        found_x = True
                        x_pos = j
                elif sim[i][j] != " " and sim[i][j] == sim[i][j].lower():
                    if not found_i:
                        found_i = True
                        i_pos = j
        print(x_pos,i_pos)
        if x_pos == i_pos:
            global_reply = "DOWN"
        elif x_pos < i_pos:
            global_reply = "LEFT"
        else:
            global_reply = "RIGHT"

    print(np.array(sim))

    # print(np.array(a))



def on_message(ws, message):
    global global_reply
    message = message[6:]
    # print(message)
    game = json.loads(message)
    x, y = json.loads(game["currentFigurePoint"])
    field = game["layers"][0]
    print("Current XY:", x, y)
    # print("Field:", field)
    global_reply = ""
    preprocess(field, x, y, game["currentFigureType"])
    if global_reply == "":
        ws.send("")
    else:
        ws.send(global_reply)


def on_error(ws, error):
    print(error)


def on_close(ws):
    print("### closed ###")


def on_open(ws):
    pass


if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp(
        "ws://codenjoy.astanajug.net:8080/contest/ws?user=AlmaU@gmail.com&code=11488134331889285721",
        on_message=on_message,
        on_error=on_error,
        on_close=on_close)

    ws.on_open = on_open
    ws.run_forever()
