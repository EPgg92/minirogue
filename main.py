#!/usr/bin/env python3

from curses import wrapper
from framework.gameobject import *
from framework.board import *
from framework.gamemanager import *
import curses
import sys

def main(stdscr):
    stdscr.clear()

    if curses.COLS < MAP_WIDTH - 1 or curses.LINES < MAP_HEIGHT - 1:
        stdscr.addstr(0, 0, "Terminal Too Small")
        stdscr.getch()
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
   # Manager.printBoard()
    player_x, player_y = 15, 15
    mob_x, mob_y = 3, 15
    while True:

        obstacles = []
        for x in range(MAP_WIDTH):
            for y in range(MAP_HEIGHT):
                if ((x, y) in board.all and not isinstance(board.all[(x, y)], (Tile, Door)))\
                or (x, y) not in board.all:
                        obstacles += [(x, y)]

        path = path_find((mob_x, mob_y), (player_x, player_y), obstacles)
        # print(path, file=sys.stderr)
        if len(path) > 0:
            mob_x = path[0][0]
            mob_y = path[0][1]

        win.erase()
        for _, gameObject in board.all.items():
            win.addstr(gameObject.y, gameObject.x, gameObject.sym)



        win.addstr(player_y, player_x, "\u263b")
        win.addstr(mob_y, mob_x, "X")
        win.refresh()
        key = win.getch()
        if key == curses.KEY_LEFT:
            if player_x > 1:
                player_x -= 1
        elif key == curses.KEY_RIGHT:
            if player_x < MAP_WIDTH - 2:
                player_x += 1
        elif key == curses.KEY_UP:
            if player_y > 1:
                player_y -= 1
        elif key == curses.KEY_DOWN:
            if player_y < MAP_HEIGHT - 2:
                player_y += 1


if __name__ == "__main__":
    wrapper(main)
