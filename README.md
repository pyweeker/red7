# red7   WORK ON PROGRESS
red7 card game demo for working on Artificial Intelligence

v36 shows stupid bots playing with random actions, each round the judge kills the weak ones

v41  player zero is human

v54 encoding state ok

v58 short encoding with only last canvas recorded, dead players skiped

v63  take_decision() 

v71 + gen12 : associating status with panorama actions, relative rewards are waiting for being evaluated by coming soon simulation

v76 : see EXPLORATION LOOP:
instanciation Players from ai.state_binary_ascii; fake filling manually ai.states_actions_rewards such as 
ai.states_actions_rewards {b'A1B2E3E4E5F0': {103: -1, 5004: 1}}

v77 decoding action

v87 buggy, backup before trying a defaultdic for filling up ai.states_actions_rewards

v90 + gen14 : Save pickle defaultdict ai.states_actions_rewards : 1120 states for two players, height first cards, one card on each palette, three cards in hand for player zero : data.pickle takes already 85,2 KiB (87 209 octets) ; can not save with json format due to TYPEERROR keys must be str, int, float, bool or None, not bytes ; could save on txt or .py but will be heavy and slower.

v92 timeit problem

v95 Memory saturation , processus halted => try use generators instead of lists

v100 : just select reward +1 solutions on each wave, no need brutforcing heavy dicts

with simple_card_maker.py you can use PIL to draw and save JPEG or PNG files for your cards.

make49.py draws card with names such as 49.jpeg

mysol.py is a variant of solitaire example provided by arcade library, adapted here for 49 colored cards

make49bis.py improves making cards for red7 game.
