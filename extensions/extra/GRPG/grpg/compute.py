class V:
    def __init__(self, val=None):
        """creates a V(alue) from a scalar."""
        self.val = None
        self.type = None
        self.children = None
        
        if isinstance(val, (int, float)):
            self.val = val
            self.type = 'constant'

        
    def set(self, val):
        """
        assigns the given scalar value to  `V` 
        (only applicable if `V` is of constant type)
        """
        if self.type != 'constant':
            raise Exception('only constants support set()')
        self.val = val


    def get(self):
        """get the evaluated value of V"""
        
        if self.type == 'constant':
            return  self.val
        
        elif self.type == 'sum':
            return V.get_sum(self.children)

        elif self.type == 'sub':
            return V.get_sub(self.children)

        elif self.type == 'mul':
            return V.get_mul(self.children)
        
        elif self.type == 'div':
            return V.get_div(self.children)
        
        else:
            raise Exception(f'invalid V type: {self.type}')
        



    @classmethod
    def get_sum(cls, args):
        """get the evaluated sum of all Vs"""
        return sum(map(lambda arg: arg.get(), args))
    
    @classmethod
    def get_sub(clas, args):
        """get the evaluated difference of two Vs"""
        if len(args) != 2:
            Exception('get_sub() requires a list of exactly 2 Vs')
        return args[0].get() - args[1].get()

    @classmethod
    def get_mul(cls, args):
        """get the evaluated product of all Vs"""
        val = 1
        for arg in args:
            val *= arg.get()
        return val

    @classmethod
    def get_div(cls, args):
        """get the evaluated division of two Vs"""
        if len(args) != 2:
            Exception('get_div() requires a list of exactly 2 Vs')
        return args[0].get() / args[1].get()



    @classmethod
    def _op(cls, type, args):
        op_val = V()
        op_val.type = type
        op_val.children = []
        for arg in args:
            if isinstance(arg, V):
                op_val.children.append(arg)
        return op_val 

    @classmethod
    def sum(cls, *args):
        return cls._op('sum', args)
    @classmethod
    def sub(cls, *args):
        return cls._op('sub', args)
    @classmethod
    def mul(cls, *args):
        return cls._op('mul', args)
    @classmethod
    def sub(cls, *args):
        return cls._op('div', args)



    def __add__(self, other):
        if isinstance(other, (int, float)):
            other = V(other)
        return V.sum(self, other)

    def __sub__(self, other):
        if isinstance(other, (int, float)):
            other = V(other)
        return V.sub(self, other)
        
    def __mul__(self, other):
        if isinstance(other, (int, float)):
            other = V(other)
        return V.mul(self, other)
        
    def __truediv__(self, other):
        if isinstance(other, (int, float)):
            other = V(other)
        return V.div(self, other)
        
    def __str__(self):
            return str(self.get())


def v(v: V):
    return v.get()