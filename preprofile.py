from pygui import pygui
from pygui.guiprofile import *
from pygui.good_tuple import mtuple
from pygui.color import color
import time

#main
CNN_PROFILE = guiprofile()
CNN_PROFILE.fps = 99999
CNN_PROFILE.size = (800,600)

#FPS counter
FPSCounter = CNN_PROFILE.draw_text()
FPSCounter.size = 22;
FPSCounter.position = (3, 600 - 20)

#Credits
CreditText = CNN_PROFILE.draw_text()
CreditText.txt = "©Gabe 2022"
CreditText.size = 22;
CreditText.position = (675, 600 - 20)

#Randomize Data
RandomizeData = CNN_PROFILE.draw_button()
RandomizeData.set_background_color(color.white())
RandomizeData.set_rect((300, 570), (200,25))
RandomizeData.set_border(3, color.darkgray())
RandomizeData.set_label("Randomize data", 20, (25,6), color.darkgray())
