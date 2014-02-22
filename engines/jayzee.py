#!/usr/bin/env python
# encoding: utf-8
"""
jayzee.py

Created by Stef Bastiaansen on 2012-10-12.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../")

chances_in_order = ["n1", "n2", "n3", "n4", "n5", "n6", "nt", "nb", "k3", "k4", "ch", "fh", "ss", "ls", "yz", "yb", "gt"]

from common import hand
from common import engine
from common import grid


class Engine(engine.Engine):


	def turn(self):

		h = hand.Hand()

		current_scores_for_positions = [self.grid.score(h, pos) for pos in self.grid.available_positions()]
		
		#if verbose:
		print current_scores_for_positions

			
		#if max(mogelijke_scores) < 20:
		#	h.reroll([0,1,2,3,4,5])
		#if max(mogelijke_scores) < 20:
		#	h.reroll([0,1,2,3,4,5])
		#mogelijke_scores = [self.grid.score(h, pos) for pos in self.grid.available_positions()]
		#print mogelijke_scores		
		


if __name__ == "__main__":
	j = Engine()
	j.start_to_run_complete();
	