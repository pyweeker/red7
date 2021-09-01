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

#PLAYERS_NB = 2
PLAYERS_NB = 4


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

		#self.canvas = []
		self.canvas = [0] # ATTENTION ZERO, Joker ???

		self.tour = 0
		self.move = 0


		self.hot_player = 0  # last player who has played
		self.hot_action = 0  # last action of the last player who has played



	@property
	def last_canvas_card(self):
		return self.canvas[-1]


	@property
	def last_canvas_mod7(self):
		return (self.canvas[-1]%7)


	@property
	def last_canvas_color(self):
		return (MOD7dict[self.last_canvas_mod7])



	




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



	def inspect_hot_player(self, players_list):

		id_player = self.hot_player

		teste_player_scores = players_list[id_player].get_player_scores()

		print(" /*-+ /*-+ /*-+ /*-+  /*-+ /*-+ /*-+ /*-+  /*-+ /*-+ /*-+ /*-+  /*-+ /*-+ /*-+ /*-+")

		

		i=0
		for player in players_list:
			i_scores = player.get_player_scores()

			print(f"\n player  ",i,"  has scores  ",i_scores)
			i += 1

		


		print(f"\n                                                           judge_dredd  is inspecting player {id_player} on rule {self.get_canvas_code()}")

	def reset_judge_scores(self):

		
		self.judge_scores = [0,0,0,0,0,0,0]

	def get_judge_scores(self, players_list):

		self.reset_judge_scores()

		


		for player in players_list:
			for i in range(len(player.player_scores)):
			

				if self.judge_scores[i] < player.player_scores[i]:

					self.judge_scores[i] = player.player_scores[i]

		print("---------------------------------------------------------------------------------------------------")


		print(f"\n judge_dredd  --------->   {self.judge_scores}")


		print(f"\n last canvas card is {self.last_canvas_card}  ,  last_canvas_mod7 {self.last_canvas_mod7}  , last_canvas_color {self.last_canvas_color} ")


	def verdict(self, players_list):

		print(f" self.hot_player >>>> {self.hot_player}")

		hot_player_list_scores = players_list[self.hot_player].get_player_scores()

		tested_player_score = hot_player_list_scores[self.get_canvas_code()]


		judge_scores = self.judge_scores

		tested_color_code = self.get_canvas_code()


		print(hot_player_list_scores)
		print(tested_player_score)

		print(judge_scores)
		print(tested_color_code)

		tested_judge_score = judge_scores[tested_color_code]

		print(f" tested_judge_score  {tested_judge_score}")







		if tested_player_score < tested_judge_score:

			players_list[self.hot_player].alive = False

			print(f"\n\n\n ==>>>        judge_dredd just killed player {players_list[self.hot_player]}")

			#players_list[self.hot_player].player_scores = [0,0,0,0,0,0,0]



		else:

			print(f"\n\n\n  judge_dredd is OK with player {players_list[self.hot_player]}")

	def judgment_day(self, players_list):

		self.inspect_hot_player(players_list)
		self.get_judge_scores(players_list)
		self.verdict(players_list)













judge_dredd = Judge()

# -------------------------------------------------------------- CLASS PLAYER



