from pygui import pygui
from pygui.guiprofile import *
from pygui.good_tuple import mtuple
from pygui.color import color
import time

    
gui = pygui.window(suppress = True)
    
gui.override_all(suppress = True)
gui.on_user_quit = gui.quit

gui.set_fps(512)
gui.set_size((500,500))

rad = gui.add_radio(position = (10,30))
rad.set_title("My radio:")
rad.set_options(["Option 1", "Option 2"])

gui.wait_for_frame()

gui.wait_until_quit()