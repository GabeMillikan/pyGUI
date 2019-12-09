'''
    defaults
'''
from pygui.good_tuple import mtuple
from pygui.color import color
_FPS = 60
_WINDOW_WIDTH = 400
_WINDOW_HEIGHT = 300
_BACKGROUND_COLOR = color.white()

class BaseElement:
    pass #nothing to do here, just for inheritence
    
class HigherElement:
    pass #nothing to do here, just for inheritence

class line(BaseElement):
    def __init__(self, start, end, clr, width):
        self.start = start
        self.end   = end
        self.color = clr
        self.width = width

class poly(BaseElement):
    def __init__(self, points, clr, closed, width):
        self.points = points
        self.color  = clr
        self.closed = closed
        self.width  = width
        
    def get_points_for_draw(self):
        return [mtuple(a).rounded().tuple() for a in self.points]
        
class circle(BaseElement):
    def __init__(self, origin, radius, clr, width, aa = False):
        self.origin = origin
        self.radius = radius
        self.color = clr
        self.width = width
        self.aa = aa
        
class text(BaseElement):
    def __init__(self, txt = "text", position = (10,10), font = "Consolas", size = 20, clr = color.darkgray(), highlight = None, bold = False, italic = False, rotation = 0):
        self.txt = txt
        self.position = position
        self.font = font
        self.size = size
        self.color = clr
        self.highlight = highlight
        self.bold = bold
        self.italic = italic
        self.rotation = 0
        
class radio(HigherElement):
    def __init__(self, position = (10,10), title = "Default Radio:", options = ["use", "radio.set_options()","to change this,", "or use dir(radio)", "for more customizations"]):
        self.defaultstyle()
        
        self.elements = []
        self.position = position
        
        self.position = position
        self.title = title
        self.options = options
        self.selected = 0
        
        self.build()
        
    def set_options(self, v):
        assert isinstance(v, list), "options must be a list of strings, ex: ['opt1', 'opt2']"
        self.options = v
        self.build()
        
    def set_title(self, v):
        self.title = v
        self.build()
        
    def set_position(self, pos):
        self.position = pos
        self.build()
    
    def set_selected(self, v):
        self.selected = v
        self.build()
        
    def defaultstyle(self):
        self.title_font = "Consolas"
        self.title_bold = False
        self.title_italic = False
        self.title_height = 20
        self.title_font_height = 20
        self.title_font_color = color.darkgray()
        self.title_offset = (4,0)
        
        self.option_font = "Consolas"
        self.option_bold = False
        self.option_italic = False
        self.option_height = 20
        self.option_font_height = 20
        self.option_font_color = color.darkgray()
        self.option_offset = (1,1.5)
        
        self.option_selected_color = color.softblue()
        self.option_deselected_color = color.darkgray()
        
    def style(self,
            title_font = None, title_bold = None, title_italic = None, title_height = None, title_font_height = None, title_font_color = None, title_offset = None,
            option_font = None, option_bold = None, option_italic = None, option_height = None, option_font_height = None, option_font_color = None, option_offset = None,
            option_selected_color = None, option_deselected_color = None):
        self.title_font = (title_font if title_font else self.title_font)
        self.title_bold = (title_bold if title_bold else self.title_bold)
        self.title_italic = (title_italic if title_italic else self.title_italic)
        self.title_height = (title_height if title_height else self.title_height)
        self.title_font_height = (title_font_height if title_font_height else self.title_font_height)
        self.title_font_color = (title_font_color if title_font_color else self.title_font_color)
        self.title_offset = (title_offset if title_offset else self.title_offset)
        
        
        self.option_font = (option_font if option_font else self.option_font)
        self.option_bold = (option_bold if option_bold else self.option_bold)
        self.option_italic = (option_italic if option_italic else self.option_italic)
        self.option_height = (option_height if option_height else self.option_height)
        self.option_font_height = (option_font_height if option_font_height else self.option_font_height)
        self.option_font_color = (option_font_color if option_font_color else self.option_font_color)
        self.option_offset = (option_offset if option_offset else self.option_offset)
        
        self.option_selected_color = (option_selected_color if option_selected_color else self.option_selected_color)
        self.option_deselected_color = (option_deselected_color if option_deselected_color else self.option_deselected_color)
        self.build()
        return
        
    def build(self):
        self.elements = []
        
        titleElement = text(txt = self.title)
        titleElement.font = self.title_font
        titleElement.size = self.title_font_height
        titleElement.color = self.title_font_color
        titleElement.highlight = None #TODO
        titleElement.bold = self.title_bold
        titleElement.italic = self.title_italic
        
        titleElement.position = (mtuple(self.position) + mtuple(self.title_offset)).rounded().tuple()
        
        self.elements.append(titleElement)
        
        for i in range(len(self.options)):
            optcenter = mtuple(self.position) + mtuple(self.option_height/2, self.option_height*(i+0.5)) + mtuple(0, self.title_height)
            optioncircle = circle(optcenter.rounded().tuple(), self.option_height/2 - 3, self.option_selected_color if i == self.selected else self.option_deselected_color, 1, aa=True)
            self.elements.append(optioncircle)
            
            if i == self.selected:
                optcenter = mtuple(self.position) + mtuple(self.option_height/2, self.option_height*(i+0.5)) + mtuple(0, self.title_height)
                optdot = circle(optcenter.rounded().tuple(), self.option_height/2 - 6, self.option_selected_color, 0, aa=True)
                self.elements.append(optdot)
        
            optiontext = text(txt = self.options[i])
            optiontext.font = self.option_font
            optiontext.size = self.option_font_height
            optiontext.color = self.option_font_color
            optiontext.highlight = None #TODO
            optiontext.bold = self.option_bold
            optiontext.italic = self.option_italic
        
            optiontext.position = mtuple(self.position) + mtuple(self.option_height, self.title_height + (self.option_height*i)) + mtuple(self.option_offset)
            optiontext.position = optiontext.position.rounded().tuple()
            self.elements.append(optiontext)
            
    def on_selection_changed(self, newselection):
        print("radio.on_selection_changed(" + str(newselection) + ") was called, handle me!")
        
