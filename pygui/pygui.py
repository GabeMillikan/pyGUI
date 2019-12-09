import threading
import time
from pygui.guiprofile import *
from pygui.color import color
from pygui.good_tuple import mtuple

class window:
    def __init__(self, profile = guiprofile(), suppress = False):
        if not suppress:
            print("Created window!")
            print("Note that only ONE window can be created per python instance running")
            print("To hide this message, create window(suppress = True)")
        """
            setup variables
        """
        self._running = True
        self.loaded = False
        self.profile = profile
        self._mousepos = (0,0)
        self.observed_fps = self.profile.fps
        
        """
            begin program
        """
        self._main_thread = threading.Thread(target = self._disp_thread)
        self._main_thread.start()
        self.frames_displayed = 0
        
    def quit(self):
        self._running = False
        self._main_thread.join()
        
    def on_user_quit(self):
        print("default window.on_user_quit()... Override me!")
        self.quit()
        
    def on_frame_render(self, framerate):
        print("default window.on_frame_render(framerate)... Override me! --try to keep this light for better performance")
        
    def wait_until_quit(self, accuracy = 0.1):
        while self._running:
            time.sleep(accuracy)
        return
        
    def wait_until_ready(self, accuracy = 0.1):
        while self.loaded:
            time.sleep(accuracy)
        return
        
    def wait_for_frame(self):
        c = self.frames_displayed
        while c == self.frames_displayed:
            time.sleep(0)
        return
        
    def _quit_event(self):
        try:
            self.on_user_quit()
        except Exception as e:
            print("Error when calling window.on_user_quit():\n  " + str(e.__class__.__name__) + " : " + str(e))
            
    def _on_mouse_click(self, x, y):
        for elem in self.profile.renderqueue:
            #clicked on radio
            if isinstance(elem, radio):
                if elem.position[0] < x < (elem.position[0] + elem.option_height):
                    #correct x for a radio switch
                    for i in range(len(elem.options)):
                        if i*elem.option_height < y - (elem.position[1] + elem.title_height) < (i+1)*elem.option_height:
                            if not(i==elem.selected):
                                #selected new option
                                elem.set_selected(i)
                                threading.Thread(target = elem.on_selection_changed, args = ([i])).start()
        
    def _disp_thread(self):
        #get pygame
        import sys,io
        outputtrap = io.StringIO()
        sys.stdout = outputtrap
        import pygame
        import pygame.freetype
        import pygame.gfxdraw
        pygame.init()
        pygame.freetype.init()
        #restore printing
        sys.stdout = sys.__stdout__
        #print things that werent part of pygame
        outputtrap = outputtrap.getvalue().split("\n")
        for l in outputtrap:
            if l.find("pygame") < 0:
                print(l)
        outputtrap = None
        #set loadstatus
        self.loaded = True
        
        self.stored_fonts = {}
        
        background = pygame.display.set_mode(self.profile.size)
        clock = pygame.time.Clock()
        fps_adjustment = 0
        start_framemeasure = time.monotonic()
        while self._running: 
            '''
                get observed framerate
            '''
            if ((self.frames_displayed+1) % self.profile.fps) == 0:
                self.observed_fps = self.profile.fps / (time.monotonic() - start_framemeasure)
                start_framemeasure = time.monotonic()
            else:
                self.observed_fps = (self.observed_fps*99 + (clock.get_fps() if clock.get_fps()>0 else self.observed_fps))/100
                
            '''
                call on_frame_render
                    - parameter is the average observed framerate
            '''
            try:
                self.on_frame_render(self.observed_fps)
            except Exception as e:
                print("\nError when calling window.on_frame_render(" + str(self.observed_fps) + "):\n  " + str(e.__class__.__name__) + " : " + str(e))
                
            '''
                event handling
            '''
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    threading.Thread(target = self._quit_event).start()
                if event.type == pygame.MOUSEBUTTONUP:
                    threading.Thread(target = self._on_mouse_click, args=(self.get_mouse_pos())).start()
            self._mousepos = pygame.mouse.get_pos()
                
            '''
                update frame settings
            '''
            currentsize = pygame.display.get_surface().get_size()
            if not (currentsize[0] == self.profile.size[0] and currentsize[1] == self.profile.size[1]):
                background = pygame.display.set_mode(self.profile.size)
                
            '''
                Draw frame
            '''
            #fill background
            background.fill(self.profile.background_color.rounded().tuple())
            #draw elements in queue
            for render in self.profile.renderqueue:
                for element in (render.elements if issubclass(render.__class__, HigherElement) else [render]): #loop thru child elements if its a HigherElement, else loop thru [element]
                    #draw line
                    if isinstance(element, line):
                        pygame.draw.line(background, element.color.rounded().tuple(), element.start, element.end, element.width)
                        
                    #draw polygon
                    if isinstance(element, poly):
                        pygame.draw.lines(background, element.color.rounded().tuple(), element.closed.rounded().tuple(), element.get_points_for_draw(), element.width);
                        
                    #draw circle
                    if isinstance(element, circle): 
                        if not element.aa:
                            pygame.draw.circle(background, element.color.rounded().tuple(), mtuple(element.origin).rounded().tuple(), int(round(element.radius)), int(round(element.width)))
                        else:
                            if element.width > 0:
                                pygame.gfxdraw.aacircle(background, int(round(element.origin[0])), int(round(element.origin[1])), int(round(element.radius)), element.color.rounded().tuple())
                            else:
                                pygame.gfxdraw.aacircle(background, int(round(element.origin[0])), int(round(element.origin[1])), int(round(element.radius)), element.color.rounded().tuple())
                                pygame.gfxdraw.filled_circle(background, int(round(element.origin[0])), int(round(element.origin[1])), int(round(element.radius)), element.color.rounded().tuple())
                        
                    #draw text
                    if isinstance(element, text):
                        if not(element.font in self.stored_fonts):
                            self.stored_fonts[element.font] = pygame.freetype.SysFont(element.font, 1, element.bold, element.italic)
                        self.stored_fonts[element.font].render_to(background, element.position, element.txt, fgcolor = element.color.rounded().tuple(), bgcolor = (None if not element.highlight else element.highlight.rounded().tuple()), rotation = element.rotation, size = element.size)
            
            '''
                Put frame on screen
            '''
            pygame.display.update()
            self.frames_displayed += 1
            
            '''
                tick the clock
                adjust tick time to attempt to reach true framerate
                    - if observed < profile.fps, increase clocktick: positive adjustment
                    - if observed > profile.fps, decrease clocktick: negative adjustment
                    - slowly change adjustment over time to P(ID) to the true fps
            '''
            if self.observed_fps < self.profile.fps:
                fps_adjustment += ( self.profile.fps - self.observed_fps )/self.profile.fps
            elif self.observed_fps > self.profile.fps: #both floats, = else:
                fps_adjustment -= ( self.observed_fps - self.profile.fps )/self.profile.fps
            
            if fps_adjustment < (100*self.observed_fps): # if we're doing that bad, chances are that clock.tick is just slowing us down
                clock.tick(self.profile.fps + fps_adjustment)
        pygame.quit()
        return
        
    '''
        set / add or remove
    '''
    def set_fps(self, value):
        self.profile.fps = value
        
    def set_background_color(self, clr):
        self.profile.background_color = clr
    
    def set_size(self, size):
        self.profile.size = size
    
    def add_line(self, start, end, clr = color.black(), width = 1):
        return self.profile.draw_line(start, end, clr = clr, width = width)
    
    def add_poly(self, points, clr = color.black(), closed = False, width = 1):
        return self.profile.draw_poly(points, clr, closed = closed, width = width)
        
    def add_outlined_rect(self, start, size, clr = color.black(), width = 1):
        return self.add_poly(
                            [start,
                            (start[0] + size[0], start[1]),
                            (start[0] + size[0], start[1] + size[1]),
                            (start[0], start[1] + size[1])],
                            clr = clr, closed = True, width = width)
                            
    def add_outlined_circle(self, origin, radius, clr = color.black(), width = 1):
        return self.profile.draw_circle(origin, radius, clr = clr, width = width)
        
    def add_filled_circle(self, origin, radius, clr = color.black()):
        return self.profile.draw_circle(origin, radius, clr = clr, width = 0)
        
    def add_text(self, txt = "text", position = (10,10), font = "Consolas", size = 20, clr = color.darkgray(), highlight = None, bold = False, italic = False, rotation = 0):
        return self.profile.draw_text(txt = txt, position = position, font = font, size = size, clr = clr, highlight = highlight, bold = bold, italic = italic, rotation = rotation)
        
    def add_radio(self, position = (10,10), title = "Default Radio:", options = ["use", "radio.set_options()","to change this,", "or use dir(radio)", "for more customizations"]):
        return self.profile.draw_radio(position=position, title=title,options=options)
        
    '''
        get
    '''
    def get_is_running(self):
        return self._running
        
    def get_mouse_pos(self):
        return self._mousepos
        
    def override_all(self, suppress = False):
        radio.on_selection_changed = self._do_nothing
        self.on_frame_render = self._do_nothing
        self.on_user_quit = self._do_nothing
        
        if suppress:
            return
        print("Overrided all events")
        print("Notice that this includes:")
        print("  - on_user_quit")
        print("To remove this message, call window.override_all(suppress = True)")
        
    def _do_nothing(*args, **kwargs):
        pass

if __name__ == "__main__":
    print("TODO: example program")
    print("use `dir(pygui.window())` for now")


