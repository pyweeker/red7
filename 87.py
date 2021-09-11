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


import base64
from sys import getsizeof

import re
#-------------------------------------------------------------- CST

PLAYERS_NB = 2
#PLAYERS_NB = 4


DISTRIBSIZE = 8 #(7 playable cards +1 for range in/exclusion)

#DECK_MAX_RANGE = 50

DECK_MAX_RANGE = 9

MOD7dict = {0: "red", 6: "grey", 5: "yellow", 4: "green", 3: "blue", 2: "cyan", 1: "magenta"}


#------------------------------- DICA  AI

from gen14 import *
possible_first_tables = encode_tabloids(tabloids)

#print(possible_first_table)

#x = input("ok ?")


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

    

    def verdict_with_returned_reward(self, players_list):

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

            

            reward = -1
            print(f"\n\n\n ==>>>        judge_dredd just killed player {players_list[self.hot_player]}        REWARD {reward}")
            return reward

            #players_list[self.hot_player].player_scores = [0,0,0,0,0,0,0]



        else:

            

            reward = 1
            print(f"\n\n\n  judge_dredd is OK with player {players_list[self.hot_player]}       REWARD {reward}")
            return reward

    


    def judgment_day(self, players_list):

        self.inspect_hot_player(players_list)
        self.get_judge_scores(players_list)
        self.verdict(players_list)


    



    def judgment_day_with_returned_reward(self, players_list):

        self.inspect_hot_player(players_list)
        self.get_judge_scores(players_list)
        returned_reward = self.verdict_with_returned_reward(players_list)
        return returned_reward


    #def decode_action(self, code_action):
    def decode_action(self, code_action, players_list):
        
        if code_action <200:
            decoded_card = code_action - 100
            #print(f"\n *!+  decoding code_action {code_action}  => fill_palette {code_action - 100}    \n")
            print(f"\n *!+  decoding code_action {code_action}  => fill_palette {decoded_card}    \n")

            players_list[0].fill_palette(decoded_card)


        elif code_action <1000:
            decoded_card = code_action - 200
            #print(f"\n *!+d  ecoding code_action {code_action}  => fill_canvas {code_action - 200}     \n")
            print(f"\n *!+d  ecoding code_action {code_action}  => fill_canvas {decoded_card}     \n")
            players_list[0].fill_canvas(decoded_card)


        else:
            duo_pal = code_action//1000
            duo_can = code_action%1000

            print(f"\n *!+  decoding code_action {code_action}  => fill_palette {duo_pal}  AND  fill_canvas {duo_can}      \n")

            players_list[0].fill_palette(duo_pal)
            players_list[0].fill_canvas(duo_can)



    #def genial(self, code_action):
    def genial(self, code_action, players_list):

        print(f" genial method inside judge klass received arg  code_action = {code_action}              calling    self.decode_action(code_action)")

        #self.decode_action(code_action)
        self.decode_action(code_action, players_list)

        #self.judgment_day(players_list)

        returned_reward = self.judgment_day_with_returned_reward(players_list)
        #ai.launch_table(players_list)
        ai.launch_table(players_list, table)


        return returned_reward

        













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
        #    if (k % 2) != 0:


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


        



        




    def very_first_fill_pal(self):

        drop = self.hand.pop()
        self.pal.append(drop)


        #self.pal.sort() # S O R T just one call, just one card in pal at first
        self.hand.sort() # S O R T





    #def fill_palette(self, drop_choice: int = None):    
    def fill_palette(self, drop_choice: int):

        print(f" __drop_choice ====>>>>  {drop_choice}")

        #if drop_choice is None:            
        #    drop_choice = random.choice(self.hand)
        #    self.pal.append(drop_choice)
        #    self.hand.remove(drop_choice)


        #if drop_choice != None:            
        #    #drop_choice = random.choice(self.hand)
        #    self.pal.append(drop_choice)
        #    self.hand.remove(drop_choice)

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


