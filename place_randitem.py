#!usr/bin/env python3

import random

def place_rand_item(param):
    item = []
    copy = param
    x = 0
    while (x < param):
        copy -= 1
        for i in range(copy, param):
            item.append(copy)
        x += 1
    return random.choice(item)


if __name__ == "__main__":
    for _ in range(100):
        print(place_rand_item(15))