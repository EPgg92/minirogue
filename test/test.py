#!/usr/bin/env python3

import sys

def lol(param):
	if (param > 1):
		print("LOL" + str(param))
	print("qwertyu")

def main():
	print(sys.argv)
	if (len(sys.argv) > 1):
		lol(int(sys.argv[1]))

if __name__ == '__main__':
	main()
