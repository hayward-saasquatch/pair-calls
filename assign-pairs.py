#!/usr/bin/env python

import os, os.path
from datetime import date, datetime, timedelta


# A pair of names: order doesn't matter; define a custom class so we
# can use these as keys in maps.

class Pair:
    def __init__(self, n1, n2): self.p = (min(n1, n2), max(n1, n2))
    def __getitem__(self, i):   return self.p[i]
    def __eq__(self, other):    return self.p == other.p
    def __hash__(self):         return self.p.__hash__()
    def __repr__(self):         return '({}, {})'.format(self.p[0], self.p[1])
    def other(self, n):
        if   self.p[0] == n: return self.p[1]
        elif self.p[1] == n: return self.p[0]
        else:                return None


# Find the next Monday after the last week already set up (or start
# from next Monday).

def next_week():
    fs = [datetime.strptime(f.replace('.csv', ''), '%Y-%m-%d').date()
          for f in os.listdir('weeks')]
    if len(fs) > 0:
        monday = max(fs) + timedelta(days=7)
    else:
        monday = date.today()
        if monday.weekday() != 0:
            monday += timedelta(days = 7 - monday.weekday())
    return monday


# Read "latest call" map between pairs and dates.

def read_latest(names):
    latest = { }
    try:
        for l in open('latest.txt'):
            n1, n2, d = l.split(',')
            d = datetime.strptime(d.replace("\n", ''), '%Y-%m-%d').date()
            latest[Pair(n1, n2)] = d
    except:
        d = date(1970, 1, 1)
        for n1 in names:
            for n2 in names:
                if n1 != n2: latest[Pair(n1, n2)] = d
    return latest


# Write "latest call" map between pairs and dates.

def write_latest(latest):
    with open('latest.txt', 'w') as fp:
        for k, v in latest.items():
            print('{},{},{}'.format(k[0], k[1], v.strftime('%Y-%m-%d')),
                  file=fp)


# Assign pairs for calls, attempting to maximise time between calls
# between a pair.

def assign_pairs(names, latest, day):
    unassigned = set(names)
    pairs = []
    while len(unassigned) > 0:
        #print('unassigned =', unassigned)
        n1 = unassigned.pop()
        #print('n1 =', n1)
        cmap = { k:v for k, v in latest.items()
                 if n1 in k and k.other(n1) in unassigned }
        #print('cmap =', cmap)
        cpairs = sorted(cmap, key=cmap.get)
        #print('cpairs =', cpairs)
        if len(cpairs) > 0:       n2 = cpairs[0].other(n1)
        elif len(unassigned) > 0: n2 = unassigned.pop()
        else:
            others = set(names)
            others.remove(n1)
            n2 = others.pop()
        #print('n2 =', n2)
        if n2 in unassigned: unassigned.remove(n2)
        pairs.append(Pair(n1, n2))
        latest[Pair(n1, n2)] = day
    return pairs


# Output pairs file for the week being processes.

def write_pairs(pairs, monday):
    f = os.path.join('weeks', monday.strftime('%Y-%m-%d') + '.csv')
    with open(f, 'w') as fp:
        for p in pairs:
            print('{},{}'.format(p[0], p[1]))
            print('{},{}'.format(p[0], p[1]), file=fp)


def main():
    names = [n.replace("\n", '') for n in open('names.txt')]
    monday = next_week()
    print('Generating pairs for week beginning', monday)
    latest = read_latest(names)
    pairs = assign_pairs(names, latest, monday)
    write_latest(latest)
    write_pairs(pairs, monday)

if __name__ == '__main__':
    main()
