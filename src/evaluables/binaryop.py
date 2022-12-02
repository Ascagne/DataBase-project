# -*- coding: utf-8 -*-
"""
Created on Tue Oct 25 11:05:54 2022

@author: Julien
"""

from enum import Enum
from .evaluable import Evaluable

class Binop(Enum):
    OR = 1
    AND = 2

class BinaryOp(Evaluable):
    __match_args__ = ('op', 'left', 'right')

    def __init__(self, op, f1, f2):
        self.op = op
        self.left = f1
        self.right = f2

    def get_op(self):
        return self.op

    def get_left(self):
        return self.left

    def get_right(self):
        return self.right

    def eval(self, model, env):
        match self.get_op():
            case Binop.OR: 
                return self.get_left().eval(model, env) | self.get_right().eval(model, env)
            case Binop.AND:
                return self.get_left().eval(model, env) & self.get_right().eval(model, env)