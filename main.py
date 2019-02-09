#!/usr/bin/env python3


from curses import wrapper
from framework.gameobject import *
from framework.board import *
from framework.gamemanager import *
import curses
import sys

from collections import defaultdict as dd

import time

def main(stdscr):
    stdscr.clear()

    if curses.COLS < MAP_WIDTH - 1 or curses.LINES < MAP_HEIGHT - 1:
        print("Terminal Too Small", file=sys.stderr)
        sys.exit(-1)

    curses.curs_set(0)
    win = curses.newwin(MAP_HEIGHT, MAP_WIDTH, WIN_Y, WIN_X)
    win.keypad(True)

    doorA = Door(18, 39)
    doorB = Door(55, 60)

    roomA = Room(0, 0, 30, 40, [doorA])
    roomB = Room(50, 60, 10, 10, [doorB])

    board = Board([roomA, roomB], [(doorA, doorB)])

    Manager = GameManager(board)
    Manager.loadItems('items.json')
    Manager.loadMonsters('mobs.json')
    Manager.placeItem(4)
    Manager.placeMob(2)
   # Manager.printBoard()
    while True:
        win.erase()

        for _, gameObject in board.all.items():
            win.addstr(gameObject.y, gameObject.x, gameObject.sym)

        for coord in Manager.placedItems:
            item = Manager.placedItems[coord]
            win.addstr(item.y, item.x, item.sym)

        for coord in Manager.placedMobs:
            item = Manager.placedMobs[coord]
            win.addstr(item.y, item.x, item.sym)
        win.addstr(Manager.player.y, Manager.player.x, "\u263b")
        win.refresh()
        key = win.getch()
        Manager.checkCollision(key)


if __name__ == "__main__":
    wrapper(main)