#***************************************************************

    @property
    def panorama(self): # provide all possible code_action for a concrete state.

        print("--Hello from panorama  method inside Player Class")

        possibles_code_action = []

        permut_pal_and_can=list(itertools.permutations(self.hand, 2))



        for card in self.hand:

            code_action_pal = card + 100
            code_action_can = card  + 200

            possibles_code_action.append(code_action_pal)
            possibles_code_action.append(code_action_can)


        print(f"permut_pal_and_can   {permut_pal_and_can}")


        for permut in permut_pal_and_can:

            code_action_pal_and_can = permut[0] * 1000 + permut[1] # ATTENTION COMBO CARDS 1,2
            print(f"permut[0]  {permut[0]}      permut[1] {permut[1]}          code_action_pal_and_can  {code_action_pal_and_can}")
            possibles_code_action.append(code_action_pal_and_can)



        for pan in possibles_code_action:

            duo_pal = pan//1000
            duo_can = pan%1000

            if duo_pal > 0:
                print(f" duo_pal {duo_pal}    duo_can {duo_can}")




        return possibles_code_action











    def take_decision(self): # METTRE UN REWARD PAR DEFAUT EN ATTENDANT FEEDBACK EVALUATIF

        if not self.hand == []:

            if len(self.hand) >= 2:

                act = random.randrange(3)

                judge_dredd.hot_player = self.idx_player
                judge_dredd.hot_action = act

                if act == 0:
                    drop_choice_palette = random.choice(self.hand)

                    code_action = drop_choice_palette + 100


                    self.fill_palette(drop_choice_palette)
                    #self.fill_palette_random()
                    print(f"\n\n\n---------0-------- player {self.idx_player}  fill_palette   ->  {self.pal}  with card {drop_choice_palette}")


                    return code_action





                elif act == 1:
                    #self.fill_canvas()
                    drop_choice_canvas = random.choice(self.hand)

                    code_action = drop_choice_canvas + 200


                    self.fill_canvas(drop_choice_canvas)


                    print(f"\n\n\n--------1--------- player {self.idx_player}  fill_canvas    with card {drop_choice_canvas}")

                    return code_action

                else:
                    #self.fill_palette()
                    drop_choice_palette = random.choice(self.hand)
                    self.fill_palette(drop_choice_palette)
                    drop_choice_canvas = random.choice(self.hand)
                    self.fill_canvas(drop_choice_canvas)

                    code_action = drop_choice_palette * 100 + drop_choice_canvas 


                    print(f"\n\n\n--------2--------- player {self.idx_player}  fill_palette _AND_ fill_canvas  : +palette  {drop_choice_palette}    +canvas {drop_choice_canvas}")

                    return code_action

            else:

                act = random.randrange(2)

                judge_dredd.hot_player = self.idx_player
                judge_dredd.hot_action = act

                if act == 0:
                    drop_choice_palette = random.choice(self.hand)

                    code_action = drop_choice_palette + 100


                    self.fill_palette(drop_choice_palette)
                    print(f"\n\n\n---------0-------- player {self.idx_player}  fill_palette   ->  {self.pal}  with card {drop_choice_palette}")
                    #self.fill_palette_random()

                    return code_action

                elif act == 1:
                    drop_choice_canvas = random.choice(self.hand)

                    code_action = drop_choice_canvas + 200


                    self.fill_canvas(drop_choice_canvas)
                    print(f"\n\n\n--------1--------- player {self.idx_player}  fill_canvas    with card {drop_choice_canvas}")

                    return code_action

        else:

            
            act = 3

            code_action = 300

            judge_dredd.hot_player = self.idx_player
            judge_dredd.hot_action = act

            self.give_up()

            return code_action


#***************************************************************





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
        

        print(f"Palette   player {self.idx_player}")

        for card in self.pal:
            print(f"         +   {self.sticker(card)}              {value(card)}    {color(card)}                    card {card}")
        print("\n\n")

        print(f"Hand   player {self.idx_player}")


        for card in self.hand:

            

            print(f" -   {self.sticker(card)}              {value(card)}    {color(card)}                       card {card}")


        #palette_to_show = [self.sticker(card)  for card in self.pal]

        print(f" _._._.> len(self.hand)    {len(self.hand)}")

        print("\n ....... . . . ..  ...   ...   ....   ....   .....   ..............")









