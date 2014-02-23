#!/usr/bin/env python
# encoding: utf-8
"""
Engine base class

Created by Stef Bastiaansen & Bart Desmet on 2012-10-31.
"""

import sys
from common import grid

import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.DEBUG)

class Engine(object):
    def __init__(self, name):
        self.name = name
    
    def start_to_run_complete(self):
        """Play a game from start to finish"""
        self.grid = grid.Grid()
        logging.debug("Starting complete game with engine %s" % self.name)
        previously_filled_positions = set(self.grid.filled_positions())
        while self.grid.available_positions():
            self.turn()
            # Check if the grid has been updated
            currently_filled_positions = set(self.grid.filled_positions())
            diff = currently_filled_positions - previously_filled_positions
            if len(diff) == 0:
                logging.error("Engine {0.name} is cheating: no position was filled.\nPreviously filled positions:\t{1}\nCurrently filled positions:\t{2}".format(self, previously_filled_positions, currently_filled_positions))
                sys.exit()
            elif len(diff) > 1:
                logging.error("Engine {0.name} is cheating: several position were changed.\nPreviously filled positions:\t{1}\nCurrently filled positions:\t{2}".format(self, previously_filled_positions, currently_filled_positions))
                sys.exit()
            previously_filled_positions = currently_filled_positions
        logging.debug("Finished complete game with engine %s" % self.name)
        return self.grid
    
    def start_to_run_turn(self):
        """Play just one turn in a game"""
        self.turn()
        return grid
    

