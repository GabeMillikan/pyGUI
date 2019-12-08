from pygui import pygui
from pygui.color import color
import time
    
gui = pygui.window(suppress = True)
gui.override_all(suppress = True)
gui.on_user_quit = gui.quit

gui.set_fps(60)
gui.set_size((100,100))

gui.wait_until_ready()
print("ready!")

time.sleep(1)

gui.set_background_color(color(255,255,255))
time.sleep(1)

gui.set_background_color(color(255,127,0))
time.sleep(1)
gui.set_size((500,100))

gui.set_background_color(color(127,0,0))
time.sleep(1)

gui.set_background_color(color(0,0,0))
time.sleep(1)


gui.wait_until_quit()