#!/usr/bin/env python
# encoding: utf-8
"""
test_engine.py

Created by Bart Desmet on 2012-09-26.
Copyright (c) 2012 LT3. All rights reserved.
"""

import sys
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


def main(processes = 1, runs = 100, store_grids = False):
    grids = [] # Deze lijst wordt nogal groot na verloop van tijd, omdat er volledige grids in worden opgeslagen. Met 10000 runs was dat 50MB, dus met 1 miljoen runs (voor 1 engine) is dat al 5GB. Gelukkig heb ik sinds kort 16 GB RAM, dus we kunnen 2 engines een miljoen spelletjes tegen elkaar laten spelen, no problem. Bovendien is het opslaan van volledige grids enkel nuttig voor het testen van engines, kwestie van statistische analyses te kunnen doen op de performance. Bij het effectieve battlen moeten we enkel de grand totals onthouden.
    if processes == 1: # Running sequentially
        runcounter = 0
        for run in range(runs):
            runcounter += 1
            if runcounter % 1000 == 0:
                print runcounter, "of", runs, "games played"
            grids.append(automahtzee.main(1, True))
    elif 1 < processes < 33: # Multiprocessing pwnz0r!!
        pool = Pool(processes)
        grids = pool.map(automahtzee.main, range(runs))
    else:
        print >>sys.stderr, "Too many processes:", processes
        sys.exit(1)
    
    print "Minimum, average and maximum grand total:", get_min(grids, "gt"), get_avg(grids, "gt"), get_max(grids, "gt")
    print "Yahtzee hit percentage:", get_hit_pct(grids, "yz")
    print "Yahtzee bonus hit percentage:", get_hit_pct(grids, "yb")
    # print sum(grids)/float(runs)


if __name__ == "__main__":
    try: processes = int(sys.argv[1])
    except IndexError: processes = 4
    try: runs = int(sys.argv[2])
    except IndexError: runs = 1000
    main(processes, runs, store_grids = False)
