#! /usr/bin/env python3
# -*- coding: utf-8 -*-


from math import *
import os

from random import shuffle
from termcolor import colored

import random

import itertools
import operator

import more_itertools as mit


#-------------------------------------------------------------- CST

PLAYERS_NB = 2

DISTRIBSIZE = 8 #(7 playable cards +1 for range in/exclusion)

MOD7dict = {0: "red", 6: "grey", 5: "yellow", 4: "green", 3: "blue", 2: "cyan", 1: "magenta"}


#-------------------------------------------------------------- TOOLKIT


def color_code(card: int):

	return card % 7

	
def color(card):

	mod7 = card % 7

	return MOD7dict[mod7]


def value(card):

	val = ceil(card/7)

	return val

# -------------------------------------------------------------- CLASS JUDGE

#canvas = []

class Judge():

	def __init__(self):

		self.canvas = []




	def get_canvas_code(self):

		# get color code , ie red is 0

		if not self.canvas == []:

			print(f" debug  canvas[-1]  {self.canvas[-1]}")

			canvas_code = color_code(self.canvas[-1])
		else:
			canvas_code = 0 # default at start




		return canvas_code


	def show_canvas(self):

		#card = canvas[-1]
		

		rule_color = MOD7dict[self.get_canvas_code()]

		print(f"   $$$$$$$$$$$$ CANVAS   {rule_color}             ")



	def inspection(self, id_player, players_list):

		teste_player_scores = players_list[id_player].get_player_scores()

		print(f"judge_dredd  is inspecting player {id_player}  and find  teste_player_scores {teste_player_scores}")




judge_dredd = Judge()

# -------------------------------------------------------------- CLASS PLAYER



