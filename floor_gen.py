#!usr/bin/env/Python3

# Genere entre 5 et 9 rooms pour un etage

import random as rand
import sys

class Terrain:                                                  #classe Mere useless (for now)
    def __init__(self, width, height):
        self.width = width
        self.height = height

class Room(Terrain):
    def __init__(self, width, height, abs_orig, content):
        Terrain.__init__(self, width, height)
        self.abs_orig = abs_orig
        self.content = content

class Tunnel(Terrain):
    def __init__(self, width, height, length):
        Terrain.__init__(self, width, height)
        self.length = length

#################################################################

def place_stairs(width, height):
    pos = 0
    while (pos % width == 0 or (pos + 1) % width == 0):          #tant qu'on a roll une mauvaise pos (sur un mur Est ou Ouest)
        pos = rand.randint(width + 1, height * (width - 1))      #reroll une position entre le mur Nord et le mur Sud
    return pos

#################################################################

def room_gen(stairs):                                            #un seul param (creer un escalier ou non)
    width = rand.randint(7,20)                                   #get room width
    height = rand.randint(5,15)                                  #get room height
    content = ['.'] * (width * height)                           #content = set tous les char de la room avec '.'
    if (stairs):
        stairs_pos = place_stairs(width, height)                 
    room = Room(width, height, 0, content)                       #creation d'une instance room
    for i in range(0, width * height):                           #pose murs "|" et "_" aux extremites
        if (i < width or i > width * (height - 1) - 1):          
            room.content[i] = '_'
        elif ((i and i != width * (height - 1) and i % width == 0) or (i + 1) % width == 0):
            room.content[i] = '|'
        else:
            if (stairs and i == stairs_pos):
                room.content[i] = '>'
            else:
                room.content[i] = '.'
    return (room)                                    

################################################################

def floor_gen():
    max_room = rand.randint(5,10)                               #choisit le nombre de pieces par etage (entre 5 et 9)
    stairs_room = rand.randint(0, max_room)                     #choisit la piece qui contient des escaliers (1 par etage)
    floor = []
    for x in range(max_room):
        if (x == stairs_room):
            room = room_gen(1)
        else:
            room = room_gen(0)
        # for y in range (0, room.width * room.height):         #
        #     sys.stdout.write(room.content[y])                 #
        #     sys.stdout.flush()                                # } affichage (debug) de la room generee
        #     if ((y + 1)% room.width == 0):                    #
        #         y += 1                                        #
        #         print('\n')                                   #
        # print('\n')
        floor.append(room)                                      #stockage de la room dans la liste 'floor'
    return (floor)

################################################################

def main(void):
    #floor_display()
    floor_gen()


if __name__ == '__main__':
    main(0)
