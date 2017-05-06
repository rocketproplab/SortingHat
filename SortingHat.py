#!/usr/bin/env python
import re
import hashlib
import random
import subprocess as sp
from common.ascii_art import AsciiImage, AsciiText
import time
import sys
import string
import argparse
import pandas as pd
import numpy as np
import os

def parsey():
    parser = argparse.ArgumentParser(description='Sorting Hat sorts, coders code.')
    parser.add_argument('-train', dest='train', metavar='N', type=str, nargs=1,
                        help='File used to train the sorting hat each year.')
    parser.add_argument('-debug', dest='debug', action='store_true',
                        help='Set debug state true')
    args = parser.parse_args()
    return args


class sortingHat():
    '''This is the Sorting Hat.
    The Sorting Hat uses a "trained" pseudo-random number generator
    seeded with the users name to determine the house placement for the user.
    The Hat needs to be trained with a new set of names each time it is run.'''
    def __init__(self):
        self.debug = False
        self.training = False
        self.set_Constants()
        self.get_flags()  # sets training state and debug state
        if not self.training:
            self.isPM = False
            self.quoteSpecified = False
            self.get_name()
            self.check_name()
            self.sort()
            self.show_result()
        elif self.training:
            self.train()

    def get_flags(self):
        flags = parsey()
        if flags.train is not None:
            self.trainingFile = flags.train[0]  # only take first entry
            self.training = True
            print('Training flag detected; Entering Training State')
        else:
            self.training = False
        if flags.debug is not False:
            self.debug = True
            print('Debug State: True')

    def train(self):
        filePath = os.path.join(os.getcwd(), self.trainingFile)
        print('\nFile Path:', filePath)
        df = pd.read_csv(filePath, header=0)
        names = df[df.columns[0]]
        numMembers = np.ones(4)
        num = int(ceil(len(names)/4+.5))  # integer division
        numMembers = numMembers*num
        print('Total number of members:', len(names))
        print('Total number of members:', len(names)//4)
        print('Number of members in each house (before remainder)', num)
        print('Remainder:', len(names) % 4)
        for i in range(0, len(names) % 4):  # randomly select a house to award the remainder members to
            j = random.randrange(0, 4)
            numMembers[j] = numMembers[j] + 1
        print('\nHere are the resulting house member counts:\n')
        print(self.houses)
        print(numMembers)

        numbersDist = []  # empty array to hold random numbers generated below
        for i in range(0, len(names)):
            numbers.append(random.random())

    def set_Constants(self):
        self.houses = ['Slytherin', 'Gryffindor', 'Hufflepuff', 'Ravenclaw']
        self.specialNames = {
            'harry potter': 'Gryffindor',
            'hermione granger': 'Gryffindor',
            'ron weasley': 'Gryffindor',
            'draco malfoy': 'Slytherin',
            'lord voldemort': 'Slytherin',
            'albus dumbledore': 'Gryffindor',
            'cameron flannery': 'Gryffindor',
            'michael phalen': 'Gryffindor',
            'alex lim': 'Hufflepuff',
            'parker brown': 'Ravenclaw',
            'brandon nyugen': 'Slytherin',
        }
        self.nameSpecifiedQuotes = {
            'harry potter': 0,
            'ron weasley': 1,
        }
        self.quotes = ['Hmm, difficult. VERY difficult. Plenty of courage, I see. Not a bad mind, either. There\'s talent, oh yes. And a thirst to prove yourself. But where to put you?',
                       'Ah! I know just what to do with you...',
                       'I\'ll have alook inside your mind and tell where you belong!',
                       'Curious, very curious...']

    def get_name(self):
        while True:
            if self.debug:
                break
            self.rawName = input('Enter your first and last name (ex: \'Nikola Tesla\'): ')
            if self.isEmpty(self.rawName):
                print('Error: Please enter your name.')
                continue
            else:
                break

        self.rawName = self.rawName.lower()

    def sort(self):
        if not(self.isPM):
            m=re.sub("([a-zA-Z])([a-zA-Z]+?[^a-zA-Z]+?)([a-zA-Z]+)[^a-zA-Z]+?$", r"\1\3", self.rawName)
            m=re.sub("[^a-zA-Z]","",m)
            hasher = hashlib.sha256()
            hasher.update(m.encode('utf-8'))
            random.seed(hasher.hexdigest(),version=2)
            for j in range(0,4):
                hasher.update(repr(random.random()).encode('utf-8'))
            self.houseChoice = int(hasher.hexdigest(), 16) % 4
            self.sortedHouse = self.houses[self.houseChoice]
        if not(self.debug):
            time.sleep(0.5)
            if self.quoteSpecified:
                self.get_quote(self.nameSpecifiedQuotes[self.rawName])
            else:
                self.get_quote()
            time.sleep(1.5)

    def show_result(self):
        houseText = AsciiText(self.sortedHouse.upper()+'!')
        houseText.display_text()
        print('\n')

    def print_crest(self):
        """print house crest *** NOT CURRENTLY USED*** """
        # prints ascii art of rocket stored in /resources/openrocketengine
        path = os.path.dirname(__file__)
        fname = os.path.join(path, 'assets', self.sortedHouse+'.jpg')

        logo_image = AsciiImage(fname)
        logo_image.display_image()

    def check_name(self):
        """check_name checks to see if the entered name is a principal member.
        If yes, house is predetermined with dictionary"""

        try:
            self.sortedHouse = self.specialNames[self.rawName]
            self.isPM = True
        except KeyError:
            self.isPM = False  # bool: is principal member of club
        try:
            self.nameSpecifiedQuotes[self.rawName]
            self.quoteSpecified = True
        except KeyError:
            self.quoteSpecified = False  # bool: is principal member of club

    def get_quote(self, *arg):
        if arg:
            i = arg[0]
        else:
            i = random.randrange(0, len(self.quotes), 1)
        self.delay_print(i)

    def delay_print(self, i):
        delayTime = 0.05
        for c in self.quotes[i]:
            if self.is_punct_char(c):
                delayTime = 0.15
            else:
                delayTime = 0.05
            sys.stdout.write('%s' % c)
            sys.stdout.flush()
            time.sleep(delayTime)

    def is_punct_char(self, c):
        '''check if char is punctuation char'''
        if c in string.punctuation:
            return 1
        else:
            return 0

    def isEmpty(self, text):
        if text:
            return False
        else:
            return True


if __name__ == '__main__':
    try:
        sp.call('clear')
    except OSError:
        sp.call('cls', shell=True)

    try:
        RPLsorting = sortingHat()
    except KeyboardInterrupt:
        print('\nKeyboardInterrupt: Exiting')