class Player():

	

	def __init__(self, idx_player):

		self.idx_player = idx_player
		
		self.pal = []
		self.alive = True
		self.hand = []

	#------------------------------------------------------ RED

		

	@property
	def score_red(self): # SCORE_RED

		return max(self.pal)


	#------------------------------------------------------ ORANGE  /  GREY



	@property
	def dico_val(self):

		#dico_val = {1:0,2:0,3:0,4:0,5:0,6:0,7:0}

		tempo_list = []



		for card in self.pal:
			tempo_list.append(ceil(card/7))


		dico_val = dict()
		for i in range(1,8):

			dico_val.update({i:tempo_list.count(i)})


		return dico_val

	@property
	def score_orange(self):

		#print("dico_val ...",self.dico_val)

		dico_val_VALUES = self.dico_val.values()

		#print("dico_val_VALUES ==>>>",dico_val_VALUES)

		#bigger_key = max(dico_val_VALUES.items(), key=operator.itemgetter(1))[0]
		bigger_key = max(dico_val_VALUES)
		
		#print(f" score_orange=>   player {self.idx_player} has bigger_key {bigger_key} ")

		return bigger_key


	# -------------------------------------------------------- YELLOW -------

	@property
	def dico_col(self):

		#dico_col = {0:0, 1:0,2:0,3:0,4:0,5:0,6:0}  #{0 is "red", 6 is "grey", 5 is "yellow", 4 is "green", 3 is "blue", 2 is "cyan", 1 is "magenta"}

		tempo_list = []





		for card in self.pal:
			tempo_list.append(color_code(card))


		dico_col = dict()
		for i in range(0,7):

			dico_col.update({i:tempo_list.count(i)})


		return dico_col



	@property
	def score_yellow(self): # MAX SAME COLOR SURVIVE

		#print("++++++++++++dico_col ...",self.dico_col)

		dico_col_VALUES = self.dico_col.values()

		#print("dico_col_VALUES ==>>>",dico_col_VALUES)

		bigger_key = max(dico_col_VALUES)
		
		#print(f" score_yellow=>   player {self.idx_player} has bigger_key {bigger_key} ")

		return bigger_key


	#----------------------------------------------------- GREEN

	

	@property
	def score_green(self):

		#odd = {1,3,5,7}

		dico_val = self.dico_val

		for k, v in dico_val.copy().items():   # COPY because of RuntimeError: dictionary changed size during iteration
			if (k % 2) != 0:
				del dico_val[k]

		

		#print(f" dico_val  {dico_val}   after elagage")

		ScoreGreen = sum(dico_val.values())

		#print(f" player {self.idx_player} ScoreGreen  {ScoreGreen}   ")

		return ScoreGreen



	#----------------------------------------------------- BLUE

	

	@property
	def score_blue(self):

		diversity = 0

		list_qtt_per_color = self.dico_col.values() # [red,magenta,cyan...orange]

		#print(f" blue fn {list_qtt_per_color}")

		for qtt in list_qtt_per_color:
			if qtt>0:
				diversity +=1


		#print(f" player {self.idx_player} has  blue score {diversity}")

		return diversity

		#for k, v in dico_val.copy().items():   # COPY because of RuntimeError: dictionary changed size during iteration
		#	if (k % 2) != 0:


	#----------------------------------------------------- CYAN / INDIGO ////////////////////

	# https://stackoverflow.com/questions/2361945/detecting-consecutive-integers-in-a-list

	@property
	def score_indigo(self):

		vals_palette = [ceil(val/7) for val in self.pal]

		set_vals_palette = set(vals_palette)

		#sorted_vals_palette = sorted(vals_palette)
		sorted_vals_palette = sorted(set_vals_palette)

		#rivers = [list(group) for group in mit.consecutive_groups(self.pal)]
		rivers = [list(group) for group in mit.consecutive_groups(sorted_vals_palette)]

		longest_river = 0
		for river in rivers:
			if len(river)>longest_river:
				longest_river = len(river)

		#print(f"!  !  !  ! player {self.idx_player} has  rivers {rivers} ; his longest river has lenght {longest_river}      score_indigo / cyan ")


		return longest_river


	#----------------------------------------------------- MAGENTA / VIOLET


	@property
	def score_violet(self):

		dwarfs = [dwarf for dwarf in self.pal if dwarf <= 21]

		len_dwarfs = len(dwarfs)

		#print(f" ********player {self.idx_player} has  dwarfs {dwarfs}")

		return len_dwarfs

	# -------------- poubelle






		self.dico_val = {1:0,2:0,3:0,4:0,5:0,6:0,7:0} # joker = zero
		self.dico_col = {0:0, 1:0,2:0,3:0,4:0,5:0,6:0} # 0 red , 6 orange / grey , 5 yellow , 4 green , 3 blue , 2 indigo / cyan , 1 violet / magenta

		self.max_same_color = 0
		self.max_same_val = 0
		self.max_even = 0 # nb paires
		self.max_diversity = 0 # nb different colors
		self.flush_lenght = 0 # successive cards
		self.dwarf = 0 # number of 1,2,3 cards


	def get_player_scores(self):

		#print(" STTTAAATTTTT !!!")

		#print(f" player  {self.idx_player}   has score_red {self.score_red}  and dico_val {self.dico_val}")

		#self.score_orange

		#self.score_yellow

		#self.score_green

		#self.score_blue

		#self.score_indigo

		#self.score_violet

		#self.player_scores = list(self.score_red, self.score_violet,self.score_indigo,self.score_blue,self.score_green,self.score_yellow,self.score_orange)
		self.player_scores = [self.score_red, self.score_violet,self.score_indigo,self.score_blue,self.score_green,self.score_yellow,self.score_orange]

		return self.player_scores







	def __str__(self):

		return f" Player {self.idx_player}   has Palette {self.pal}    life status is {self.alive}   last hand was {self.hand}"


	def get_hand(self, deck):

		for distri in range(DISTRIBSIZE):
			newcard = deck.pop()
			self.hand.append(newcard)
			#print(f"\n player {self.idx_player}   has just taken new card {self.hand}")

		self.hand.sort() # S O R T

		self.fill_palette()

		#print(f"\n player {self.idx_player}   received hand {self.hand}   and has palette {self.pal}")



	def fill_palette(self):
		drop = self.hand.pop()
		self.pal.append(drop)
		#print(f"\n player {self.idx_player}   fill his palette card {drop} ; his full palette is {self.pal}   ; his hand is {self.hand}")

		self.pal.sort() # S O R T
		self.hand.sort() # S O R T


	def draw_one_card(self,deck):
		pass



	def fill_canvas(self):

		#global canvas

		drop_choice = random.choice(self.hand)



		


		print(f" drop_choice  {drop_choice}")

		judge_dredd.canvas.append(drop_choice)

		self.hand.remove(drop_choice)

		print(f" player {self.idx_player}   updated hand :   {self.hand}")

		print(f" updated canvas  {judge_dredd.canvas}")





	def sticker(self, card):

		val = value(card)
		col = color(card)

		#text = colored(val, col, attrs=['reverse', 'blink'])
		#text = colored(val, col)
		text = colored(val, col, attrs=['bold'])

		return text


	def debriefing(self):

		
		print(f"\n player {self.idx_player}    game : \n ")
		
		



		

		#for i in range(len(self.pal)):
		#	print(f"  __ player {self.idx_player}    palette :  -   {palette_to_show[i]}         {self.pal}")

		print(f"Palette   player {self.idx_player}")



		for card in self.pal:
			print(f"         +   {self.sticker(card)}              {value(card)}    {color(card)}                    card {card}")
		print("\n\n")



		print(f"Hand   player {self.idx_player}")




		for card in self.hand:

			#print(f"    -   {value(card)}    {color(card)} ")

			print(f" -   {self.sticker(card)}              {value(card)}    {color(card)}                       card {card}")


		#palette_to_show = [self.sticker(card)  for card in self.pal]

		print("\n ....... . . . ..  ...   ...   ....   ....   .....   ..............")









