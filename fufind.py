import sys
import os
from FunFinder import FunFinder

def main(args):
    theFunFinder = FunFinder(args[1:])
    
    try:
        theFunFinder.run_unix_find()
    except OSError, e:
        print >>sys.stderr, "Execution failed:", e

    print theFunFinder.findResults

#RUN IT
main(sys.argv)

