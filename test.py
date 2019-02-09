#!/usr/bin/env python3
import sys, random

class GameObject():
    def __init__(self, x, y):
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


class LivingObject(GameObject):
    def __init__(self, x, y):
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


class Player(LivingObject):
    def __init__(self, x, y):
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
                print("Degat (CC): " + str(int(round(dmg))))
            else:
                print("Degat: " + str(int(round(dmg))))
        livingObject.modifyHp(-int(round(dmg)))


class Item(GameObject):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.setDescription("unknown description")
        self.setName("unknown name")

    def setName(self, name):
        self.name = name

    def setDescription(self, description):
        self.description = description



class Food(Item):
    def __init__(self, x, y):
        super().__init__(x, y)
    
    def setHpGiven(self, hp):
        self.hpGiven = hp


class Weapon(Item):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.critChance = 0 # 0-100
        self.critCoeff = 1.5

    def setAtk(self, minAtk, maxAtk):
        self.minAtk = minAtk
        self.maxAtk = maxAtk

    def setCritChance(self, crit):
        self.critChance = crit

    def setCritCoeff(self, critCoeff):
        self.critCoeff = critCoeff

class Gold(Item):
    def __init__(self, x, y):
        super().__init__(x, y)

    def setAmount(self, amount, maxAmount = 0):
        if maxAmount <= 0:
            self.amount = amount
        else:
            self.amount = random.randint(amount, maxAmount)
    

p = Player(0, 0)
p2 = Player(0, 0)

p2.setHp(2500)

item = Food(0, 0)
item2 = Weapon(0, 0)

item2.setAtk(42, 101)
item2.setCritChance(18)
item2.setCritCoeff(2.02)

gold = Gold(0, 0)
gold.setAmount(42)

manager = [item, item2, gold]

p.equip(item2)

print(p.equippedWeapon)

while p2.hp > 0:
    p.attack(p2)
    print(p2.hp)


# def main():
#     p1 = GameObject(0, 0, 100, 22)
#     p2 = GameObject(0, 0, 101, 42)

#     print(p1.collide(p2))

# if __name__ == "__main__":
#     main()