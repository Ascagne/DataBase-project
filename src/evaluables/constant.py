# -*- coding: utf-8 -*-
"""
Created on Tue Oct 25 11:08:19 2022

@author: Julien
"""

from .evaluable import Evaluable

class Constant(Evaluable):
    __match_args__ = ('value',)

    def __init__(self, val):
        self.value = val
        
    def get_value(self):
        return self.value

    def eval(self, model, env):
        return self.value
        # self.value = self.value.replace("\\", "\\\\")
        # if "'" not in self.value:
        #     return f"'{self.value}'"
        # else:
        #     self.value = self.value.replace("\"", "\\\"")
        #     return f"\"{self.value}\"" 

    