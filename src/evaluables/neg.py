# -*- coding: utf-8 -*-
"""
Created on Tue Oct 25 11:10:36 2022

@author: Julien
"""

from .evaluable import Evaluable

class Neg(Evaluable):
    __match_args__ = ('formula',)
    def __init__(self, f):
        self.formula = f
        
    def get_formula(self):
        return self.formula

    def eval(self, model, env):
        return not self.get_formula().eval(model, env)

    