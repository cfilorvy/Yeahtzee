#!/usr/bin/env python
# encoding: utf-8
"""
Engine base class

Created by Stef Bastiaansen & Bart Desmet on 2012-10-31.
"""

from common import grid

class Engine(object):
	
	def __init__(self):
		self.grid = grid.Grid()


	def start_to_run_complete(self):
		while self.grid.available_positions():
			self.turn();

		print "Grand total: %d" % (self.grid.grand_total())

		return self.grid


	def start_to_run_turn(self):
		self.turn();	
		return grid;
		





