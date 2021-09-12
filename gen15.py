#! /usr/bin/env python3
# -*- coding: utf-8 -*-


from math import *
import os

from random import shuffle

import random

import itertools
import operator

import more_itertools as mit


import base64
from sys import getsizeof


DISTRIBSIZE = 4
PACK = 3 + 1
#HANDSIZE = 3
HANDSIZE = 7

#maxcol = 3
#maxval = 3
maxcol = 7
maxval = 7
colval = maxcol * maxval



deck = [x for x in range(1,colval)] # idx zero is a joker to keep number aligned

shuffle(deck)



def get_ordered_deck(colval):  
    deck = [x for x in range(1,colval)]
    return deck 

decky = get_ordered_deck(colval)

print(f"decky = {decky}")


def get_crops_raw(fulllist, lencrop):

    crops_raw=list(itertools.combinations(deck, lencrop))


    return crops_raw



crops_raw = get_crops_raw(decky, HANDSIZE)
print(f"crops_raw = \n {crops_raw}")


def get_possible_sorted_hands(fulllist, crop):

    multiholes_sorted = []    

    for multihole in crop:
        multihole = list(multihole)
        multihole.sort()
        multiholes_sorted.append(multihole)

    multiholes_sorted.sort()
    print(f"multiholes_sorted  \n {multiholes_sorted}")
    return multiholes_sorted


hands = get_possible_sorted_hands(decky, crops_raw)
print(f"hands = \n {hands}")
print(f"len(hands) =  {len(hands)}")


        
def gruyere_decks(fulldeck,possible_crops):

    gruyere_decks = []

    for combo in possible_crops:
        new_gruyere =[card for card in fulldeck if not card in combo]
        gruyere_decks.append(new_gruyere)

    print(f"gruyere_decks \n {gruyere_decks}")
    print(f"len(gruyere_decks) =  {len(gruyere_decks)}")

    return gruyere_decks



gd = gruyere_decks(decky,hands)


def get_very_first_possible_tables(hands=hands, gd=gd):

    zip_hands_gd = zip(hands, gd)
    print(f"zip_hands_gd   {zip_hands_gd}")

    zipped_list = list(zip_hands_gd)

    print(f"\n zipped_list \n  {zipped_list}")

    print("\n -----------------------------------------")

    tabloids = []


    n_zip = 0
    for zipo in zipped_list:
        permut=list(itertools.permutations(zipo[1], 2))
        #print("\n   ", zipo,"    ",zipo[0],"    ",zipo[1])
        print("\n   ", zipo,"    >  ",permut)
        n_zip += 1


        for perm in permut:
            print(perm)
            print("zipo[0]  ", zipo[0])
            print("perm[0]  ", perm[0])
            print("perm[1]  ", perm[1])
            


            #table = perm[0].copy()  #'int' object has no attribute 'copy'
            table = list(perm)

            print("table", table)
            for zipy in zipo[0]:
                table.append(zipy)
            print("table", table)

            tabloids.append(table)


    print("n_zip   ", n_zip)
    print("len(permut)  ",len(permut))

    print("***")
    
    tabloids.sort()

    print(tabloids)
    print(len(tabloids))
    return tabloids

tabloids = get_very_first_possible_tables(hands, gd)



#def encode_tabloids(tabloids, players_list, judge):
def encode_tabloids(tabloids): # 4 players version , ia on player 0

    all_encodes = []

    print("inside  encode_tabloids  fn")
    print(f"tabloids \n {tabloids}   \n   len(tabloids)   {len(tabloids)}")


    for tab in tabloids:

        

        Apal_list = tab[0]
        Bpal_list = tab[1]
        Cpal_list = players_list[2].pal
        Dpal_list = players_list[3].pal

        #Cpal_list = None
        #Dpal_list = None


        all_players_pals = [Apal_list,Bpal_list,Cpal_list,Dpal_list]
        #all_players_pals = [Apal_list,Bpal_list]


        Ehand_list = tab[2:]

        print(f" Ehand_list =  {Ehand_list}")

        #Fcanvas_list = judge_dredd.canvas
        Fcanvas_list = [0] #red for very first table













        #--------

        charnumsA = []


        charnumsA.append('A' + str(Apal_list))
        Astr = ''.join(charnumsA)


      

        #--------    
        charnumsB = []


        charnumsB.append('B' + str(Bpal_list))


        
        Bstr = ''.join(charnumsB)
        

        #--------  

        charnumsC = []


        charnumsC.append('C' + str(Cpal_list))
        Cstr = ''.join(charnumsC)


      

        #--------    
        charnumsD = []


        charnumsD.append('D' + str(Dpal_list))


        
        Dstr = ''.join(charnumsD)  
        
                
        #--------

        charnumsE = []

        for card in Ehand_list: # player zero

            charnumsE.append('E' + str(card))


        Estr = ''.join(charnumsE)

        #--------        !!

        #charnumsF = []

        #for card in Fcanvas_list: # 

        #    charnumsF.append('F' + str(card))


        #Fstr = ''.join(charnumsF)

        #--------   !!

        charnumsF = []
        charnumsF.append('F' + str(Fcanvas_list[-1]))
        Fstr = ''.join(charnumsF)

        # !!!!!!!!


        state_hexa = Astr + Bstr + Cstr + Dstr + Estr + Fstr
        #state_hexa = Astr + Bstr + Estr + Fstr




        print(f"-->==>  >>>>     _Encoding state gives   {state_hexa}")


        #AJOUTER 'X' + index du current player pour donner referentiel d interpretation. Attention X depasse les lettres hexa, base 64 ?

        # https://stackoverflow.com/questions/43207978/python-converting-from-base64-to-binary

        binary_ascii =state_hexa.encode("ascii")

        print("binary_ascii = ",binary_ascii)

        all_encodes.append(binary_ascii)

    return all_encodes


possible_first_table = encode_tabloids(tabloids)

"""
for cod in all_encodes:

    print(cod,"    ",type(cod))


print(f" len(all_encodes)  {len(all_encodes)} ")

print(f"    getsizeof(all_encodes) = {getsizeof(all_encodes)}")

"""