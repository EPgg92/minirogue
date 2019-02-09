#!/usr/bin/env python3
import sys

class GameObject():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.color = 0
        self.hidden = False
        self.sym = '#'

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
            self.destroy()
        if self.hp > self.maxHp:
            self.hp = self.maxHp
    
    def setHp(self, hp):
        self.hp = hp
    
    def setMaxHp(self, maxHp):
        self.maxHp = maxHp

    def setDamage(self, damage):
        self.damage = damage

    def setLevel(self, level):
        self.level = level


class Player(LivingObject):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.items = []
        self.setHp(30)
        self.setMaxHp(30)
        self.setDamage(10)
        self.setColor(0xFF0000)
        self.setPosition(0, 0)
        self.setLevel(1)


    def eat(self, food):
        self.modifyHp(food.hp)
        self.delItem(food)

    def addItem(self, item):
        self.items.append(item)

    def delItem(self, item):
        self.items.remove(item)


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


p = Player(0, 0)

item = Food(0, 0)

manager = [item]

print(manager)
print(p.items)

if p.collide(item):
    p.addItem(item)

print(manager)
print(p.items)

# def main():
#     p1 = GameObject(0, 0, 100, 22)
#     p2 = GameObject(0, 0, 101, 42)

#     print(p1.collide(p2))

# if __name__ == "__main__":
#     main()