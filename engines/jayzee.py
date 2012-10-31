#!/usr/bin/env python
# encoding: utf-8
"""
jayzee.py

Created by Stef Bastiaansen on 2012-10-12.
Copyright (c) 2012 LT3. All rights reserved.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../")
from common import grid
from common import hand

def main(process_id, verbose = False):

	print "fons" 

	g = grid.Grid()
	h = hand.Hand()
	h.sort_by_value()
	
	
	
	


if __name__ == '__main__':
    main(1)

