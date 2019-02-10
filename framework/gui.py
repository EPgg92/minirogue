from framework.gameobject import *
import curses

# wouesh ptit comment pour le merge :P

class Text():
    def __init__(self, text, x, y):
        self.value = str(text)
        self.x = x
        self.y = y

class Gui():
    def __init__(self, x, y, width, height, win):
        self.vertical = "\u007c"
        self.horizontal = "\u2015"
        self.x = x
        self.y = y
        self.width = width + x
        self.height = height + y
        self.win = win
        self.relx = x + 1
        self.rely = y + 1
        self.texts = []

    def draw(self):
        self.drawBorder()
        for text in self.texts:
            self.win.addstr(text.y + self.rely, text.x + self.relx, text.value)

    def drawBorder(self):
        x = self.x
        y = self.y
        for self.x in range(self.width):
            for self.y in range(self.height):
                if self.y == y or self.y == self.height - 1:
                    self.win.addstr(self.y, self.x, self.horizontal)
                elif self.x == x:
                    self.win.addstr(self.y, self.x, self.vertical)
                elif self.width - 1 - self.x == 0:
                    self.win.addstr(self.y, self.x, self.vertical)
                elif self.height - 1 - self.y == 0:
                    self.win.addstr(self.y, self.x, self.horizontal)
                else:
                    self.win.addstr(self.y, self.x, ' ')
        self.x = x
        self.y = y

    def setText(self, text):
        self.texts.append(text)
