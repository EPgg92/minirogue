from framework.gameobject import *
from framework.board import *
from framework.gui import *
import curses, copy, sys

MAP_HEIGHT = 75
MAP_WIDTH = 100

class GameManager():
	def __init__(self, board, gui):
		self.clock = 0
		self.golds = []
		self.weapons = []
		self.foods = []
		self.mobs = []
		self.placedItems = {}
		self.placedMobs = {}
		self.board = board
		self.player = Player(10, 10)
		self.player.setSym('\u263A')
		self.moveObstacles = []
		self.set_moveObstacles()
		self.gui = gui
		

	def reset_placedMobs(self):
		self.placedMobs = {self.placedMobs[k].getPosition() : self.placedMobs[k] for k in self.placedMobs}

	def set_moveObstacles (self):
		for x in range(MAP_WIDTH):
			for y in range(MAP_HEIGHT):
				if (x, y) in self.board.all:
					if type(self.board.all[(x, y)]) is Wall:
						self.moveObstacles.append((x,y))
				else:
					self.moveObstacles.append((x,y))

	def mobIsNear(self, monster, dist):
		p = self.player.getPosition()
		m = monster.getPosition()
		if abs(p[0] - m[0]) == 0 and abs(p[1] - m[1]) == dist:
			return True
		if abs(p[0] - m[0]) == dist and abs(p[1] - m[1]) == 0:
			return True
		return False

	def update(self, key, win):
		def inventory(win):
			win.clear()
			str0 =  self.player.__str_inventory__()
			win.addstr(1, 1, str0)
			win.addstr(MAP_HEIGHT -1, 1, " Press 'q' to quit this menu")
			win.box()
			win.refresh()
			while True:
				if win.getkey() == 'q':
					break

		def armyourself(win):
			win.clear()
			str0 = "Your equipped weapon is:\n"
			if self.player.equippedWeapon == None:
				str0 += "\tNothing! you are crazy\n"
			else:
				str0 += "\t" + self.player.equippedWeapon.name + '\n'
			str0 += ' Owned Weapons to equip:\n'
			weaplist = {}
			if self.player.weapons == []:
				str0 += "\tOh Shit, nothing! It's suck!\n"
			else:
				weaplist = {str(x + 1) : w for x, w in enumerate(self.player.weapons)}
				str0 += '\n'.join(["\t{} : {}".format(x, weaplist[x].name) for x in weaplist])
				str0 += '\n'
			win.addstr(1, 1, str0)
			#win.addstr(MAP_HEIGHT -1, 1, " Press 'q' to quit this menu or \npress a weapon number")
			win.refresh()
			while True:
				key = win.getkey()
				if key == 'q':
					break
				if key in weaplist:
					self.player.equip(weaplist[key])
					break
		self.clock += 1
		if key == 'i':
			inventory(win)
		elif key == 'u':
			armyourself(win)
		else:
			self.checkCollision(key)
			self.player.regen(self.clock)
			if self.clock >= 100:
				self.clock = 0
		coord_player = self.player.getPosition()
		for monster in self.placedMobs:
			if abs(coord_player[0] - monster[0]) <= 5 and abs(coord_player[1] - monster[1]) <= 5:
				xfm, yfm = (0, 0)
				if self.mobIsNear(self.placedMobs[monster], 1):
					dmg = self.placedMobs[monster].attack(self.player)
					self.gui.setText(Text(self.placedMobs[monster].name + " hit you for " + str(dmg) + " damages.", 1, 2))
				else:
					path = path_find(monster, coord_player, self.moveObstacles)
					if len(path) > 0:
						xfm, yfm = path[0]
						if 	(xfm, yfm) in self.board.all:
							if type(self.board.all[(xfm, yfm)]) is Tile or type(self.board.all[(xfm, yfm)]) is Door:
								self.placedMobs[monster].move(xfm, yfm)
		self.reset_placedMobs()
		self.gui.setText(Text("Gold : " + str(self.player.gold), 1, 1))
		self.gui.setText(Text("HP : " + str(self.player.hp) + "/" + str(self.player.maxHp), 16, 1))
		self.gui.setText(Text("Level : " + str(self.player.level), 30, 1))
		self.gui.setText(Text("XP : " + str(self.player.xp) + "/" + str(self.player.xpMax), 45, 1))
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
			monster.setXpGiven(d["xp"])
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
					weapon.setSym('!')
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
					food.setSym('=')
					self.foods.append(food)

	def checkCollision(self, key):
		x = self.player.x
		y = self.player.y
		if key == 'a': # curses.KEY_LEFT:
			if x > 1:
				x -= 1
		elif key == 'd': #curses.KEY_RIGHT:
			if x < MAP_WIDTH - 2:
				x += 1
		elif key == 'w': #curses.KEY_UP:
			if y > 1:
				y -= 1
		elif key == 's': #curses.KEY_DOWN:
			if y < MAP_HEIGHT - 2:
				y += 1
		if (x, y) in self.board.all:
			obj = self.board.all[(x, y)]
			if (x, y) in self.placedItems:
				self.player.addItem(self.placedItems[(x, y)])
				self.gui.setText(Text("you picked: " + self.placedItems[(x, y)].name + ".", 1, 3))
				del self.placedItems[(x, y)]
			elif (x, y) in self.placedMobs:
				dmg = self.player.attack(self.placedMobs[(x, y)])
				self.gui.setText(Text("you hit " + self.placedMobs[(x, y)].name + " for " + str(dmg) + " damages.", 1, 3))
				if self.placedMobs[(x, y)].hp <= 0:
					del self.placedMobs[(x, y)]
			if not isinstance(obj, Wall) and (x, y) not in self.placedMobs:
				self.player.move(x, y)

	def placeItem(self, number):
		save = number
		for room in self.board.rooms:
			tiles = room.tiles
			number = save
			while number:
				index = random.choice(list(tiles.keys()))
				if tiles[index]:
					number -= 1
					dict_item = random.choice([self.golds, self.weapons, self.foods])
					item = copy.deepcopy(dict_item[random.randint(0, len(dict_item) - 1)])
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
					mob = copy.deepcopy(self.mobs[random.randint(0, len(self.mobs) - 1)])
					mob.setPosition(index[0], index[1])
					self.placedMobs[index] = mob
