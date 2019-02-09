from framework.gameobject import *
from framework.board import *

X = 100
Y = 10

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

        self.player = Player(0, 0)
        self.player.setSym('\u263A')
        
    def update(self, x, y):
        self.clock += 1
        self.checkCollision(x, y)
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
                    self.golds.append(gold)
                if "food" in id:
                    food = Food(0, 0)
                    food.setName(n["name"])
                    food.setDescription(n["description"])
                    food.setHpGiven(n["hpGiven"])
                    self.foods.append(food)

    def checkCollision(self, x, y):
            obj = self.gameObject[(x, y)]
            if obj:
                if isinstance(obj, Item):
                    if self.player.collide(obj):
                        self.player.addItem(obj)
                        self.gameObject[(x, y)].remove(obj)
                if isinstance(obj, Monster):
                    self.player.attack(obj)
                # if isinstance(obj, Wall):
                #    if self.player.collide(obj):
                #       self.player.rollBack()

    def printBoard(self):
        board = self.board
       # self.placeItem(10)
       # self.placeMob(10)
        for y in range(Y):
            for x in range(X):
                print(board[(x, y)], end = '')
            print()

    def placeItem(self, number):
        board = self.board
        while number:
            index = random.choice(list(board.keys()))
            if board[index] is '-':
                number -= 1
                board[index] = 'A'

    def placeMob(self, number):
        board = self.board
        while number:
            index = random.choice(list(board.keys()))
            if board[index] is '-':
                number -= 1
                board[index] = self.mobs[random.randint(0, len(self.mobs) - 1)].sym