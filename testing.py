import time
import sys


def print_bar(progress, iterLen, length=50, fill='█', prefix=''):
    ratio = iterLen / length
    barProg = int(progress / ratio)
    bar = fill * barProg + '-' * int(length - barProg)
    sys.stdout.write(f'\r{prefix} |{bar}| {round(((progress / iterLen) * 100), 1)}% Complete')
    sys.stdout.flush()


for i in range(100):
    print_bar(i + 1, 100)
    time.sleep(0.1)
