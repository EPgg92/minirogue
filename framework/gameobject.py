#!/usr/bin/env python3
# coding: utf-8
import random, json
from pprint import pprint

class GameObject():
	def __init__(self, x = 0, y = 0):
		self.x = x
		self.y = y
		self.color = 0
		self.hidden = False
		self.sym = None

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

	def regen(self, clock):
		if clock % 20 == 0:
			self.modifyHp(1)

############################################################

class Door(GameObject):
	def __init__(self, x, y, sym = "+"):
		super().__init__(x, y)
		self.sym = sym

############################################################

class Tile(GameObject):
	def __init__(self, x, y, sym = "-"):
		super().__init__(x, y)
		self.sym = sym

############################################################

class Wall(GameObject):
	def __init__(self, x, y, sym = "#"):
		super().__init__(x, y)
		self.sym = sym

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
