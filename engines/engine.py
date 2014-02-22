#!/usr/bin/env python
# encoding: utf-8
"""
Engine base class

Created by Stef Bastiaansen & Bart Desmet on 2012-10-31.
"""

from common import grid

import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.DEBUG)

class Engine(object):
    def __init__(self, name):
        self.name = name
        self.grid = grid.Grid()
    
    def start_to_run_complete(self):
        """Play a game from start to finish"""
        logging.debug("Starting complete game with engine %s" % self.name)
        while self.grid.available_positions():
            self.turn()
        logging.debug("Finished complete game with engine %s" % self.name)
        return self.grid
    
    def start_to_run_turn(self):
        """Play just one turn in a game"""
        self.turn()
        return grid
    

