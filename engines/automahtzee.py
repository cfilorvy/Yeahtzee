#!/usr/bin/env python
# encoding: utf-8
"""
automahtzee.py

Created by Bart Desmet on 2012-08-14.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../")

from common import grid
from common import hand
from engines import engine

import ipdb
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.DEBUG)

class Engine(engine.Engine):
    def __init__(self, *args):
        args = list(args)
        super(Engine, self).__init__(args.pop(0))
        if args: self.logic = args.pop(0)
        else: self.logic = "always_yz"
        self.verbose = True
    
    def turn(self):
        #process_id, verbose = False
        #'''Process_id is necessary, because an argument is needed for Pool.map'''
        h = hand.Hand()
        h.sort_by_value()
        if self.verbose: print "Roll {0.rolls}:\t{0}".format(h)
        
        try:
            logic_function = {
                "always_yz":        self.logic_always_yahtzee,
                "yz_and_s":         self.logic_yahtzee_and_straights,
            }[self.logic]
            return logic_function(h)
        except KeyError:
            logging.error("No valid logic defined")
            raise
    
    def go_for_yahtzee(self, h):
        """Rerolls hand to maximize chances for a yahtzee"""
        logging.debug("Going for Yahtzee")
        while h.rolls < 3:
            selection = h.make_inverse_selection([h.max_tally()[1][-1]])
            if self.verbose: print "Dice to reroll:\t{0}".format(selection)
            h.reroll(selection)
            if self.verbose: print "Roll {0.rolls}:\t{0}".format(h)
        possible_scores = [self.grid.score(h, pos) for pos in self.grid.available_positions()]
        max_score = max(possible_scores)
        best_pos = self.grid.available_positions()[possible_scores.index(max_score)]
        if self.verbose: print "Best position:{0}".format(best_pos)
        self.grid.assign(h, best_pos)
        if self.verbose: print "Assigned hand to position '{0}' for {1} points.\n".format(grid.positions[best_pos][0], self.grid.get_score(best_pos))
        return self.grid
    
    def go_for_straight(self, h):
        """Rerolls hand to maximize chances for a straight"""
        logging.debug("Going for straight")
        pass # to be implemented, will raise cheating error now
        # Should start by checking if current hand is ls, then ss
        return self.grid
    
    def straight_likely(self, h):
        """Returns True if going for a straight is a good idea,
        given the current grid and hand."""
        # Check if any straight position (ls, ss) is still open
        if "s" in [p[1] for p in self.grid.available_positions()]:
            # Don't go for a straight if there is a 3 of a kind or better
            if h.max_tally()[0] <= 2:
                return True # Needs extra check for straight probability
        return False
    
    def logic_always_yahtzee(self, h):
        """Game logic that always goes for yahtzee"""
        return self.go_for_yahtzee(h)
    
    def logic_yahtzee_and_straights(self, h):
        """Game logic that goes for yahtzees and straights"""
        ipdb.set_trace()
        if self.straight_likely(h): return self.go_for_straight(h)
        else: self.go_for_yahtzee(h)
    

if __name__ == "__main__":
    j = Engine("automahtzee")
    j.start_to_run_complete();
    