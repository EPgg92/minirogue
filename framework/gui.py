from framework.gameobject import *
import curses

# wouesh ptit comment pour le merge :P

MAP_WIDTH = 100

class Text():
    def __init__(self, text, x, y):
        self.value = str(text)
        self.x = x
        self.y = y

class Gui():
    def __init__(self, win):
        self.win = win
        self.texts = []

    def draw(self):
        self.drawBorder()
        for text in self.texts:
            self.win.addstr(text.y, text.x, text.value)
        self.texts.clear()

    def drawBorder(self):
        x = 0
        y = 0
        for x in range(MAP_WIDTH):
            for y in range(5):
                if y < 4:
                    self.win.addstr(y, x, ' ')
                else:
                    self.win.addstr(y, x, u"\u2015")

    def setText(self, text):
        self.texts.append(text)
