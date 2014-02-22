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

import copy
from functools import partial
from multiprocessing import Pool

import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.DEBUG)

class Tournament(object):
    """Yahtzee tournament in which one or more engines can compete over the course of multiple games"""
    def __init__(self, engines, threads, games):
        self.engines = engines
        # Engines should have unique names
        assert len(self.engines) == len(list(set(e.name for e in self.engines)))
        self.threads = threads
        self.games = games
        self.stored_games = {e.name: [] for e in engines} # Stores the games of each engine
    
    def play_game(self, engine):
        """Play a single game and return a deep copy of the grid"""
        return copy.deepcopy(engine.start_to_run_complete())
    
    def __call__():
        Tournament.play_tournament()
    
    def play_tournament(self):
        # Deze lijst wordt nogal groot na verloop van tijd, omdat er volledige
        # grids in worden opgeslagen. Met 10000 runs was dat 50MB, dus met
        # 1 miljoen runs (voor 1 engine) is dat al 5GB.
        # Het opslaan van volledige grids is enkel nuttig voor het testen van
        # engines, kwestie van statistische analyses te kunnen doen op de
        # performance. Bij het effectieve battlen moeten we enkel de grand
        # totals onthouden.
        if self.threads == 1: # Running sequentially
            self.gamecounter = 0
            for game in range(self.games):
                self.gamecounter += 1
                if self.gamecounter % 1000 == 0:
                    logging.info("{0.gamecounter} of {0.games} games played".format(self))
                for e in self.engines:
                    logging.debug("Playing game {0.gamecounter} with engine {1.name}".format(self, e))
                    self.stored_games[e.name].append(self.play_game(e))
        elif 1 < self.threads < 33: # Multiprocessing pwnz0r!!
            for engine in self.engines:
                pool = Pool(self.threads)
                play_game_with_engine = partial(self.play_game, engine=engine) 
                self.stored_games[engine.name] = pool.map(play_game_with_engine, range(self.games))
        else:
            logging.error("Too many processes: {0.threads}".format(self))
            sys.exit(1)
        
        print "Minimum, average and maximum grand total:", self.get_minimum("gt"), self.get_average("gt"), self.get_maximum("gt")
        print "Yahtzee hit percentage:", self.get_hit_ratio("yz")
        print "Yahtzee bonus hit percentage:", self.get_hit_ratio("yb")
    
    def get_average(self, position):
        """Returns the average score for a position, over all grids,
        for each engine"""
        def average(pos, name):
            return sum(g.get_score(pos) for g in self.stored_games[name])/float(len(self.stored_games[name]))
        return {e.name: average(position, e.name) for e in self.engines}
    
    def get_minimum(self, position):
        """Returns the minimum score for a position, over all grids,
        for each engine"""
        def minimum(pos, name):
            return min(g.get_score(pos) for g in self.stored_games[name])
        return {e.name: minimum(position, e.name) for e in self.engines}
    
    def get_maximum(self, position):
        """Returns the maximum score for a position, over all grids,
        for each engine"""
        def maximum(pos, name):
            return max(g.get_score(pos) for g in self.stored_games[name])
        return {e.name: maximum(position, e.name) for e in self.engines}
    
    def get_hit_ratio(self, position):
        """Returns the average number of non-zero scores for a position,
        over all grids, for each engine"""
        def hit_ratio(pos, name):
            # for g in self.stored_games[name]: print repr(g)
            return sum(1 for g in self.stored_games[name] if g.get_score(pos))/float(len(self.stored_games[name]))
        return {e.name: hit_ratio(position, e.name) for e in self.engines}
    

def import_engine(arg):
    """Translate a command line engine argument of the form
    engine_name[.arg1][.argn] into an imported Engine object"""
    engine_name = arg.split(".")[0]
    engine_args = arg.split(".")[1:] # Options are added with dot notation
    try:
        engine_module = __import__("engines.%s" % engine_name, fromlist=["engines"]) # fromlist defines the package from which to import
        e = engine_module.Engine(engine_name, *engine_args) # Instantiate an Engine from the desired module, with the desired arguments. The length of engine_args should match the number of positional arguments in the engine constructor.
    except ImportError:
        logging.error("Could not find engine module '{0}'".format(engine_name))
        raise
    return e

def CLParser():
    '''Parses the command line arguments and returns them.'''
    import argparse
    parser = argparse.ArgumentParser(description = "Let's play some Yeahtzee!", epilog = "And that, my friends, is how it's done.")
    parser.add_argument("-t", "--threads", type = int, default = 1, help="Maximum number of simultaneous threads")
    parser.add_argument("-g", "--games", type = int, default = 100, help="Number of games to be played")
    parser.add_argument("-e", "--engines", nargs = "*", default = [], help="Engines participating in the tournament. Options for an engine can be appended with dots.")
    arguments = parser.parse_args()
    
    try: assert arguments.engines
    except AssertionError:
        logging.error("Specify engines using the -e option")
        raise
    engines = [import_engine(e) for e in arguments.engines]
    
    return arguments.threads, arguments.games, engines

if __name__ == "__main__":
    threads, games, engines = CLParser()
    global ENGINES
    ENGINES = engines
    t = Tournament(engines, threads, games)
    t.play_tournament()
