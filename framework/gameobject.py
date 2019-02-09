#!/usr/bin/env python3
# coding: utf-8
import random, json
from pprint import pprint
from framework.room import room


class GameObject():
    def __init__(self, x = 0, y = 0):
        self.x = x
        self.y = y
        self.color = 0
        self.hidden = False
        self.sym = None

    def draw(window):
        pass

    def setColor(self, color):
        self.color = color

    def setSym(self, sym):
        self.sym = sym

    def setHidden(self, hidden):
        self.hidden = hidden

    def setPosition(self, x, y):
        self.x = x
        self.y = y

    def isHidden(self):
        return self.hidden

    def destroy(self):
        del(self)

############################################################

class LivingObject(GameObject):
    def __init__(self, x = 0, y = 0):
        super().__init__(x, y)
        self.level = 1

    def collide(self, gameObject):
        return self.x == gameObject.x and self.y == gameObject.y

    def move(self, x, y):
        self.setPosition(x, y)

    def attack(self, livingObject):
        livingObject.modifyHp(-self.damage)

    def modifyHp(self, hp):
        self.hp += hp
        if self.hp <= 0:
            self.hp = 0
            self.destroy()
        if self.hp > self.maxHp:
            self.hp = self.maxHp

    def setHp(self, hp):
        self.hp = hp
        self.setMaxHp(hp)

    def setMaxHp(self, maxHp):
        self.maxHp = maxHp

    def setDamage(self, damage):
        self.damage = damage

    def setLevel(self, level):
        self.level = level
############################################################


class Monster(LivingObject):
    def __init__(self, x = 0, y = 0):
        super().__init__(x, y)

    def setAtk(self, minAtk, maxAtk):
        self.minAtk = minAtk
        self.maxAtk = maxAtk

    def setCritChance(self, critChance):
        self.critChance = critChance

    def setCritCoeff(self, critCoeff):
        self.critCoeff = critCoeff

    def updateDamage(self):
        dmg = random.randint(self.minAtk, self.maxAtk)
        rand = random.randint(0, 100)
        if self.critChance >= rand:
            dmg *= self.critCoeff
        super().setDamage(int(round(dmg)))

    def setName(self, name):
        self.name = name

    def move(self, x, y):
        self.updateDamage()
        self.setPosition(x, y)


############################################################

class Player(LivingObject):
    def __init__(self, x = 0, y = 0):
        super().__init__(x, y)
        self.gold = 0
        self.foods = []
        self.weapons = []
        self.setHp(30)
        self.setMaxHp(30)
        self.setDamage(10)
        self.setColor(0xFF0000)
        self.setPosition(0, 0)
        self.setLevel(1)
        self.equippedWeapon = None

    def eat(self, food):
        self.modifyHp(food.hp)
        self.delItem(food)

    def addItem(self, item):
        if isinstance(item, Food):
            self.foods.append(item)
        if isinstance(item, Weapon):
            self.weapons.append(item)
        if isinstance(item, Gold):
            self.gold += item.amount

    def delItem(self, item):
        if isinstance(item, Food):
            self.foods.remove(item)
        if isinstance(item, Weapon):
            self.weapons.remove(item)

    def equip(self, item):
        self.equippedWeapon = item

    def attack(self, livingObject):
        dmg = self.damage
        if self.equippedWeapon:
            dmg += random.randint(self.equippedWeapon.minAtk, self.equippedWeapon.maxAtk)
            rand = random.randint(0, 100)
            if self.equippedWeapon.critChance >= rand:
                dmg *= self.equippedWeapon.critCoeff
        livingObject.modifyHp(-int(round(dmg)))

    def regen(clock):
        if clock % 20 == 0:
            self.modifyHp(1)

############################################################

class Item(GameObject):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.setDescription("unknown description")
        self.setName("unknown name")

    def setName(self, name):
        self.name = name

    def setDescription(self, description):
        self.description = description

############################################################

class Food(Item):
    def __init__(self, x, y):
        super().__init__(x, y)

    def setHpGiven(self, hp):
        self.hpGiven = hp

############################################################

class Weapon(Item):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.critChance = 0
        self.critCoeff = 1.5

    def setAtk(self, minAtk, maxAtk):
        self.minAtk = minAtk
        self.maxAtk = maxAtk

    def setCritChance(self, crit):
        self.critChance = crit

    def setCritCoeff(self, critCoeff):
        self.critCoeff = critCoeff

############################################################

class Gold(Item):
    def __init__(self, x, y):
        super().__init__(x, y)

    def setAmount(self, amount, maxAmount = 0):
        if maxAmount <= 0:
            self.amount = amount
        else:
            self.amount = random.randint(amount, maxAmount)

############################################################

X = 100
Y = 10

class GameManager():
    def __init__(self):
        self.clock = 0

        self.golds = []
        self.weapons = []
        self.foods = []
        self.mobs = []

        self.placedItems = {}
        self.placedMobs = {}
        self.board = room(X, Y)

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
        self.placeMob(10)
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