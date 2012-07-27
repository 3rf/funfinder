import sys
import os
from FunFinder import FunFinder

def main(args):
    theFunFinder = FunFinder(args[1:])
    
    try:
        theFunFinder.run_unix_find()
        theFunFinder.rank_results()
        theFunFinder.dump_results()

    except OSError, e:
        print >>sys.stderr, "Execution failed:", e
        exit(1)
   
#RUN IT
main(sys.argv)

