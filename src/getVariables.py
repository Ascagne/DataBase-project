# -*- coding: utf-8 -*-

# EXTERNAL LIBRARIES

import sys
from pathlib import Path
import os
import yaml
# INTERNAL IMPORTS

CONFIG_FILE = Path(os.path.realpath(__file__)).parent.parent / 'etc/config.yml'

with open(CONFIG_FILE) as file:
    try:
        config = yaml.safe_load(file)
    except yaml.YAMLError as exc:
        print(exc)
        config = {}
        
sys.path.append(config.get('ROOT_DIR'))

from src.evaluables.binaryop import *
from src.evaluables.binarypred import *
from src.evaluables.constant import *
from src.evaluables.neg import *
from src.evaluables.quantified import *
from src.evaluables.unarypred import *
from src.evaluables.variable import *
from src.errors.formula_error import FormulaError

def computeVariables(f, all_var:set, quantified_var:set, bound_var:set):
    match f:
        case BinaryOp(binop, f1, f2):
            a1, q1, b1 = computeVariables(f1, all_var, quantified_var, bound_var) 
            a2, q2, b2 = computeVariables(f2, all_var, quantified_var, bound_var)
            return set(a1) | set(a2), set(q1) | set(q2), set(b1) | set(b2)
        
        case Quantified(quantifier, v, f): 
            quantified_var = quantified_var | set([v.value]) 
            all_var = all_var | set([v.value]) 
            return computeVariables(f, all_var, quantified_var, bound_var)
        
        case BinaryPred(pred, t1, t2):
            match t1:
                case Variable(v): 
                    bound_var = bound_var | set([v.value])
                    all_var = all_var | set([v.value])
                case Constant(v): pass
                case _: raise FormulaError(t, 'Case not found')
                    
            match t2:
                case Variable(v): 
                    bound_var = bound_var | set([v.value])
                    all_var = all_var | set([v.value])
                case Constant(v): pass
                case _: raise FormulaError(t, 'Case not found')
                
            return all_var, quantified_var, bound_var
        
        case Variable(v): 
            all_var = all_var | set([v.value])
            return all_var, quantified_var, bound_var
        
        case UnaryPred(pred, t): 
            match t:
                case Variable(v):
                    bound_var = bound_var | set([v.value])
                    all_var = all_var | set([v.value])
                    return all_var, quantified_var, bound_var
                
                case Constant(v):
                    pass
                case _:
                    raise FormulaError(t, 'Case not found')
                    
        case Constant(v): return all_var, quantified_var, bound_var
        case Neg(f): return computeVariables(f, all_var, quantified_var, bound_var)

        case _:
            raise FormulaError(formula, 'Case not found')
            
def getVariables(f):
    all_var, quantified_var, bound_var = computeVariables(f, set(), set(), set())
    free_var = all_var.difference(quantified_var)
    return list(free_var), list(bound_var)
        
       