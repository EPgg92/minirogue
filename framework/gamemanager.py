from framework.gameobject import *
from framework.board import *
import curses

MAP_HEIGHT = 75
MAP_WIDTH = 100

class GameManager():
    def __init__(self, board):
        self.clock = 0

        self.golds = []
        self.weapons = []
        self.foods = []
        self.mobs = []

        self.placedItems = {}
        self.placedMobs = {}
        self.board = board

		# x , y = (0,)

        self.player = Player( 10, 10)
        self.player.setSym('\u263A')

    def update(self, key):
        self.clock += 1
        self.checkCollision(key)
        self.player.regen(self.clock)
        if self.clock >= 100:
            self.clock = 0


    def loadMonsters(self, path):
        with open(path) as file:
            data = json.load(file)
        for d in data:
            monster = Monster(0,0)
            monster.setSym(d["symbol"])
            monster.setAtk(d["min"], d["max"])
            monster.setCritCoeff(d["critCoeff"])
            monster.setCritChance(d["critChance"])
            monster.setName(d["name"])
            monster.setHp(d["hp"])
            monster.updateDamage()
            self.mobs.append(monster)

    def loadItems(self, path):
        with open(path) as file:
            data = json.load(file)
        for id in data:
            for n in data[id]:
                if "weapon" in id:
                    weapon = Weapon(0, 0)
                    weapon.setName(n["name"])
                    weapon.setDescription(n["description"])
                    weapon.setAtk(n["min"], n["max"])
                    weapon.setCritChance(n["critChance"])
                    weapon.setCritCoeff(n["critCoeff"])
                    self.weapons.append(weapon)
                if "gold" in id:
                    gold = Gold(0, 0)
                    gold.setName(n["name"])
                    gold.setDescription(n["description"])
                    gold.setAmount(n["min"], n["max"])
                    gold.setSym('$')
                    self.golds.append(gold)
                if "food" in id:
                    food = Food(0, 0)
                    food.setName(n["name"])
                    food.setDescription(n["description"])
                    food.setHpGiven(n["hpGiven"])
                    self.foods.append(food)

    def checkCollision(self, key):
        x = self.player.x
        y = self.player.y
        if key == curses.KEY_LEFT:
            if x > 1:
                x -= 1
        elif key == curses.KEY_RIGHT:
            if x < MAP_WIDTH - 2:
                x += 1
        elif key == curses.KEY_UP:
            if y > 1:
                y -= 1
        elif key == curses.KEY_DOWN:
            if y < MAP_HEIGHT - 2:
                y += 1
        if (x, y) in self.board.all:
            obj = self.board.all[(x, y)]
            if (x, y) in self.placedItems:
                self.player.addItem(self.placedItems[(x, y)])
                del self.placedItems[(x, y)]
            elif (x, y) in self.placedMobs:
                self.player.attack(self.placedMobs[(x, y)])
                if self.placedMobs[(x, y)].hp <= 0:
                    del self.placedMobs[(x, y)]
            if not isinstance(obj, Wall) and (x, y) not in self.placedMobs:
                self.player.move(x, y)


    # def printBoard(self):
    #     board = self.board
    #     for y in range(Y):
    #         for x in range(X):
    #             print(board[(x, y)], end = '')
    #         print()

    def placeItem(self, number):
        save = number
        for room in self.board.rooms:
            tiles = room.tiles
            number = save
            while number:
                index = random.choice(list(tiles.keys()))
                if tiles[index]:
                    number -= 1
                    item = self.golds[random.randint(0, len(self.golds) - 1)]
                    item.setPosition(index[0], index[1])
                    self.placedItems[index] = item

    def placeMob(self, number):
        save = number
        for room in self.board.rooms:
            tiles = room.tiles
            number = save
            while number:
                index = random.choice(list(tiles.keys()))
                if tiles[index]:
                    number -= 1
                    mob = self.mobs[random.randint(0, len(self.mobs) - 1)]
                    mob.setPosition(index[0], index[1])
                    self.placedMobs[index] = mob
