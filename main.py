#!/usr/bin/env python3


from curses import wrapper
from framework.gameobject import *
from framework.board import *
from framework.gamemanager import *
import curses
import sys


#from collections import defaultdict as dd

import time

def main(stdscr):
	stdscr.clear()

	if curses.COLS < MAP_WIDTH - 1 or curses.LINES < MAP_HEIGHT - 1:
		print("Terminal Too Small", file=sys.stderr)
		return (64)
	curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
	curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
	curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)
	curses.curs_set(0)
	win = curses.newwin(MAP_HEIGHT, MAP_WIDTH, WIN_Y, WIN_X)
	win.keypad(True)
	win.box()
	doorA = Door(19, 40)
	doorB = Door(55, 60)

	roomA = Room(1, 1, 30, 40, [doorA])
	roomB = Room(50, 60, 10, 10, [doorB])

	board = Board([roomA, roomB], [(doorA, doorB)])

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
			win.addstr(item.y, item.x, item.sym, curses.color_pair(3))

		for coord in Manager.placedMobs:
			item = Manager.placedMobs[coord]
			win.addstr(item.y, item.x, item.sym, curses.color_pair(2))

		win.addstr(Manager.player.y, Manager.player.x, '\u263A', curses.color_pair(1))
		win.border('|', '|', '-', '-', '+', '+', '+', '+')
		win.refresh()
		key = win.getkey() # win.getch()
		if key == '`':
			break
		Manager.update(key)
	return (Manager.player)

if __name__ == "__main__":
	player = wrapper(main)
	print(player.__str_inventory__())
