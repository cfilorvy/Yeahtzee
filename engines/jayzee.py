#!/usr/bin/env python
# encoding: utf-8
"""
jayzee.py

Created by Stef Bastiaansen on 2012-10-12.
"""

import sys
import os
import sqlite3
import logging

importance_in_order = ["n1", "n2", "n3", "n4", "n5", "n6", "nt", "nb", "k3", "k4", "ch", "fh", "ss", "ls", "yz", "yb",
                       "gt"]

from common import hand, grid
from engines import engine


class Engine(engine.Engine):
    importance = None;

    def __init__(self, name):
        super(Engine, self).__init__(name)
        self.get_importances()

    def get_importances(self):

        con = None

        try:
            con = sqlite3.connect('data/jayzee.db')

            con.row_factory = sqlite3.Row

            cur = con.cursor()
            cur.execute('SELECT * FROM importance ORDER BY average_score DESC LIMIT 1')

            importance = cur.fetchone()

            print "Hoogste gemiddelde %d" % (importance["average_score"])

        except sqlite3.Error, e:

            print "Error %s:" % e.args[0]
            sys.exit(1)

        finally:

            if con:
                con.close()

    def turn(self):

        h = hand.Hand()

        # logging.info("First troll {0}".format(h))

        current_scores_for_positions = [self.grid.score(h, pos) for pos in self.grid.available_positions()]

        h.reroll([1, 1, 1, 1, 1])
        # logging.info("Second troll {0}".format(h))

        h.reroll([1, 2, 3, 4, 5])
        # logging.info("Third troll {0}".format(h))

        min_score = min(current_scores_for_positions)

        worst_pos = self.grid.available_positions()[current_scores_for_positions.index(min_score)]

        self.grid.assign(h, worst_pos)

        # logging.info("Assigned hand to position {0} of {1} games played".format(grid.positions[worst_pos][0], self.grid.get_score(worst_pos)))

        return self.grid

    # if max(mogelijke_scores) < 20:
    #	h.reroll([0,1,2,3,4,5])
    # if max(mogelijke_scores) < 20:
    #	h.reroll([0,1,2,3,4,5])
    # mogelijke_scores = [self.grid.score(h, pos) for pos in self.grid.available_positions()]
    # print mogelijke_scores


'''




	Function bepaal_importance_and_probability

			For each row in grid(1-13) where points == '---'
				calculateImportance
					1-6 + chance
						-> Bereken currrentValueByMax (0-1) voor elke row
						-> is de bonus al gehaald?
						-> hoeveel punten zijn er nog te halen met 1-6, wat is het percentage daarvan, van die rij
						- des te hoger het aantal ogen, des te hoger de standaard importance
					7-13
						-> des te hoger des te beter

			For each row in grid(1-13) where points == '---'
				calculateProbabilityInDeVolgendeWorp
					1-6
						-> of de benodigde punten gehaald zullen worden
					7-13
						-> of dit effectief kan gehaald worden
					chance
						-> de nieuwe waarde moet hoger liggen dan de huidige




	Na First roll
		
		bepaal_importance_and_probability()
		
		Make descision
			Kies de rij waar
				-> de importance x probabilityInDeVolgendeWorp het grootste is

			Als de probabilityInDeVolgendeWorp == 1 (en er dus geen dobbelstenen meer gegooie moeten worden)
				-> assign Die Hand
			Else
				- kies de dobbelstenen die gerold moeten worden om de gekozen rij te optimaliseren
				Second roll


	Na second roll


		bepaal_importance_and_probability()
		
		Make descision
			Kies de rij waar
				-> de importance x probabilityInDeVolgendeWorp het grootste is

			Als de probabilityInDeVolgendeWorp == 1 (en er dus geen dobbelstenen meer gegooie moeten worden)
				-> assign Die Hand
			Else
				- kies de dobbelstenen die gerold moeten worden om de gekozen rij te optimaliseren
				Third roll
		
	Na second roll

		bepaal_importance_and_probability()
		
		Bekijk voor elke vrije rij
			- hoeveel punten er gescoord worden met de hand
			- Overloop de rijen per importance
				- Als de rij de gewenste currrentValueByMax overschrijdt, assign de hand

			- Wordt er nergens een rij ingevuld, dan wordt de score ingevuld bij de volgens importance laagste rij

			
		

'''



# if __name__ == "__main__":
#	j = Engine("jayzee")
#	j.start_to_run_complete();