# -------------------------------------------------------------- INIT


Players = []





deck = [x for x in range(0,DECK_MAX_RANGE)]

"""


for i in range(PLAYERS_NB):
    newplayer = Player(i)
    Players.append(newplayer)

# HUMAN PRESENCE !!!!!!!!!!!!!!
Players[0].human = True
print("PLAYER 0  is HUMAN !!!")
"""
#-------------------------------------------------------------- SET UP




#---------------------------------------------------------------- GUI

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


clear_screen()

print("__ ATTENTION JOKER 0 __\n\n")



#------------- verif debug starting

shuffle(deck)





#---------------------------------------------------------------- distri

"""
for player in Players:
    player.get_hand(deck)
    player.very_first_fill_pal()

    player.debriefing()
    print("..............................................")

print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
print("\n xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx  Fight  !!!!!")

"""




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


# -------------------------------------------------------------- CLASS Brain


class Brain():

    def __init__(self):

        self.state_binary_ascii = None

        self.tabloids = list(list())

        self.states_actions = dict()

        self.states_actions_rewards = dict(dict())

    def cheat_player_one(self, players_list): # for test and debug

        players_list[1].pal = [49]

        print("\n CALLING cheat_player_one()   ")


    def show_states_actions_rewards(self):
        print(f"\n____________________________\n {self.states_actions_rewards}")



    #def launch_table(self, players_list):
    def launch_table(self, players_list, table):


        
        #self.state_binary_ascii = self.tabloids[0]

        #a table looks like  b'A4B2E1E3E5F0'

        self.state_binary_ascii = table

        state_binary_str = str(self.state_binary_ascii)

        # 'A1B2E3E4E5F0'

        tokens = re.findall(r'[A-Z][0-9]+', state_binary_str)
        groups = {}
        for token in tokens:
            letter = token[0]
            number = int(token[1:])
            groups.setdefault(letter, []).append(number)

            #groups = {'A': [10, 14, 28], 'B': [33, 44], 'C': [17, 21], 'D': [6, 18, 25], 'E': [13, 15, 20, 35], 'F': [0, 1, 0, 19, 5]}


        print(f" \n\n________________>>Fist msg inside Brain launch_table method, look Players {players_list}")

        if players_list != []:
            players_list.clear()



        if 'A' in groups:
                PlayerA = Player(0)
                PlayerA.pal = groups['A']
                if 'E' in groups:
                    PlayerA.hand = groups['E']

                players_list.append(PlayerA)

        if 'B' in groups:
            PlayerB = Player(1)
            PlayerB.pal = groups['B']
            players_list.append(PlayerB)


        judge_dredd.canvas = groups['F']

        print(f" \n\n________________>>Second msg inside Brain launch_table method, look Players {players_list}")

        print(players_list[0].__dict__)


        self.cheat_player_one(players_list)

        










    #@property
    def encode(self, players_list, judge): # 4 players version , ia on player 0

        

        Apal_list = players_list[0].pal
        Bpal_list = players_list[1].pal
        #Cpal_list = players_list[2].pal
        #Dpal_list = players_list[3].pal

        Cpal_list = None
        Dpal_list = None


        #all_players_pals = [Apal_list,Bpal_list,Cpal_list,Dpal_list]
        all_players_pals = [Apal_list,Bpal_list]


        Ehand_list = players_list[0].hand

        print(f" Ehand_list = players_list[0].hand  {Ehand_list}")

        Fcanvas_list = judge_dredd.canvas













        #--------

        charnumsA = []

        for card in Apal_list: # player zero

            charnumsA.append('A' + str(card))


        if players_list[0].alive is True:
            Astr = ''.join(charnumsA)
        else:
            Astr = ''

        #--------    
        charnumsB = []

        for card in Bpal_list: 

            charnumsB.append('B' + str(card))


        if players_list[1].alive is True:
            Bstr = ''.join(charnumsB)
        else:
            Bstr = ''

        #--------    
        
                
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


        #state_hexa = Astr + Bstr + Cstr + Dstr + Estr + Fstr
        state_hexa = Astr + Bstr + Estr + Fstr




        print(f"-->==>  >>>>     _Encoding state gives    state_hexa =  {state_hexa}       getsizeof(state_hexa) = {getsizeof(state_hexa)}")


        #AJOUTER 'X' + index du current player pour donner referentiel d interpretation. Attention X depasse les lettres hexa, base 64 ?

        # https://stackoverflow.com/questions/43207978/python-converting-from-base64-to-binary

        state_binary_ascii=state_hexa.encode("ascii")

        self.state_binary_ascii = state_binary_ascii

        print("state_binary_ascii = ",state_binary_ascii,"type",type(state_binary_ascii), "getsizeof(t)   ",getsizeof(state_binary_ascii))

        sample_string_bytes = state_binary_ascii

        base64_bytes = base64.b64encode(sample_string_bytes)
        print("base64_bytes = ",base64_bytes,"     getsizeof(base64_bytes)       ",getsizeof(base64_bytes))

        base64_string = base64_bytes.decode("ascii")
        print("base64_string = ",base64_string,"     getsizeof(base64_string)       ",getsizeof(base64_string))


        #decoded = base64.decodebytes(t)
        decoded = base64.decodebytes(base64_bytes)


        print(decoded)
        print(len(decoded)*8)

        zeros_and_ones = "".join(["{:08b}".format(x) for x in decoded])

        #print("".join(["{:08b}".format(x) for x in decoded]))

        print(f" zeros_and_ones is type {type(zeros_and_ones)}  and is value \n     {zeros_and_ones}         getsizeof(zeros_and_ones) = {getsizeof(zeros_and_ones)}  ")

        int_from_base2 = int(zeros_and_ones, 2)

        print(f" int_from_base2 is type {type(int_from_base2)}  and is value \n     {int_from_base2}            getsizeof(int_from_base2) = {getsizeof(int_from_base2)}")


        size_of_variable = getsizeof(int_from_base2)

        print(f"   size_of_variable  > int_from_base2   {size_of_variable} ")


        str_from_int = str(int_from_base2)


        size_of_variable = getsizeof(str_from_int)

        print(f"   size_of_variable >>> str_from_int {size_of_variable} ")


        return state_hexa



    





    def get_possible_first_tables(self, tabloids):

        # [b'A1B2E3E4E5F0', ...]



    	


    	self.tabloids = tabloids


    def fill_states_actions(self, panorama):
        

        

        self.states_actions[self.state_binary_ascii] = panorama


    def prepare_states_actions_rewards(self):

        #self.states_actions_rewards = dict(zip(self.tabloids, "None"))
        # d = {i: i**2 for i in range(10) if i%2==0}


        #self.states_actions_rewards = {i: 666 for i in self.tabloids}

        for k,v in self.states_actions.items():
            self.states_actions_rewards[k] = dict()


        print(f"self.states_actions_rewards   INSIDE prepare_states_actions_rewards method   \n  {self.states_actions_rewards}")



    #def fill_states_actions_rewards(self, code_action, reward):
    def fill_states_actions_rewards(self, state_binary_ascii, code_action, reward):  

        #self.states_actions_rewards[self.state_binary_ascii][code_action] = reward
        #self.states_actions_rewards[state_binary_ascii][code_action] = reward

        #new_entry = {state_binary_ascii: {code_action: reward}}
        new_entry = {code_action: reward}

        #self.states_actions_rewards.update(new_entry)


        self.states_actions_rewards[state_binary_ascii].update(new_entry)



