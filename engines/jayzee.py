#!/usr/bin/env python
# encoding: utf-8
"""
jayzee.py

Created by Stef Bastiaansen on 2012-10-12.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../")

importance_in_order = ["n1", "n2", "n3", "n4", "n5", "n6", "nt", "nb", "k3", "k4", "ch", "fh", "ss", "ls", "yz", "yb", "gt"]

from common import hand
from common import grid
from engines import engine

class Engine(engine.Engine):


	def turn(self):

		h = hand.Hand()

		current_scores_for_positions = [self.grid.score(h, pos) for pos in self.grid.available_positions()]
		
		#reroll 1
  		h.reroll([1,2,3,4,5]);
		print "First roll:\t", h

		#reroll 2
		h.reroll([1,2,3,4,5]);
		print "<Second></Second> roll:\t", h

		min_score = min(current_scores_for_positions)

 		worst_pos = self.grid.available_positions()[current_scores_for_positions.index(min_score)]
			
		self.grid.assign(h, worst_pos)

		print "Assigned hand to position '%s' for %d points.\n" % (grid.positions[worst_pos][0], self.grid.return_score_or_zero(worst_pos))

		return self.grid

		#if max(mogelijke_scores) < 20:
		#	h.reroll([0,1,2,3,4,5])
		#if max(mogelijke_scores) < 20:
		#	h.reroll([0,1,2,3,4,5])
		#mogelijke_scores = [self.grid.score(h, pos) for pos in self.grid.available_positions()]
		#print mogelijke_scores	

		


if __name__ == "__main__":
	j = Engine("jayzee")
	j.start_to_run_complete();
	