#!/usr/bin/env python3

import os, os.path
from datetime import datetime

def main():
    ds = sorted([datetime.strptime(f.replace('.csv', ''), '%Y-%m-%d').date()
                 for f in os.listdir('weeks')])
    with open('all-pair-calls.csv', 'w') as fp:
        print('"Week beginning","Caller 1","Caller 2"', file=fp)
        for d in ds:
            dout = d.strftime('%d %b %Y')
            f = os.path.join('weeks', d.strftime('%Y-%m-%d') + '.csv')
            first = True
            for l in open(f).readlines():
                n1, n2 = l.split(',')
                print('"{}","{}","{}"'.format(dout if first else '',
                                              n1, n2.replace("\n", '')),
                      file=fp)
                first = False

if __name__ == '__main__':
    main()