ai = Brain()

ai.get_possible_first_tables(possible_first_tables)



EXPLORATION = True

while EXPLORATION:

    print(ai.__dict__)

    print(ai.states_actions_rewards)

    # !

    print(f"ai.states_actions.items()  \n {ai.states_actions.items()}")

    ai.prepare_states_actions_rewards()

    print(f"ai.states_actions.items()  \n {ai.states_actions.items()}")

    z = input(" WTF ? ")



    for table in ai.tabloids:



    #ai.launch_table(Players)
        ai.launch_table(Players, table)

        print("\n * ---> ",ai.state_binary_ascii)


        for player in Players:

            print(player)


        panorama_0 = Players[0].panorama

        print(f" panorama_0 {panorama_0}")


        ai.fill_states_actions(panorama_0)

        print(f" ai.states_actions {ai.states_actions}")


        #ai.fill_states_actions_rewards(b'A1B2E3E4E5F0',777) 


        print(f" ai.states_actions_rewards {ai.states_actions_rewards}")

        







        #ai.prepare_states_actions_rewards()                                     # KeyError: b'A1B2E3E4E5F0'   self.states_actions_rewards[self.state_binary_ascii][code_action] = reward

        print(f" ai.states_actions_rewards {ai.states_actions_rewards}")





        print(f" ... ai.states_actions_rewards {ai.states_actions_rewards}")


        state_now = ai.state_binary_ascii
        returned_rewards = []
        for code_action in ai.states_actions[state_now]:
            #some_reward = judge_dredd.genial(code_action)
            some_reward = judge_dredd.genial(code_action, Players)





            print(f"ai.states_actions[state_now]   =  {ai.states_actions[state_now]}           code_action   {code_action}")

            import inspect
            sign = inspect.signature(ai.fill_states_actions_rewards)
            print(f"\n\n\n                         sign ai.fill_states_actions_rewards ====>  {sign}     \n\n\n")

            ai.fill_states_actions_rewards(state_now,code_action, some_reward)


            print(f" ... ai.states_actions_rewards {ai.states_actions_rewards}")




    ai.show_states_actions_rewards()




    


    xyz = input("\n >>> ok ?")




    #for table in ai.tabloids:

    #    ai.state_binary_ascii = table

    #    for code_action in ?[table]:

    #        if ai.states_actions_rewards[table][code_action] == 'Unknown':

    #            print("Unknown")



