#!/usr/bin/env python3

from curses import wrapper
from framework.gameobject import *
from framework.board import *
from framework.gamemanager import *
import curses
import sys
import random

def procedural_gen():
    w_max = int((MAP_WIDTH - 10) /3) - 1
    h_max = int((MAP_HEIGHT - 10) /3) - 1
    nb_room = 9
    room_link = [(Door(0,0), Door(0,0)) for _ in range(8)]
    rooms = {}
    i = 0
    for x in range(3):
        for y in range(3):
            rooms[i] = Room(x * w_max + 3, y * h_max + 3, random.randint(3,w_max - 1),random.randint(3, h_max - 1), [])
            i += 1
            i = 0
    for link in room_link:
        curr = rooms[i]
        suiv = rooms[i + 1]
        l_curr = link[0]
        l_suiv = link[1]
        # print(i,'curr',curr.x, curr.width, curr.y, curr.height)
        # print(i+1,'suiv',suiv.x, suiv.width, suiv.y, suiv.height)
        # print()
        x, y = (curr.x,0)
        while (x == curr.x or x == curr.width or curr.y == y or curr.height == y):
            x , y = random.choice(list(curr.walls))
            l_curr.setPosition(x, y)
            curr.doors[l_curr.x, l_curr.y] = l_curr

        x, y = (suiv.x,0)
        while (x == suiv.x or x == suiv.width or suiv.y == y or suiv.height == y):
            x , y = random.choice(list(suiv.walls))
            l_suiv.setPosition(x, y)
            suiv.doors[l_suiv.x, l_suiv.y] = l_suiv
            i+=1
    return Board([rooms[x] for x in rooms], [])
#return Board([rooms[x] for x in rooms], room_link)

def main(stdscr):
    stdscr.clear()
    if curses.COLS < MAP_WIDTH - 1 or curses.LINES < MAP_HEIGHT - 1:
        stdscr.addstr(0, 0, "Terminal Too Small")
        stdscr.getch()
        sys.exit(-1)

    curses.curs_set(0)
    curses.init_pair(1, curses.COLOR_GREEN, 0)
    curses.init_pair(2, curses.COLOR_RED, 0)
    curses.init_pair(3, curses.COLOR_YELLOW, 0)
    curses.init_pair(4, curses.COLOR_BLUE, 0)
    curses.init_pair(5, curses.COLOR_MAGENTA, 0)
    curses.init_pair(6, curses.COLOR_CYAN, 0)
    curses.init_pair(7, curses.COLOR_WHITE, curses.COLOR_WHITE)

    win = curses.newwin(MAP_HEIGHT, MAP_WIDTH, WIN_Y, WIN_X)
    win.keypad(True)

    doorA = Door(19, 40)
    doorB = Door(55, 60)

    roomA = Room(1, 1, 30, 40, [doorA])
    roomB = Room(50, 60, 10, 10, [doorB])

    board = Board([roomA, roomB], [(doorA, doorB)])
    #board = procedural_gen()

    Manager = GameManager(board)
    Manager.loadItems('items.json')
    Manager.loadMonsters('mobs.json')
    Manager.placeItem(10)
    Manager.placeMob(5)
    while True:
        win.erase()

        for _, gameObject in board.all.items():
            win.addstr(gameObject.y, gameObject.x, gameObject.sym)

        for coord in Manager.placedItems:
            item = Manager.placedItems[coord]
            item.draw(win)

        for coord in Manager.placedMobs:
            item = Manager.placedMobs[coord]
            item.draw(win)

        win.addstr(Manager.player.y, Manager.player.x, '\u263A', curses.color_pair(1))
        win.box()
        # win.redrawwin()
        win.refresh()
        key = win.getkey() # win.getch()
        if key == '`':
            break
        Manager.update(key, win)
    return (Manager.player)

if __name__ == "__main__":
    player = wrapper(main)
    print(player.__str_inventory__())
    #procedural_gen()
