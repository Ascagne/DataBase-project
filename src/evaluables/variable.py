# -*- coding: utf-8 -*-
"""
Created on Tue Oct 25 11:07:58 2022

@author: Julien
"""

from .evaluable import Evaluable

class Variable(Evaluable):
    __match_args__ = ('name',)

    def __init__(self, name):
        self.name = name
        
    def get_name(self):
        return self.name

    def eval(self, model, env):
        return env.get(self.get_name())

    