# -*- coding: utf-8 -*-
"""
Created on Mon Oct 17 15:08:34 2022

@author: Julien

"""

# EXTERNAL LIBRARIES

import sys
from pathlib import Path
import os

# INTERNAL IMPORTS

sys.path.append(Path(os.path.realpath(__file__)).parent.parent)   
from src.evaluables.binaryop import *
from src.evaluables.binarypred import *
from src.evaluables.constant import *
from src.evaluables.neg import *
from src.evaluables.quantified import *
from src.evaluables.unarypred import *
from src.evaluables.variable import *
from src.errors import *

class Visitor:
    def __init__(self, model, env) -> None:
        self.model = model
        self.env = env
        
    def __call__(self, formula):
        match formula:
            case Quantified(Quantifier.FORALL, v, f): return self.visit_quantifier_forall(v, f)
            case Quantified(Quantifier.EXISTS, v, f): return self.visit_quantifier_exists(v, f)
            case BinaryOp(Binop.AND, f1, f2): return self.visit_binaryop_and(f1, f2)
            case BinaryOp(Binop.OR, f1, f2): return self.visit_binaryop_or(f1, f2)
            case Neg(f): return self.visit_neg(f)
            case UnaryPred(UPred.ACTOR, t): return self.visit_unarypred_actor(t)
            case UnaryPred(UPred.DIRECTOR, t): return self.visit_unarypred_director(t)
            case UnaryPred(UPred.FILM, t): return self.visit_unarypred_film(t)
            case UnaryPred(UPred.ARTIST, t): return self.visit_unarypred_artist(t)
            case BinaryPred(BPred.ACTS, t1, t2): return self.visit_binarypred_acts(t1, t2)
            case BinaryPred(BPred.DIRECTS, t1, t2): return self.visit_binarypred_directs(t1, t2)
            case BinaryPred(BPred.EQ, t1, t2): self.visit_binarypred_eq(t1, t2)
            case Variable(v): return self.visit_variable(v)
            case Constant(v): return self.visit_constant(v)
            case _: raise FormulaError(formula, 'Case not found')
            
    def visit_quantifier_forall(self, v, f):
        env_var = self.env.get(v)
        res = True
        for x in self.model.get_domain():
            self.env[v] = x
            res = res and self(f)
            
            if res != True: break
            
        self.env[v] = env_var
        return res
    
    def visit_quantifier_exists(self, v, f):
        env_var = self.env.get(v)
        res = False
        for x in self.model.get_domain():
            self.env[v] = x
            res = res or self(f)
            
            if res == True: break
            
        self.env[v] = env_var
        return res
    
    def visit_binaryop_or(self, f1, f2):
        return self(f1) or self(f2)
    
    def visit_binaryop_and(self, f1, f2):
        return self(f1) and self(f2)
    
    def visit_neg(self, f):
        return not self(f)
    
    def visit_unarypred_actor(self, t):
        return self.model.is_actor(self(t))
    
    def visit_unarypred_director(self, t):
        return self.model.is_director(self(t))
    
    def visit_unarypred_film(self, t):
        return self.model.is_film(self(t))
    
    def visit_unarypred_artist(self, t):
        return self.model.is_artist(self(t))
    
    def visit_binarypred_acts(self, t1, t2):
        return self.model.acts_in(self(t1), self(t2))
    
    def visit_binarypred_directs(self, t1, t2):
        return self.model.directs(self(t1), self(t2))
    
    def visit_binarypred_eq(self, t1, t2):
        return self(t1) == self(t2)
    
    def visit_variable(self, v):
        return self.env.get(v)
    
    def visit_constant(self, v):
        return v
    

    