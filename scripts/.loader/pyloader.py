
### LXCONFIG - PYLOADER V1 ###
# Copyright Michael Davis (2022)

import subprocess
import functools
import hashlib

FMODE_OVERWRITE = 'W'
FMODE_APPEND = 'A'

HOME = ".loader/syms/"

class Sym(object):
    def __init__ (self, name):
        self.name = name
        self.path = name.replace (".", "/")
        self.status = self._loadFile ()

    def _loadFile(self):
        rc = -1
        try:
            with open (HOME + self.path, 'r+') as fOd:
                self.bin = fOd.read()
                rc = 0
        except FileNotFoundError:
            self.sourceData = None
        return rc



class SymLink(object):
    links = []
    longest = 0

    def __init__ (self, source, dest, fmode):
        self.source = source
        self.dest = dest
        self.fmode = fmode
        self.status = self._load_source()
        print (self.status)


        SymLink.links.append (self)
        SymLink.longest = SymLink.longest if SymLink.longest >= len(self.source) else len(self.source)

    def _load_source (self):
        rc = -1
        try:
            with open (self.source, 'rb') as fOd:
                self.sourceData = fOd.read()
                print (hex_hash(self.sourceData))
                rc = 0
        except FileNotFoundError:
            self.sourceData = None
        return rc

    def __repr__ (self):
        return f'{self.source.ljust (self.longest)} => {self.dest}'

    #@staticmethod
    #def longest ():
    #    return functools.reduce (lambda a, b: a if a >= len(b.source) else len(b.source), SymLink.links, 0)


def hex_hash (data, encode=False):
    data = data.encode("utf-8") if encode else data
    return hashlib.sha1(data).hexdigest()
        

def main ():
    SymLink (HOME + "settings/vimrc", "~/.vimrc", FMODE_OVERWRITE)
    SymLink ("../settings/vimwerqwerjqorjrc", "~/.vimrc", FMODE_OVERWRITE)
    SymLink ("../settings/vimasdfasdfrc", "~/.vimrc", FMODE_OVERWRITE)

    print ("Source  %s  Destination" % (' ' * (SymLink.longest - 6)))
    print ("-" * (SymLink.longest + 15))
    for link in SymLink.links:
        print (hex_hash(link.source, True)[0:20])
        print (link.sourceData)

    Sym("aliases")




if __name__ == '__main__':
    print ('\nPYLOADER - V1\n')
    main()
    print ()