class Player():

	

	def __init__(self, idx_player, human= False):

		self.idx_player = idx_player
		
		self.pal = []
		self.alive = True
		self.hand = []

		self.human = human

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

		if self.alive is True:
			self.player_scores = [self.score_red, self.score_violet,self.score_indigo,self.score_blue,self.score_green,self.score_yellow,self.score_orange]
		else:
			self.player_scores = [0,0,0,0,0,0,0]

		return self.player_scores







	def __str__(self):

		return f" Player {self.idx_player}   has Palette {self.pal}    life status is {self.alive}   last hand was {self.hand}"


	def get_hand(self, deck): # get 7+1 cards for begin the game, 7 in hand and extra one to launch the paleyr palette

		for distri in range(DISTRIBSIZE):
			newcard = deck.pop()
			self.hand.append(newcard)		



		#print(f" self.hand BEFORE drop ====>>>>  {self.hand}")

		#drop = self.hand.pop()

		#print(f" self.hand AFTER drop ====>>>>  {self.hand}")

		#print(f" sending__drop ====>>>>  {drop}")


		#self.fill_palette(drop)




	def very_first_fill_pal(self):

		drop = self.hand.pop()
		self.pal.append(drop)



	#def fill_palette(self, drop_choice: int = None):	
	def fill_palette(self, drop_choice: int):

		print(f" __drop_choice ====>>>>  {drop_choice}")

		#if drop_choice is None:			
		#	drop_choice = random.choice(self.hand)
		#	self.pal.append(drop_choice)
		#	self.hand.remove(drop_choice)


		#if drop_choice != None:			
		#	#drop_choice = random.choice(self.hand)
		#	self.pal.append(drop_choice)
		#	self.hand.remove(drop_choice)

		self.pal.append(drop_choice)
		self.hand.remove(drop_choice)


		#self.pal.append(drop_choice)
		#self.hand.remove(drop_choice)

		self.pal.sort() # S O R T
		self.hand.sort() # S O R T


	def fill_palette_random(self):

		print("INSIDE  fill_palette_random(self)")

		drop_choice = random.choice(self.hand)
		self.pal.append(drop_choice)
		self.hand.remove(drop_choice)
		self.pal.sort() # S O R T
		self.hand.sort() # S O R T


	


		
	

	def fill_canvas(self, drop_choice: int = None):		


		if drop_choice is None:			
			drop_choice = random.choice(self.hand)
		
		judge_dredd.canvas.append(drop_choice)
		self.hand.remove(drop_choice)
		self.hand.sort() 

		print(f"\n player {self.idx_player} fill_canvas  with drop_choice  {drop_choice}  ,  updated hand :   {self.hand}  , updated canvas  {judge_dredd.canvas}  rule is now {judge_dredd.last_canvas_color}")



	def draw_one_card(self,deck):
		pass

	


	def give_up(self):

		self.alive = False
		self.player_scores = [0,0,0,0,0,0,0]

		print(f"\n   >>> player {self.idx_player}  is giving up !!!  ")


	def random_action(self):

		if not self.hand == []:

			if len(self.hand) >= 2:

				act = random.randrange(3)

				judge_dredd.hot_player = self.idx_player
				judge_dredd.hot_action = act

				if act == 0:
					#self.fill_palette()
					self.fill_palette_random()
					print(f"\n\n\n---------0-------- player {self.idx_player}  fill_palette   ->  {self.pal}")

				elif act == 1:
					self.fill_canvas()
					print(f"\n\n\n--------1--------- player {self.idx_player}  fill_canvas")
				else:
					#self.fill_palette()
					self.fill_palette_random()
					self.fill_canvas()
					print(f"\n\n\n--------2--------- player {self.idx_player}  fill_palette _AND_ fill_canvas")

			else:

				act = random.randrange(2)

				judge_dredd.hot_player = self.idx_player
				judge_dredd.hot_action = act

				if act == 0:
					#self.fill_palette()
					self.fill_palette_random()
				elif act == 1:
					self.fill_canvas()

		else:

			
			act = 3

			judge_dredd.hot_player = self.idx_player
			judge_dredd.hot_action = act

			self.give_up()








	def sticker(self, card):

		val = value(card)
		col = color(card)

		#text = colored(val, col, attrs=['reverse', 'blink'])
		#text = colored(val, col)
		text = colored(val, col, attrs=['bold'])

		return text


	def show_palette(self):

		print(f"\n player {self.idx_player}    has Palette : \n ")

		for card in self.pal:

			#print(f" {card}")
			print(f"{self.sticker(card)}")



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

		print(f" _._._.> len(self.hand)    {len(self.hand)}")

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

# HUMAN PRESENCE !!!!!!!!!!!!!!
Players[0].human = True
print("PLAYER 0  is HUMAN !!!")

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
	player.very_first_fill_pal()

	player.debriefing()
	print("..............................................")


print("\n xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx  Fight  !!!!!")



"""

for j in range(5):
	print(" \n \n ________________________________________________________________________ TOUR  ",j)
	for player in Players:
		player.fill_palette()
		player.debriefing()


"""

#judge_dredd.still_alive_ids(Players)

#


def counting_alives(players_list):
	alives_status = [player.alive for player in players_list]
	count_alives = alives_status.count(True)


	print(" alives_status   =>   ", alives_status,"__________>>>>>>   count_alives  ",count_alives)
	#print(f"____________________________________________>>>>>>   count_alives  {count_alives}")


	

	if count_alives>1:
		AGAIN = True
	else:
		AGAIN = False



	return AGAIN







AGAIN = True

#while count_alives >1:
while AGAIN:

	for player in Players:

		if player.human is False and player.alive is True:
			player.random_action()

			judge_dredd.inspect_hot_player(Players)

			judge_dredd.get_judge_scores(Players)

			judge_dredd.verdict(Players)


			


			

			AGAIN = counting_alives(Players)


			

		elif player.human is True and player.alive is True:

			for gamer in Players:
				if gamer.alive is True:
					gamer.show_palette()

			print(f" canvas is {judge_dredd.last_canvas_color}")

			player.debriefing()

			action_human = int(input("\n   waiting for HUMAN  action ( __0=fill_palette,   __ 1=fill_canvas,   __ 2= Pal and Can    -> "))

			if action_human == 0:
				first_drop = int(input("first drop -> "))
				player.fill_palette(first_drop)
				print(f"\n\n\n---------0-------- player {player.idx_player}  fill_palette   ->  {player.pal}")

				judge_dredd.judgment_day(Players)

			elif action_human == 1:
				first_drop = int(input("first drop -> "))
				player.fill_canvas(first_drop)
				print(f"\n\n\n--------1--------- player {player.idx_player}  fill_canvas")
				judge_dredd.judgment_day(Players)

			elif action_human == 2:
				first_drop = int(input("first drop -> "))
				second_drop = int(input("second drop -> "))
				player.fill_palette(first_drop)
				player.fill_canvas(second_drop)
				print(f"\n\n\n--------2--------- player {player.idx_player}  fill_palette _AND_ fill_canvas")
				judge_dredd.judgment_day(Players)

			else:
				print("Sorry you are too much drunk, please respect your keyboard...")


		else:
			print("BBBUUUGGG")
			AGAIN = False # need a break or a pass ?, this line does not work













for player in Players:

		if player.alive is True:
			print(f"\n\n\n $$$ >>>  WINNER IS PLAYER  {player.idx_player}")



"""
id_player = 0

judge_dredd.inspect_hot_player(Players)

judge_dredd.get_judge_scores(Players)
"""