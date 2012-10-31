#!/usr/bin/env python
# encoding: utf-8
"""
gerard.py

Created by Bart Desmet on 2012-09-26.
Copyright (c) 2012 LT3. All rights reserved.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../")
from multiprocessing import Pool # Dit kunnen we hiervoor maar beter gebruiken :)
from engines import automahtzee

def get_avg(grids, position):
    """Returns the average score for a position, over all grids in results"""
    return sum(grid.return_score_or_zero(position) for grid in grids)/float(len(grids))


def get_min(grids, position):
    return min(grid.return_score_or_zero(position) for grid in grids)


def get_max(grids, position):
    return max(grid.return_score_or_zero(position) for grid in grids)


def get_hit_pct(grids, position):
    return sum(1 for grid in grids if grid.return_score_or_zero(position))/float(len(grids))


def solo(engine, threads = 1, games = 100, store_grids = False):
    grids = [] # Deze lijst wordt nogal groot na verloop van tijd, omdat er volledige grids in worden opgeslagen. Met 10000 runs was dat 50MB, dus met 1 miljoen runs (voor 1 engine) is dat al 5GB. Gelukkig heb ik sinds kort 16 GB RAM, dus we kunnen 2 engines een miljoen spelletjes tegen elkaar laten spelen, no problem. Bovendien is het opslaan van volledige grids enkel nuttig voor het testen van engines, kwestie van statistische analyses te kunnen doen op de performance. Bij het effectieve battlen moeten we enkel de grand totals onthouden.
    if threads == 1: # Running sequentially
        runcounter = 0
        for game in range(games):
            gamecounter += 1
            if gamecounter % 1000 == 0:
                print gamecounter, "of", games, "games played"
            grids.append(engine.main(1, True))
    elif 1 < threads < 33: # Multiprocessing pwnz0r!!
        pool = Pool(threads)
        grids = pool.map(engine.main, range(games))
    else:
        print >>sys.stderr, "Too many processes:", threads
        sys.exit(1)
    
    print "Minimum, average and maximum grand total:", get_min(grids, "gt"), get_avg(grids, "gt"), get_max(grids, "gt")
    print "Yahtzee hit percentage:", get_hit_pct(grids, "yz")
    print "Yahtzee bonus hit percentage:", get_hit_pct(grids, "yb")
    # print sum(grids)/float(games)


def CLParser():
    '''Parses the command line arguments and returns them.'''
    import argparse
    parser = argparse.ArgumentParser(description = "Let's play some Yeahtzee!", epilog = "And that, my friends, is how it's done.")
    parser.add_argument("-t", "--threads", type = int, default = 4, help="Maximum number of simultaneous threads")
    parser.add_argument("-g", "--games", type = int, default = 100, help="Number of games to be played")
    parser.add_argument("-e", "--engines", nargs = "*", default = [], help="Engines participating in the tournament. Options for an engine can be appended with dots.")
    arguments = parser.parse_args()
    
    try: threads = int(arguments.threads)
    except ValueError:
        print >>sys.stderr, "Enter a valid number for option -t"
        sys.exit(1)
    
    try: games = int(arguments.games)
    except ValueError:
        print >>sys.stderr, "Enter a valid number for option -g"
        sys.exit(1)
    
    try: assert arguments.engines
    except AssertionError:
        print >>sys.stderr, "Specify engines using the -e option"
        sys.exit(1)
    
    engines = []
    for engine_caller in arguments.engines:
        engine_fields = engine_caller.split(".")
        try:
            engine_module = __import__("engines.%s" % engine_fields[0], fromlist=["engines"])
            engine = (engine_module, engine_fields[1:])
            engines.append(engine)
        except ImportError:
            print >>sys.stderr, "Could not find engine module '%s'" % engine_fields[0]
            sys.exit(1)
    print engines
    
    return threads, games, engines


if __name__ == "__main__":
    threads, games, engines = CLParser()
    solo(engines[0][0], threads, games, store_grids = False)
