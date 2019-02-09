#!/usr/bin/env python3

import sys
from pprint import pprint


def room(w, h):
    d = {}
    for x in range(w):
        for y in range(h):
            if (x == 0 or y == 0 or x == w - 1 or y == h - 1):
                d[(x, y)] = '#'
            else:
                d[(x, y)] = '-'
    return d         