#//////////////////////

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

            print(f"                                              canvas is $ => ___ {judge_dredd.last_canvas_color}  ___")

            player.debriefing()

            state_hexa = ai.encode(Players, judge_dredd)


            #panorama = player.panorama()
            print(f"\n\n $$$$$$$$$$$$$$        panorama  {player.panorama}  \n\n")

            print("ai  =  ", ai)
            #ai.states_actions[]
            ai.fill_states_actions(player.panorama)


            print(f"\n\n _ _ _        ai.states_actions  {ai.states_actions}  \n\n")

            ai.prepare_states_actions_rewards()


            for code_action in player.panorama:
                reward= "Unknown"
                ai.fill_states_actions_rewards(code_action, reward)


            print(f"\n\n -_-_-_-        ai.states_actions_rewards  {ai.states_actions_rewards}  \n\n")




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
charnumsC = []

        for card in Cpal_list: 

            charnumsC.append('C' + str(card))


        if players_list[2].alive is True:
            Cstr = ''.join(charnumsC)
        else:
            Cstr = ''

        #--------    
        charnumsD = []

        for card in Dpal_list: 

            charnumsD.append('D' + str(card))


        if players_list[3].alive is True:
            Dstr = ''.join(charnumsD)
        else:
            Dstr = ''s
"""



"""
id_player = 0

judge_dredd.inspect_hot_player(Players)

judge_dredd.get_judge_scores(Players)
"""

# TRY

"""
if 'A' in groups:
                PlayerA = Player(0)
                PlayerA.pal = groups['A']
                if 'E' in groups:
                    PlayerA.hand = groups['E']

                players_list.append(PlayerA)

if 'B' in groups:
    PlayerB = Player(1)
    PlayerB.pal
    players_list.append(PlayerB)


judge_dredd.canvas = groups['F']
"""

"""
try:

            
            PlayerA = Player(0)
            PlayerA.pal = groups['A']
                
            PlayerA.hand = groups['E']

            players_list.append(PlayerA)

            
            PlayerB = Player(1)
            PlayerB.pal= groups['B']
            players_list.append(PlayerB)


            judge_dredd.canvas = groups['F']

        except:
            print("An exception occurred")
"""