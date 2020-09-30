import random

BIG_NUMBER = 10000000
count = 0


def do_something():
    global count
    count *= 3
    count /= 2


for i in range(BIG_NUMBER):
    do_something()
