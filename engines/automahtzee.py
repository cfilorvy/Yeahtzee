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
        
        try: return {
            "always_yz": self.logic_always_yahtzee(h),
            }[self.logic]
        except KeyError:
            print "No logic defined"
            raise
    
    def logic_always_yahtzee(self, h):
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
    

if __name__ == "__main__":
    j = Engine("automahtzee")
    j.start_to_run_complete();
    