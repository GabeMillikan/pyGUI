class mtuple: # a tuple that can be be operated on
    def __init__(self, *args):
        if len(args) == 1:
            if isinstance(args[0], tuple):
                self.value = args[0]
                return
            elif isinstance(args[0], list):
                self.value = tuple(list)
                return
            elif isinstance(args[0], mtuple):
                self.value = args[0].value
                return
        self.value = tuple(args)
        
    def __getitem__(self, i):
        return self.value[i]
        
    def __setitem__(self, i, val):
        assert (isinstance(val, int) or isinstance(val, float)), "mtuple only accepts ints/floats"
        self.value = list(self.value)
        self.value[i] = val
        self.value = tuple(self.value) #lol
        
    def clone(self):
        new = mtuple(1)
        new.value = self.value
        return new
        
    def length(self):
        return sum([x**2 for x in self])**0.5
        
    def inplace_round(self):    
        for i in range(len(self)):
            self[i] = int(round(self[i]))
        
    def rounded(self):
        new = self.clone()
        new.inplace_round()
        return new
        
    def tuple(self):
        return self.value
        
    def __repr__(self):
        return str(self)
        
    def __str__(self):
        return str(self.value)
        
    def __len__(self):
        return len(self.value)
        
    def __add__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            new = self.clone()
            for i in range(len(new)):
                new[i] = new[i] + other
            return new
        elif isinstance(other, mtuple):
            new = self.clone()
            for i in range(len(self)):
                new[i] = self[i] + other[i]
            return new
        else:
            raise TypeError("mtuple addition doesnt support " + other.__class__.__name__)
            
    def __iadd__(self, other):
        self = self + other #goodluck trying to save memory
        return self
                
    def __truediv__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            new = self.clone()
            for i in range(len(new)):
                new[i] /= other
            return new
        elif isinstance(other, mtuple):
            new = self.clone()
            for i in range(len(new)):
                new[i]/=other[i]
            return new
        else:
            raise TypeError("mtuple division doesnt support " + other.__class__.__name__)
            
    def __itruediv__(self, other):
        self = self / other #lol
        return self
        
    def __mul__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            new = self.clone()
            for i in range(len(new)):
                new[i] *= other
            return new
        elif isinstance(other, mtuple):
            new = self.clone()
            for i in range(len(new)):
                new[i]*=other[i]
            return new
        else:
            raise TypeError("mtuple division doesnt support " + other.__class__.__name__)
        
    def __imul__(self, other):
        self = self * other #lol
        return self
        
    def __sub__(self, other):
        return self + (other * (-1))
        
    def __isub__(self, other):
        self = self - other
        return self