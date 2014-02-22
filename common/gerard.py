#!/usr/bin/env python
# encoding: utf-8
"""
gerard.py

Central game administration

Created by Bart Desmet on 2012-09-26.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../")


from multiprocessing import Pool # Dit kunnen we hiervoor maar beter gebruiken :)
from engines import automahtzee
# import game as g

class Game(object):
    def __init__(self):
        pass


def get_avg(grids, position):
    """Returns the average score for a position, over all grids in results"""
    return sum(grid.return_score_or_zero(position) for grid in grids)/float(len(grids))


def get_min(grids, position):
    return min(grid.return_score_or_zero(position) for grid in grids)


def get_max(grids, position):
    return max(grid.return_score_or_zero(position) for grid in grids)


def get_hit_pct(grids, position):
    return sum(1 for grid in grids if grid.return_score_or_zero(position))/float(len(grids))


class Tournament(object):
    def __init__(self, engines, threads, games):
        self.engines = engines
        self.threads = threads
        self.games = games
    
    
    def play_game(self):
        return self.engines[0][0].main(1, True)
    
    
    def __call__():
        Tournament.play_tournament()
    
    
    def play_tournament(self):
        self.stored_games = [] # Deze lijst wordt nogal groot na verloop van tijd, omdat er volledige grids in worden opgeslagen. Met 10000 runs was dat 50MB, dus met 1 miljoen runs (voor 1 engine) is dat al 5GB. Gelukkig heb ik sinds kort 16 GB RAM, dus we kunnen 2 engines een miljoen spelletjes tegen elkaar laten spelen, no problem. Bovendien is het opslaan van volledige grids enkel nuttig voor het testen van engines, kwestie van statistische analyses te kunnen doen op de performance. Bij het effectieve battlen moeten we enkel de grand totals onthouden.
        if self.threads == 1: # Running sequentially
            self.gamecounter = 0
            for game in range(self.games):
                self.gamecounter += 1
                if self.gamecounter % 1000 == 0:
                    print self.gamecounter, "of", self.games, "games played"
                self.stored_games.append(self.play_game())
        elif 1 < self.threads < 33: # Multiprocessing pwnz0r!!
            pool = Pool(self.threads)
            self.stored_games = pool.map(self.play_game, range(self.games))
        else:
            print >>sys.stderr, "Too many processes:", self.threads
            sys.exit(1)
        
        print "Minimum, average and maximum grand total:", get_min(self.stored_games, "gt"), get_avg(self.stored_games, "gt"), get_max(self.stored_games, "gt")
        print "Yahtzee hit percentage:", get_hit_pct(self.stored_games, "yz")
        print "Yahtzee bonus hit percentage:", get_hit_pct(self.stored_games, "yb")
        # print sum(self.stored_games)/float(self.games)


def CLParser():
    '''Parses the command line arguments and returns them.'''
    import argparse
    parser = argparse.ArgumentParser(description = "Let's play some Yeahtzee!", epilog = "And that, my friends, is how it's done.")
    parser.add_argument("-t", "--threads", type = int, default = 4, help="Maximum number of simultaneous threads")
    parser.add_argument("-g", "--games", type = int, default = 100, help="Number of games to be played")
    parser.add_argument("-e", "--engines", nargs = "*", default = [], help="Engines participating in the tournament. Options for an engine can be appended with dots.")
    arguments = parser.parse_args()
    
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
            ### Eventueel voorstellen om human player toe te voegen
            print >>sys.stderr, "Could not find engine module '%s'" % engine_fields[0]
            sys.exit(1)
    
    return arguments.threads, arguments.games, engines


global ENGINES
if __name__ == "__main__":
    threads, games, engines = CLParser()
    ENGINES = engines
    t = Tournament(engines, threads, games)
    t.play_tournament()
