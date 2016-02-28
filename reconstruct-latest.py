#!/usr/bin/env python

import os
import os.path
import random
import itertools
from datetime import date, datetime, timedelta


# A pair of names: order doesn't matter; define a custom class so we
# can use these as keys in maps.

class Pair:
    def __init__(self, n1, n2): self.p = (min(n1, n2), max(n1, n2))

    def __getitem__(self, i): return self.p[i]

    def __eq__(self, other): return self.p == other.p

    def __hash__(self): return self.p.__hash__()

    def __repr__(self): return '({}, {})'.format(self.p[0], self.p[1])

    def other(self, n):
        if self.p[0] == n:
            return self.p[1]
        elif self.p[1] == n:
            return self.p[0]
        else:
            return None


# Read "latest call" map between pairs and dates.

def reconstruct_latest(names):
    latest = {}
    weeks = [os.path.splitext(f)[0] for f in sorted(os.listdir('weeks'))]
    for w in weeks:
        yr, mon, day = w.split('-')
        d = date(int(yr), int(mon), int(day))
        for l in open(os.path.join('weeks', w + '.csv')):
            n1, n2 = l.replace("\n", '').split(',')
            latest[Pair(n1, n2)] = d
    return latest


# Write "latest call" map between pairs and dates.

def write_latest(latest):
    with open('reconstructed-latest.txt', 'w') as fp:
        for k, v in latest.items():
            print('{},{},{}'.format(k[0], k[1], v.strftime('%Y-%m-%d')),
                  file=fp)


def main():
    names = [n.replace("\n", '') for n in open('names.txt')]
    latest = reconstruct_latest(names)
    write_latest(latest)

if __name__ == '__main__':
    main()
