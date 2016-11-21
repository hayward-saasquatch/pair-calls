#!/usr/bin/env python3

import os, os.path, sys, time
from datetime import datetime
import requests

ENDPOINT = open('slack-endpoint.txt').read().replace("\n", '')

def send(t):
    time.sleep(1)
    requests.post(ENDPOINT + "&text=" + t )

def main():
    post = ""
    if len(sys.argv) != 2:
        print('Usage: send-pairs.py <monday-date>')
        sys.exit(1)
    wbstr = sys.argv[1]
    pfile = os.path.join('weeks', wbstr + '.csv')
    if not os.path.exists(pfile):
        print('Pair file ' + pfile + ' does not exist!')
        sys.exit(1)
    wb = datetime.strptime(wbstr, '%Y-%m-%d')
    wbtitle = wb.strftime("%d %B %Y")
    if wbtitle.startswith('0'): wbtitle = wbtitle[1:]
    post = post + "<!here|here> Paired calls for the week beginning " + wbtitle + "\n"
    for l in open(pfile):
        n1, n2 = l.split(',')
        n2 = n2.replace("\n", '')
        post = post + "{} and {}".format(n1, n2) + "\n"
        
    send(post)

if __name__ == '__main__':
    main()
