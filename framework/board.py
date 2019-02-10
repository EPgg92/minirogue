#!/usr/bin/env python3

from framework.gameobject import *
from queue import Queue
from pprint import pprint

MAP_HEIGHT = 75
MAP_WIDTH = 75
# TODO Center Window
WIN_X = 0
WIN_Y = 0

def neighbors(current, obstacles):
    neighbors = []
    if current[0] - 1 >= 0 and (current[0] - 1, current[1]) not in obstacles:
        neighbors += [(current[0] - 1, current[1])]
    if current[0] + 1 <= MAP_WIDTH - 1 and (current[0] + 1, current[1]) not in obstacles:
        neighbors += [(current[0] + 1, current[1])]
    if current[1] - 1 >= 0 and (current[0], current[1] - 1) not in obstacles:
        neighbors += [(current[0], current[1] - 1)]
    if current[1] + 1 <= MAP_HEIGHT - 1 and (current[0], current[1] + 1) not in obstacles:
        neighbors += [(current[0], current[1] + 1)]

    return neighbors

def get_points_of_rooms(rooms):
    points = []
    for room in rooms:
        for tiles in room.tiles:
            points += [tiles]
        for wall in room.walls:
            points += [wall]
    return points

def path_find(start, end, obstacles):
    frontier = Queue()
    frontier.put(start)

    came_from = {}
    came_from[start] = None

    while not frontier.empty():
        current = frontier.get()
        if current == end:
            break
        for next in neighbors(current, obstacles):
            if next not in came_from:
                frontier.put(next)
                came_from[next] = current

    current = end
    path = []
    while current != start:
        path = [current] + path
        current = came_from[current]

    return path[:-1]

class Board():
    def __init__(self, rooms, association_of_doors):
        self.rooms = rooms

        self.obstacles = get_points_of_rooms(self.rooms)

        self.hallways = []
        for association in association_of_doors:
            hallway = Hallway((association[0].x, association[0].y),
                              (association[1].x, association[1].y),
                              self.obstacles)
            self.hallways += [hallway]

        self.all = {}
        for room in self.rooms:
            self.all.update(room.doors)
            self.all.update(room.tiles)
            self.all.update(room.walls)
        for hallway in self.hallways:
            self.all.update(hallway.tiles)


class Hallway():
    def __init__(self, start, end, obstacles):
        self.tiles = {}
        for point in path_find(start, end, obstacles):
            tile = Tile(point[0], point[1])
            tile.setSym("░")
            self.tiles[(point[0], point[1])] = tile

class Room():
    def __init__(self, x, y, width, height, doors):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.doors = {}
        self.tiles = {}
        self.walls = {}

        for door in doors:
            self.doors[(door.x, door.y)] = door

        for x in range(self.x, self.x + width):
            if (x, self.y) not in self.doors:
                wall = Wall(x, self.y)
                self.walls[(x, self.y)] = wall

            if (x, self.y + height - 1) not in self.doors:
                wall = Wall(x, self.y + height - 1)
                self.walls[(x, self.y + height - 1)] = wall

        for y in range(self.y, self.y + height):
            if (self.x, y) not in self.doors:
                wall = Wall(self.x, y)
                self.walls[(self.x, y)] = wall

            if (self.x + width - 1, y) not in self.doors:
                wall = Wall(self.x + width - 1, y)
                self.walls[(self.x + width - 1, y)] = wall

        for x in range(self.x + 1, self.x + width - 1):
            for y in range(self.y + 1, self.y + height - 1):
                tile = Tile(x, y)
                self.tiles[(x, y)] = tile
