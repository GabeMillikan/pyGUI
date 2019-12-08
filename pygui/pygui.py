import threading
import time
from pygui.guiprofile import guiprofile
from pygui.color import color

class window:
    def __init__(self, suppress = False):
        if not suppress:
            print("Created window!")
            print("Note that only ONE window can be created per python instance running")
            print("To hide this message, create window(suppress = True)")
        """
            setup variables
        """
        self._running = True
        self.loaded = False
        self.profile = guiprofile() #will spawn with defaults
        
        """
            begin program
        """
        self._main_thread = threading.Thread(target = self._disp_thread)
        self._main_thread.start()
        
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
        
    def _quit_event(self):
        try:
            self.on_user_quit()
        except Exception as e:
            print("Error when calling window.on_user_quit():\n  " + str(e.__class__.__name__) + " : " + str(e))
        
    def _disp_thread(self):
        global _GLOBAL
        
        #get pygame
        import sys,io
        outputtrap = io.StringIO()
        sys.stdout = outputtrap
        import pygame
        pygame.init()
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
        
        self.background = pygame.display.set_mode(self.profile.size)
        clock = pygame.time.Clock()
        recorded_fps = [self.profile.fps for i in range(self.profile.measure_fps_over_framecount)]
        while self._running:
            '''
                timer for recording fps
            '''
            fbegin = time.monotonic()
            
            '''
                call on_frame_render
                    - parameter is the average observed framerate
            '''
            observed_fps = sum(recorded_fps)/(len(recorded_fps))
            try:
                self.on_frame_render(observed_fps)
            except Exception as e:
                print("\nError when calling window.on_frame_render(" + str(observed_fps) + "):\n  " + str(e.__class__.__name__) + " : " + str(e))
                
            '''
                event handling
            '''
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    threading.Thread(target = self._quit_event).start()
                
            '''
                update frame settings
            '''
            currentsize = pygame.display.get_surface().get_size()
            if not (currentsize[0] == self.profile.size[0] and currentsize[1] == self.profile.size[1]):
                self.background = pygame.display.set_mode(self.profile.size)
                
            '''
                Draw frame
            '''
            self.background.fill(self.profile.background_color)
            
            '''
                Put frame on screen
            '''
            pygame.display.update()
            
            '''
                tick the clock
                adjust tick time to attempt to reach true framerate
                    - if observed < profile.fps, increase clocktick: positive adjustment
                    - if observed > profile.fps, decrease clocktick: negative adjustment
                    - adjustment = profile.fps - observed
                    - clocktick = profile.fps + adjustment
                    - clocktick = profile.fps + profile.fps - observed
                    - clocktick = 2(profile.fps) - observed
            '''
            clock.tick((2*self.profile.fps) - observed_fps)
            
            framerate = time.monotonic()-fbegin
            framerate = 99999 if framerate < 0.0001 else 1/framerate
            recorded_fps.insert(0, framerate)
            recorded_fps.pop()
        pygame.quit()
        return
        
    def set_fps(self, value):
        self.profile.fps = value
        
    def set_background_color(self, clr):
        self.profile.background_color = clr
    
    def set_size(self, size):
        self.profile.size = size
        
    def override_all(self, suppress = False):
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


