# -*- coding: utf-8 -*-
"""
Created on Tue Oct 26 21:06:57 2021

@author: k4toh
"""

import random
import numpy as np
import pickle
import bjgame as bj

suit = ["SPADE", "HEART", "DIAMD", "CLOVE"]
number = ['a', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
deck = []
deltcard = []


def CardSum(cards): #引数はTrumpCard class 返り値はint
    buffer = []

    i = 0
    for i in range(len(cards)):
        buffer.append(cards[i].number)
    buffer.sort()
    
    Csum = 0
    for j in buffer:
        if (j == "J" or j == "Q" or j == "K"):
            #print("kjq")
            Csum = 10 + Csum
        elif j == "a":
            #print("ace")
            if Csum <= 10 :
                #print("a = 11")
                Csum = 11 + Csum
            else:
                #print("a = 1")
                Csum = 1 + Csum
        else:
            #print("suuji")
            Csum = int(j) + Csum 
    
    return Csum 

class TrumpCard:
    def __init__(self, suit, number):
        self.suit = suit
        self.number = number
    
for i in suit:
    for j in number:
        b = TrumpCard(i, j)
        deck.append(b)

npdeck = np.array(deck)

sdeck = np.random.shuffle(npdeck)
adeck = random.shuffle(deck)

for k in range(2):
    deltcard.append(deck.pop())
    pass

sendfile = pickle.dumps(deltcard)