class button(HigherElement):   
    def __init__(self, position, size, label):
        self.font_size = 15
        self.font = "Consolas"
        self.position = position
        self.size = size
        self.label = label
        
        self.background_color = color.lightgray()
        self.outline_color = color.darkgray()
        self.border_width = 2
        self.font_color = color(25,25,25)
        self.label_offset = ( mtuple(size) / 2).tuple()
        
        self.elements = []
        self.build()
        
    def set_rect(self, pos, size):
        self.position = pos
        self.size = size
        self.build()
        
    def set_label(self, txt, font_size, label_offset, font_color, font = "Consolas"):
        self.label = txt
        self.font_size = font_size
        self.label_offset = label_offset
        self.font_color = font_color
        self.font = font
        self.build()
        
    def set_background_color(self, c):
        self.background_color = c
        self.build()
        
    def set_border(self, width, clr):
        self.border_width = width
        self.outline_color = clr
        self.build()
        
    def on_click(self):
        print("Default button.on_click()... Overrride me!")
        
    def build(self):
        self.elements = []
        #border
        self.elements.append(
            poly(
                [self.position,
                (self.position[0] + self.size[0], self.position[1]),
                (mtuple(self.position) + mtuple(self.size)).tuple(),
                (self.position[0], self.position[1] + self.size[1])
                ],
                self.outline_color, True, self.border_width)
            )
        #background
        self.elements.append(
            poly(
                [self.position,
                (self.position[0] + self.size[0], self.position[1]),
                (mtuple(self.position) + mtuple(self.size)).tuple(),
                (self.position[0], self.position[1] + self.size[1])
                ],
                self.background_color, True, 0)
        )
        #label
        self.elements.append(
            text(txt = self.label, position = (mtuple(self.position)+mtuple(self.label_offset)).tuple(), font = self.font, size = self.font_size, clr = self.font_color)
        )
        
        
class guiprofile:
    def __init__(self):
        self.fps = _FPS
        self.background_color = _BACKGROUND_COLOR
        self.size = (_WINDOW_WIDTH, _WINDOW_HEIGHT)
        
        #elements
        self.renderqueue = []
        
    def draw_line(self, start, end, clr = color.black(), width = 1):
        new = line(start, end, clr, width)
        self.renderqueue.append(new)
        return new
        
    def draw_poly(self, points, clr, closed = False, width = 1):
        new = poly(points, clr, closed, width)
        self.renderqueue.append(new)
        return new
        
    def draw_circle(self, origin, radius, clr = color.black(), width = 1):
        new = circle(origin, radius, clr, width)
        self.renderqueue.append(new)
        return new
        
    def draw_button(self, position = (0,0), size = (20,10), label = "Button"):
        new = button(position, size, label)
        self.renderqueue.append(new)
        return new
        
    def draw_text(self, txt = "text", position = (10,10), font = "Consolas", size = 20, clr = color.darkgray(), highlight = None, bold = False, italic = False, rotation = 0):
        new = text(txt = txt, position = position, font = font, size = size, clr = clr, highlight = highlight, bold = bold, italic = italic, rotation = rotation)
        self.renderqueue.append(new)
        return new
        
    def draw_radio(self, position = (10,10), title = "Default Radio:", options = ["use", "radio.set_options()","to change this,", "or use dir(radio)", "for more customizations"]):
        new = radio(position = position, title = title, options = options)
        self.renderqueue.append(new)
        return new
        
        