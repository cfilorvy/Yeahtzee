#!/usr/bin/env python
# encoding: utf-8
"""
hand.py

Created by Bart Desmet on 2012-08-14.
Copyright (c) 2012 LT3. All rights reserved.
"""

import random

random.seed()


class Hand(object):
    """A hand of 5 dice"""

    def __init__(self):
        self.rolls = 1
        self.dice = [random.choice([1, 2, 3, 4, 5, 6]) for d in range(5)]

    def max_tally(self):
        """Returns an integer from 1 to 5, indicating the tally
        of the most frequent dice in the hand. Also returns a sorted list
        of the value(s) that occur that often."""

        dd = self.get_dicedict()
        max_tally = max(dd.values())
        return max_tally, sorted([v for v in dd if dd[v] == max_tally])

    def get_dicedict(self):
        dicedict = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0}
        for d in self.dice:
            dicedict[d] += 1
        return dicedict

    def sort_by_value(self):
        self.dice.sort()
        return self.dice

    def sort_by_tally(self):
        dd = self.get_dicedict()

    def make_inverse_selection(self, values):
        selection = []
        for index in range(5):
            if self.dice[index] in values:
                selection.append(0)
            else:
                selection.append(1)
        return selection

    def reroll(self, which):
        assert self.rolls < 3
        for index in range(5):
            if which[index]:
                self.dice[index] = random.choice([1, 2, 3, 4, 5, 6])
        self.rolls += 1

    def __str__(self):
        # return "Hand: %s" % " ".join(str(x) for x in self.dice)
        return " ".join(str(x) for x in self.dice)


def main():
    pass


if __name__ == '__main__':
    main()
