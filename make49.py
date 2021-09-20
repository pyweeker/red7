#! /usr/bin/env python3
# -*- coding: utf-8 -*-

# https://stackoverflow.com/questions/54165439/what-are-the-exact-color-names-available-in-pils-imagedraw/54165440
# https://www.youtube.com/watch?v=rLZk7cWbycI  FONTS Linux

# On linux you can find fronts for example here :  /usr/share/fonts/truetype/freefont

from PIL import Image, ImageFont, ImageDraw, ImageEnhance
import os

folder = "49"
os.mkdir(folder)

CARD_WIDTH = 140 
CARD_HEIGHT = 190 


#font = ImageFont.load_default()

fontsize_a = 20
fontsize_c = 80

font_a = ImageFont.truetype("./freefont/FreeSansBoldOblique.ttf", fontsize_a)
font_c = ImageFont.truetype("./freefont/FreeSansBoldOblique.ttf", fontsize_c)

from itertools import cycle
colors = ["violet","indigo","blue","green","yellow","orange","red"]

colors_cycle = cycle(colors)
print(colors_cycle)





for i in range(1,50):

	next_colors_cycle = next(colors_cycle)

	button_img = Image.new('RGB', (CARD_WIDTH,CARD_HEIGHT), next_colors_cycle)

	button_draw = ImageDraw.Draw(button_img)
	button_draw.text((0, 0), f"{i}", font=font_a)

	if i<10:
		button_draw.text((CARD_WIDTH//3, CARD_HEIGHT//3), f"{i}", font=font_c)
	else:
		button_draw.text((CARD_WIDTH//7, CARD_HEIGHT//3), f"{i}", font=font_c)

	button_img.save(f"./49/{i}.jpg", "JPEG")


