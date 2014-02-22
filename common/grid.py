#!/usr/bin/env python
# encoding: utf-8
"""
grid.py

Created by Bart Desmet on 2012-08-14.
Copyright (c) 2012 LT3. All rights reserved.
"""

import sys
from common import hand as h

positions_in_order = ["n1", "n2", "n3", "n4", "n5", "n6", "nt", "nb", "k3", "k4", "ch", "fh", "ss", "ls", "yz", "yb", "gt"]
unassignable_positions = ["nt", "nb", "gt"]
assignable_positions = [x for x in positions_in_order if x not in unassignable_positions]


positions = {
    "n1": ("ones", "enen"),
    "n2": ("twos", "tweeën"),
    "n3": ("threes", "drieën"),
    "n4": ("fours", "vieren"),
    "n5": ("fives", "vijven"),
    "n6": ("sixes", "zessen"),
    "nt": ("number total", "nummertotaal"),
    "nb": ("number bonus", "de bonus"),
    "k3": ("three of a kind", "three of a shnackies"),
    "k4": ("four of a kind", "carré"),
    "ch": ("chance", "chance"),
    "fh": ("full house", "full house"),
    "ss": ("small straight", "kleine straat"),
    "ls": ("large straight", "grote straat"),
    "yz": ("yahtzee", "yahtzee"),
    "yb": ("yahtzee bonus", "yahtzee bonus"),
    "gt": ("grand total", "totaal"),
    }


fixed_scores = {
    "fh": 25,
    "ss": 30,
    "ls": 40,
    "yz": 50,
    "yb": 100,
    }

class FilledInError():
    pass


class InvalidPositionError():
    pass


class Grid(object):
    """Yahtzee score grid"""
    def __init__(self):
        self.grid = {x: (None, "---") for x in positions}
        self.update_totals()
    
    
    def update_totals(self):
        self.grid["nt"] = (None, self.number_total()) # No hand for this position
        self.grid["nb"] = (None, {True: 30, False: 0}[self.grid["nt"] >= 63])
        self.grid["gt"] = (None, self.grand_total())
        
        # Check if YB position should become available
        if self.grid["yb"][0] is None:              # YB has not been attained
            # (Grid for YB should not be reset if it has already been attained)
            if self.grid["yz"][1] not in ("---", 0):# YZ has been attained
                self.grid["yb"] = (None, "---")     # YB available for scoring
            else:                                   # No YZ attained yet
                self.grid["yb"] = (None, 0)         # YB unavailable
    
    def available_positions(self):
        """Returns all the grid positions that are currently available
        for scoring.
        - YB is only available after YZ has been scored other than 0 or ---
        - NB, NT and GT are never available for scoring
        
        If 13 positions have been scored in the grid,
        no further positions can be filled"""
        if len([x for x in self.grid.values() if x[0] != None]) < 13:
            return [x for x in assignable_positions if self.grid[x][1] == "---"]
        else: return []
    
    
    def assign(self, hand, position):
        """Assigns a tuple to a position in the grid, of the form
        (hand, score of this hand for this position)"""
        assert isinstance(hand, h.Hand)
        # print "POSITION:", position
        # print self
        try: assert self.grid[position][1] == "---"
        except AssertionError:
            raise FilledInError
        self.grid[position] = (hand, self.score(hand, position))
        self.update_totals()
    
    
    def score(self, hand, position):
        """This function checks how many points you would get if the hand would
        be filled in at the given position."""
        
        try: assert self.grid[position][1] == "---"
        except AssertionError:
            print self
            print position
            raise FilledInError
        except KeyError:
            print "\nCheck your code. This is not a valid position:", position, "\n"
            raise
        
        if position.startswith("n"): # Return sum of relevant number
            n = int(position[1])
            return sum(d for d in hand.dice if d == n)
        
        elif position in ["k3", "k4", "ch"]: # Return total sum
            if position == "k3" and hand.max_tally()[0] < 3:
                return 0 # The is not a three of a kind
            elif position == "k4" and hand.max_tally()[0] < 4:
                return 0 # The is not a four of a kind
            return sum(hand.dice)
        
        elif position in ["fh", "ss", "ls", "yz", "yb"]: # Return fixed score
            if position == "fh":
                tallies = hand.get_dicedict().values()
                if 1 in tallies:
                    return 0 # This is not a full house
            
            elif position in ["ss", "ls"]:
                ds = "".join(str(x) for x in hand.sort_by_value())
                if position == ["ss"]:
                    if "1234" not in ds and "2345" not in ds and "3456" not in ds:
                        return 0
                else:
                    if "12345" not in ds and "23456" not in ds:
                        return 0
            
            else:
                if hand.max_tally()[0] < 5:
                    return 0 # This is not a yahtzee
                if position == "yb" and self.grid["yz"] == "---":
                    return 0 # YB only scores points if there already is a YZ
            
            return fixed_scores[position]
        
        else:
            raise InvalidPositionError
    
    
    def get_score(self, pos):
        if self.grid[pos][1] == "---": return 0
        else: return self.grid[pos][1]
    
    def number_total(self):
        """Sums all scores of the currently filled number positions"""
        return sum(self.grid[pos][1] for pos in ["n1", "n2", "n3", "n4", "n5", "n6"] if self.grid[pos][0])
        
    
    
    def grand_total(self):
        """Sums all scores of the currently filled assignable positions
        plus the number bonus"""
        return sum(self.grid[pos][1] for pos in assignable_positions if self.grid[pos][0]) + self.grid["nb"][1]
    
    
    def __str__(self):
        return "YEAHTZEE SCORE GRID\n" + "\n".join("%-15s: %3d" % (positions[pos][0], self.grid[pos][1]) for pos in positions_in_order) + "\n"
    



if __name__ == '__main__':
    main()

