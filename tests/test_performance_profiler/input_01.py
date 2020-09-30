import random

BIG_NUMBER = 10000000


def do_something():
    li = []
    for i in range(10000000):
        li.append(random.randint(0, BIG_NUMBER))
    li.sort()
    return li


do_something()
