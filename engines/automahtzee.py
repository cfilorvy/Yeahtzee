#!/usr/bin/env python
# encoding: utf-8
"""
automahtzee.py

Created by Bart Desmet on 2012-08-14.
Copyright (c) 2012 LT3. All rights reserved.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../")


from common import grid
from common import hand
from common import engine


class Engine(engine.Engine):

    def turn(self):
        verbose = True
        #process_id, verbose = False
        #'''Process_id is necessary, because an argument is needed for Pool.map'''
        h = hand.Hand()
        h.sort_by_value()
        if verbose: print "First roll:\t", h
        selection = h.make_inverse_selection([h.max_tally()[1][-1]])
        if verbose: print "Dice to reroll:\t", selection
        h.reroll(selection)
        if verbose: print "Second roll:\t", h
        selection = h.make_inverse_selection([h.max_tally()[1][-1]])
        if verbose: print "Dice to reroll:\t", selection
        h.reroll(selection)
        if verbose: print "Final roll:\t", h
        possible_scores = [self.grid.score(h, pos) for pos in self.grid.available_positions()]
        max_score = max(possible_scores)
        best_pos = self.grid.available_positions()[possible_scores.index(max_score)]
        if verbose: print "Best position:\t", best_pos
        self.grid.assign(h, best_pos)
        if verbose: print "Assigned hand to position '%s' for %d points.\n" % (grid.positions[best_pos][0], self.grid.return_score_or_zero(best_pos))
        return self.grid



if __name__ == "__main__":
    j = Engine()
    j.start_to_run_complete();
    