# -*- coding: utf-8 -*-
"""
Created on Tue Oct 25 12:00:11 2022

@author: Julien
"""

from .evaluable import Evaluable
from enum import Enum

class BPred(Enum):
    EQ = 1
    ACTS = 2
    DIRECTS = 3


class BinaryPred(Evaluable):
    __match_args__ = ('predicate', 'arg1', 'arg2')

    def __init__(self, pred, t1, t2):
        self.predicate = pred
        self.arg1 = t1
        self.arg2 = t2

    def get_predicate(self):
        return self.predicate

    def get_arg1(self):
        return self.arg1

    def get_arg2(self):
        return self.arg2

    def eval(self, model, env):
        v1 = self.get_arg1().eval(model, env)
        v2 = self.get_arg2().eval(model, env)
        
        match self.get_predicate():
            case BPred.EQ: return v1 == v2
            case BPred.ACTS: return model.acts_in(v1, v2)
            case BPred.DIRECTS: return model.directs(v1, v2)