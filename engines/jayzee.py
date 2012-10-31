#!/usr/bin/env python
# encoding: utf-8
"""
jayzee.py

Created by Stef Bastiaansen on 2012-10-12.
Copyright (c) 2012 LT3. All rights reserved.
"""

import sys
sys.path.append("/Users/stef/Desktop/python/Yeahtzee/")
from common import grid
from common import hand

def main(process_id, verbose = False):
	g = grid.Grid()
	h = hand.Hand()
	h.sort_by_value()
	
	tallies = [5]
	
	if 1 in tallies:
		print "NOG fh"
	return g


if __name__ == '__main__':
    main(1)

