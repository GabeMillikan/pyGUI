import random
import math

_changing_h = 0
class color:
    global color
    # grayscale
    def white(): return         color(255, 255, 255);
    def lightgray(): return     color(200, 200, 200)
    def gray(): return          color(127, 127, 127)
    def darkgray(): return      color(50 , 50 , 50 )
    def black(): return         color(0  , 0  , 0  )
    # solids
    def red(): return           color(255, 0  , 0  )
    def green(): return         color(0  , 255, 0  )
    def blue(): return          color(0  , 0  , 255)
    # soft solids
    def softred(): return       color(255, 100, 100)
    def softgreen(): return     color(100, 255, 100)
    def softblue(): return      color(100, 100, 255)
    # dark solids
    def darkred(): return       color(127, 0  , 0  )
    def darkgreen(): return     color(0  , 127, 0  )
    def darkblue(): return      color(0  , 0  , 127)
    # rainbow
    #todo
    
    #creation
    def __init__(self,r,g,b):
        self.value = (r,g,b)
        
    def __getitem__(self, i):
        return self.value[i]
        
    def __setitem__(self, i, val):
        assert (isinstance(val, int) or isinstance(val, float)), "mtuple only accepts ints/floats"
        self.value = list(self.value)
        self.value[i] = val
        self.value = tuple(self.value) #lol
        
    def tuple(self):
        return self.value
        
    def inplace_round(self):
        self.value = (int(round(self.value[0])), int(round(self.value[1])), int(round(self.value[2])))
        
    def rounded(self):
        new = color(0,0,0)
        new.value = self.value
        new.inplace_round()
        return new
        
    def __str__(self):  
        return str(self.value)
        
    def random():
        x = str(random.random()).split(".")[-1]
        _1 = int(round(int(x[ :3])*255/999))
        _2 = int(round(int(x[3:6])*255/999))
        _3 = int(round(int(x[6:9])*255/999))
        return color(_1, _2, _3)
        
    def hsv_to_rgb(hsv):
        h,s,v = hsv
        h /= 360
        s /= 100
        v /= 100
        
        i = math.floor(h*6)
        f = h*6 - i
        p = v*(1-s)
        q = v*(1-f*s)
        t = v*(1-(1-f)*s)
        i = i % 6
        
        if   i == 0:
            return color(int(round(v*255)),int(round(t*255)),int(round(p*255)))
        elif i == 1:
            return color(int(round(q*255)),int(round(v*255)),int(round(p*255)))
        elif i == 2:
            return color(int(round(p*255)),int(round(v*255)),int(round(t*255)))
        elif i == 3:
            return color(int(round(p*255)),int(round(q*255)),int(round(v*255)))
        elif i == 4:
            return color(int(round(t*255)),int(round(p*255)),int(round(v*255)))
        elif i == 5:
            return color(int(round(v*255)),int(round(p*255)),int(round(q*255)))
            
    def rainbow(speed = 0.1):
        global _changing_h
        _changing_h += speed
        return color.hsv_to_rgb(color(_changing_h, 100, 100))
        
        
        