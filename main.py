#!/usr/bin/env python3

from framework.gameobject import *

def main():
    p1 = Player(25, 25)
    gameManager = GameManager()
    gameManager.loadItems('items.json')
    for n in gameManager.golds:
        print(n.name, n.amount)
    for n in gameManager.foods:
        print(n.name, n.hpGiven)
    for n in gameManager.weapons:
        print(n.name)
    print(u'\u263B')

if __name__ == "__main__":
    main()