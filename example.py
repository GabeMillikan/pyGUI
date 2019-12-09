from pygui import pygui
from pygui.guiprofile import *
from pygui.good_tuple import mtuple
from pygui.color import color
import time
from preprofile import *

    
gui = pygui.window(suppress = True, profile = CNN_PROFILE)
gui.override_all(suppress = True)
gui.on_user_quit = gui.quit

def frameRender(fps):
    FPSCounter.txt = "FPS: " + str(fps).split(".")[0]

def x():
    print("Randomize Data Here")
    
RandomizeData.on_click = x
    
gui.on_frame_render = frameRender
    
gui.wait_for_frame()

gui.wait_until_quit()