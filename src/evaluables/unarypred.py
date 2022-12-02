# -*- coding: utf-8 -*-
"""
Created on Tue Oct 25 11:06:48 2022

@author: Julien
"""

from enum import Enum
from .evaluable import Evaluable

class UPred(Enum):
    ACTOR = 1
    FILM = 2
    ARTIST = 3
    DIRECTOR = 4

class UnaryPred(Evaluable):
    __match_args__ = ('predicate', 'arg')

    def __init__(self, pred, t):
        self.predicate = pred
        self.arg = t

    def get_predicate(self):
        return self.predicate

    def get_arg(self):
        return self.arg

    def eval(self, model, env):
        v = self.get_arg().eval(model, env)
        match self.predicate:
            case UPred.ACTOR: return model.is_actor(v) # is v in the table Actor of the model
            case UPred.FILM: return model.is_film(v)
            case UPred.ARTIST: return model.is_artist(v)
            case UPred.DIRECTOR: return model.is_director(v)