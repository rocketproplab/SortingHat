#!/usr/bin/env python
import random
import subprocess as sp
import os
from common.ascii_art import AsciiImage

class sortingHat():
    def __init__(self):
        self.isPM = False
        self.houses = ['Slytherin', 'Gryffindor', 'Hufflepuff', 'Ravenclaw']
        self.get_name()
        if not(self.isPM):
            self.sort()
            self.show_result()

    def get_name(self):
        self.rawName = input('Enter your first and last name: ')
        self.check_name()
        self.asciiName = float(''.join(str(ord(c)) for c in self.rawName))

    def sort(self):
        random.seed(self.asciiName)
        self.houseChoice = random.randrange(0, 4, 1)
        self.sortedHouse = self.houses[self.houseChoice]

    def show_result(self):
        print(self.sortedHouse+'!')

    def print_crest(self):
        """print house crest *** NOT CURRENTLY USED*** """
        # prints ascii art of rocket stored in /resources/openrocketengine
        path = os.path.dirname(__file__)
        fname = os.path.join(path, 'assets', self.sortedHouse+'.jpg')

        logo_image = AsciiImage(fname)
        logo_image.display_image()

    def check_name(self):
        """check_name checks to see if the entered name is a principal member.
        If yes, house is predetermined with dictionary also defined in this
        method"""
        self.principalMembers = {
            'Cameron Flannery': 'Ravenclaw',
            'Michael Phalen': 'Gryffindor',
            'Alex Lim': 'Hufflepuff',
            'Parker Brown': 'Ravenclaw',
            'Brandon Nyugen': 'Ravenclaw',
        }

        try:
            self.sortedHouse = self.principalMembers[self.rawName]
            self.show_result()
            self.isPM = True
        except KeyError:
            self.isPM = False  # bool: is principal member of club


if __name__ == '__main__':
    try:
        sp.call('clear')
    except OSError:
        sp.call('cls', shell=True)

    RPLsorting = sortingHat()
