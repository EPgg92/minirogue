#!/usr/bin/env python3

from framework.gameobject import *

def main():
    p1 = Player(25, 25)
    gameManager = GameManager()
    gameManager.loadItems('items.json')
    for n in gameManager.golds:
        print(n.name, n.amount)

if __name__ == "__main__":
    main()