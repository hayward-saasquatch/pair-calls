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
            monday += timedelta(days=7-monday.weekday())
    return monday


# Read "latest call" map between pairs and dates.

def read_latest(names):
    latest = {}
    try:
        for l in open('latest.txt'):
            n1, n2, d = l.split(',')
            d = datetime.strptime(d.replace("\n", ''), '%Y-%m-%d').date()
            latest[Pair(n1, n2)] = d
    except:
        d = date(1970, 1, 1)
        for n1 in names:
            for n2 in names:
                if n1 != n2:
                    latest[Pair(n1, n2)] = d
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
    # Make list of all possible pairs.
    all_pairs = list(set([Pair(n1, n2) for n1 in names for n2 in names
                          if n1 != n2]))
    npairs = len(all_pairs)

    # Add default last meeting times and random tiebreakers.
    tiebreakers = list(range(0, npairs))
    random.seed()
    random.shuffle(tiebreakers)
    keys = zip(itertools.repeat(date(1970, 1, 1)), tiebreakers)
    all_pairs = dict(zip(all_pairs, keys))

    # Set last meeting times.
    for k, v in latest.items():
        all_pairs[k] = (v, all_pairs[k][1])

    # Sort by meeting times and tiebreakers.
    work_pairs = sorted(all_pairs.keys(), key=lambda k: all_pairs[k],
                        reverse=True)
    left_pairs = work_pairs

    # Pull out oldest pairs.
    pairs = []
    while len(work_pairs) > 0:
        pair = work_pairs.pop()
        work_pairs = [p for p in work_pairs if pair[0] not in p]
        work_pairs = [p for p in work_pairs if pair[1] not in p]
        pairs.append(pair)
        latest[pair] = day

    # If there is an odd number of people, we'll be missing someone.
    # Work out who.
    if len(names) % 2 == 1:
        left_name = names
        for i in range(len(pairs)):
            left_name = [n for n in left_name if n not in pairs[i]]
        left_name = left_name[0]

        # Get the oldest pair for the missing person.
        left_pairs = [p for p in left_pairs if left_name in p]
        pair = left_pairs.pop()
        pairs.append(pair)
        latest[pair] = day

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
