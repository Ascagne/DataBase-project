# -*- coding: utf-8 -*-
"""
Created on Tue Oct 25 16:06:35 2022

@author: Julien
"""

import os
import sys
from pathlib import Path

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
        
def eval_pattern_matching(formula, model, env):
    match formula:
        case Quantified(Quantifier.FORALL, v, f): 
            env_var = env.get(v)
            res = all(eval_pattern_matching(f, model, formula.modify_env(env, x))  for x in model.get_domain())
            env[v] = env_var
            return res
        
        case Quantified(Quantifier.EXISTS, v, f): 
            env_var = env.get(v)
            res = any(eval_pattern_matching(f, model, formula.modify_env(env, x)) for x in model.get_domain())
            env[v] = env_var
            return res
        
        case BinaryOp(Binop.AND, f1, f2): return eval_pattern_matching(f1, model, env) and eval_pattern_matching(f2, model, env)
        case BinaryOp(Binop.OR, f1, f2): return eval_pattern_matching(f1, model, env) or eval_pattern_matching(f2, model, env)
        case Neg(f): return not eval_pattern_matching(f, model, env)
        case UnaryPred(UPred.ACTOR, t): return model.is_actor(eval_pattern_matching(t, model, env))
        case UnaryPred(UPred.DIRECTOR, t): return model.is_director(eval_pattern_matching(t, model, env))
        case UnaryPred(UPred.FILM, t): return model.is_film(eval_pattern_matching(t, model, env))
        case UnaryPred(UPred.ARTIST, t): return model.is_artist(eval_pattern_matching(t, model, env))
        case BinaryPred(BPred.ACTS, t1, t2): return model.acts_in(eval_pattern_matching(t1, model, env), eval_pattern_matching(t2, model, env))
        case BinaryPred(BPred.DIRECTS, t1, t2): return model.directs(eval_pattern_matching(t1, model, env), eval_pattern_matching(t2, model, env))
        case BinaryPred(BPred.EQ, t1, t2): return eval_pattern_matching(t1, model, env) == eval_pattern_matching(t2, model, env)
        case Variable(v): return env.get(v)
        case Constant(v): return v
        case _:
            raise FormulaError(formula, 'Case not found')
            