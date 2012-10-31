#!/usr/bin/env python
# encoding: utf-8
"""
jayzee.py

Created by Stef Bastiaansen on 2012-10-12.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../")

from common import hand
from common import engine
from common import grid
from common import engine


class Jayzee(engine.Engine):

	def __init__(self):
		#bereken de kansen
		pass

	def turn(self):
		h = hand.Hand()
		mogelijke_scores = [self.grid.score(h, pos) for pos in self.grid.available_positions()]
		print mogelijke_scores
		if max(mogelijke_scores) < 20:
			h.reroll([0,1,2,3,4,5])
		if max(mogelijke_scores) < 20:
			h.reroll([0,1,2,3,4,5])
		mogelijke_scores = [self.grid.score(h, pos) for pos in self.grid.available_positions()]
		print mogelijke_scores		

		

if __name__ == "__main__":
	j = Jayzee()
	j.startToRun()
	j.turn()