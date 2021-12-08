# WARNING: method update() is unsafe
# compound expression formed with current expression cannot be used to update
# the current expression; as these will cause infinite loops

# example 1: updating E1 with E2; where E2 =  E1 + 1
# example 2: updating E1 with E2; where E2 = E3 + 1 but  E3 = E1 + 1

import warnings

class E:
    """
    E denotes Expression, and evaluates to a scalar (can be `int`, `float`)\n
    can be used to create expressions out of scalars and/or other `E`s\n
    compund `E` values are reflected when its dependant `E`s values are changed
    """
    def __init__(self, val=None):
        """creates a Expression from a given scalar (int/float)"""
        self._val = None
        self._type = None
        self.children = None
        
        if isinstance(val, (int, float)):
            self._val = val
            self._type = 'scalar'

        # prevent double wrapping.
        elif isinstance(val, E):
            raise Exception(f"initial value: {val} is already an E")

        elif val is not None:
            raise Exception(f"unsupported initial value: {val}")

        
    def set(self, val):
        """
        assigns the given scalar value to  `E` 
        (only applicable if `E` is of scalar type) \n
        """
        if self._type != 'scalar':
            raise Exception('only scalars support set()')
        self._val = val

    @property
    def val(self):
        """get the evaluated value of `E`"""
        
        if self._type == 'scalar':
            return  self._val
        
        elif self._type == 'sum':
            return E.get_sum(self.children)

        elif self._type == 'sub':
            return E.get_sub(self.children)

        elif self._type == 'mul':
            return E.get_mul(self.children)
        
        elif self._type == 'div':
            return E.get_div(self.children)
        
        else:
            raise Exception(f'invalid V type: {self._type}')
        



    @classmethod
    def get_sum(cls, args):
        """get the evaluated sum of all `E`s"""
        return sum(map(lambda arg: arg.val, args))
    
    @classmethod
    def get_sub(clas, args):
        """get the evaluated difference of two `E`s"""
        if len(args) != 2:
            Exception('get_sub() requires a list of exactly 2 Vs')
        return args[0].val - args[1].val

    @classmethod
    def get_mul(cls, args):
        """get the evaluated product of all `E`s"""
        val = 1
        for arg in args:
            val *= arg.val
        return val

    @classmethod
    def get_div(cls, args):
        """get the evaluated division of two `E`s"""
        if len(args) != 2:
            Exception('get_div() requires a list of exactly 2 Vs')
        return args[0].val / args[1].val



    @classmethod
    def _op(cls, type, args):
        op_val = E()
        op_val._type = type
        op_val.children = []
        for arg in args:
            if isinstance(arg, E):
                op_val.children.append(arg)
            elif isinstance(arg, (int, float)):
                op_val.children.append(E(arg))

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
    def div(cls, *args):
        return cls._op('div', args)


    # useful operator overloads.
    def __add__(self, other):
        return E.sum(self, other)

    def __sub__(self, other):
        return E.sub(self, other)
        
    def __mul__(self, other):
        return E.mul(self, other)
        
    def __truediv__(self, other):
        return E.div(self, other)

        
    def __str__(self):
            return str(self.val)


    def update(self, e):
        """updates `E` to a new `E`"""
        warnings.warn('self@E.update() is dangerous. make sure to use deepcopy\n\
            to get around example 1. and dont do example 2 in the first place\n\
            refer compute.py for examples')
        self._type = e.type
        self._val = e.val


    def eq(self):
        if self._type == 'scalar':
            return str(self._val)
        
        if self._type == 'sum':
            return '(' + ' + '.join([child.eq() for child in self.children])  + ')'
        if self._type == 'sub':
            return '(' + ' + '.join([child.eq() for child in self.children])  + ')'
        if self._type == 'mul':
            return '(' + ' * '.join([child.eq() for child in self.children])  + ')'
        if self._type == 'div':
            return '(' + ' / '.join([child.eq() for child in self.children])  + ')'