# -------------------------------------------------------------- INIT


Players = []


"""

def get_canvas_code():

	# get color code , ie red is 0

	if not canvas == []:

		print(f" debug  canvas[-1]  {canvas[-1]}")

		canvas_code = color_code(canvas[-1])
	else:
		canvas_code = 0 # default at start


	return canvas_code




def show_canvas():

	#card = canvas[-1]
	

	rule_color = MOD7dict[get_canvas_code()]

	print(f"    CANVAS   {rule_color}             ")


"""


deck = [x for x in range(0,50)] # idx zero is a joker to keep number aligned

#Players = [Player() for player in range(PLAYERS_NB)]




for i in range(PLAYERS_NB):
	newplayer = Player(i)
	Players.append(newplayer)



#-------------------------------------------------------------- SET UP




#---------------------------------------------------------------- GUI

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


clear_screen()

print("__ ATTENTION JOKER 0 __\n\n")



#------------- verif debug starting

#print(deck)
shuffle(deck)

#print(deck)




#for player in Players:
#	print(player)





#---------- distri

for player in Players:
	player.get_hand(deck)

	player.debriefing()
	print("..............................................")


print("\n xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx  Fight  !!!!!")


for j in range(5):
	print(" \n \n ________________________________________________________________________ TOUR  ",j)
	for player in Players:
		player.fill_palette()
		player.debriefing()

	

judge_dredd.show_canvas()

Players[0].fill_canvas()

print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
judge_dredd.show_canvas()
Players[1].fill_canvas()
print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")

judge_dredd.show_canvas()


# https://ozzmaker.com/add-colour-to-text-in-python/


#----------------- ANAL
"""
def anal_red():

	maxitem = max(itertools.chain(Players[0].pal, Players[1].pal))

	print(f" maxitem  {maxitem}")


	for player in Players:

		if maxitem in player.pal:

			print(f" maxitem found in player  {player.idx_player}")





def table_analyzer():

	anal_red()

	

	for player in Players:
		player.anal_stats()

"""

#--------- PRATIK

#table_analyzer()

id_player = 0

judge_dredd.inspection(id_player, Players)