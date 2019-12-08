'''
    defaults
'''
from pygui.color import color
_FPS = 60
_WINDOW_WIDTH = 400
_WINDOW_HEIGHT = 300

class guiprofile:
    def __init__(self):
        self.fps = _FPS
        self.measure_fps_over_framecount = self.fps
        self.background_color = color.white
        self.size = (_WINDOW_WIDTH, _WINDOW_HEIGHT)
        