#! /usr/bin/env python3
# -*- coding: utf-8 -*-

# https://stackoverflow.com/questions/54165439/what-are-the-exact-color-names-available-in-pils-imagedraw/54165440
# https://www.youtube.com/watch?v=rLZk7cWbycI  FONTS Linux

# On linux you can find fonts for example here :  /usr/share/fonts/truetype/freefont

from PIL import Image, ImageFont, ImageDraw, ImageEnhance
import os

folder = "cardpics"
os.mkdir(folder)

CARD_WIDTH = 140 
CARD_HEIGHT = 190 


#font = ImageFont.load_default()

fontsize_a = 20
fontsize_c = 80

font_a = ImageFont.truetype("./freefont/FreeSansBoldOblique.ttf", fontsize_a)
font_c = ImageFont.truetype("./freefont/FreeSansBoldOblique.ttf", fontsize_c)


colors = ["violet","indigo","blue","green","yellow","orange","red"]

for col in colors:
	for i in range(1,8):
		button_img = Image.new('RGBA', (CARD_WIDTH,CARD_HEIGHT), col)

		button_draw = ImageDraw.Draw(button_img)
		button_draw.text((0, 0), f"{i}", font=font_a)
		button_draw.text((CARD_WIDTH//3, CARD_HEIGHT//3), f"{i}", font=font_c)

		button_img.save(f"./cardpics/{i}_{col}.png", "PNG")
