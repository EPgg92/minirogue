import curses

def main():
	curses.initscr()
	curses.beep()
	curses.noecho()
	curses.curs_set(0)
	window = curses.newwin(30, 30, 0, 0)
	window.keypad(1)
	window.timeout(1)
	while True:
		window.clear()
		window.border(0)
		window.addstr(1, 1, "lol")

if __name__ == '__main__':
	main()
