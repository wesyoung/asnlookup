#!/usr/bin/env python
from .data_manager import update_asnnames, update_asndb

from collections import namedtuple
import pyasn
import sys
import json

def load_asnames(fn):
    with open(fn) as f:
        return json.load(f)

ASRecord = namedtuple("ASRecord", "ip asn prefix owner")

class ASNLookup(object):
    def __init__(self):
        update_asnnames('asnames.json', 24)
        update_asndb('asn.db', 24)

        self.asndb = pyasn.pyasn('asn.db')
        self.asnames = load_asnames('asnames.json')

    def lookup_asname(self, asn):
        return self.asnames.get(str(asn))

    def lookup(self, ip):
        rec =  self.asndb.lookup(ip)
        if not rec:
            return ASRecord(ip, 'NA', 'NA', 'NA')
        asn, prefix = rec
        owner = self.lookup_asname(asn)
        return ASRecord(ip, asn, prefix, owner)

def main():
    l = ASNLookup()
    for line in sys.stdin:
        ip = line.strip()
        rec = l.lookup(ip)
        print("\t".join(str(s) for s in rec))


if __name__ == '__main__':
    main()
