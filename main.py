#!/usr/bin/env python3

from framework.gameobject import *

def main():
    p1 = Player(25, 25)
    gameManager = GameManager()
    gameManager.loadItems('items.json')
    gameManager.loadMonsters('mobs.json')
    gameManager.printBoard()

if __name__ == "__main__":
    main()