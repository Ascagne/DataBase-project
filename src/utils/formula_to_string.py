# -*- coding: utf-8 -*-
"""
Created on Tue Oct 25 16:04:52 2022

@author: Julien
"""

# EXTERNAL LIBRARIES

import sys
from pathlib import Path
import os
# import the module where you define the classes that implement the structure of first order logic formulae

# INTERNAL IMPORTS

sys.path.append(Path(os.path.realpath(__file__)).parent.parent)   

from src.evaluables.binaryop import *
from src.evaluables.binarypred import *
from src.evaluables.constant import *
from src.evaluables.neg import *
from src.evaluables.quantified import *
from src.evaluables.unarypred import *
from src.evaluables.variable import *

def formula_to_string(f):
    match f:
        case BinaryOp(Binop.AND, f1, f2): return f"({formula_to_string(f1)} ∧ {formula_to_string(f2)})"
        case BinaryOp(Binop.OR, f1, f2): return f"({formula_to_string(f1)} ∨ {formula_to_string(f2)})"
        case Neg(f): return f"¬{formula_to_string(f)}"
        case Quantified(Quantifier.FORALL, v, f): return f"(∀ {v}. {formula_to_string(f)})"
        case Quantified(Quantifier.EXISTS, v, f): return f"(∃ {v}. {formula_to_string(f)})"
        case UnaryPred(UPred.ACTOR, t): return f"actor({formula_to_string(t)})"
        case UnaryPred(UPred.DIRECTOR, t): return f"director({formula_to_string(t)})"
        case UnaryPred(UPred.FILM, t): return f"film({formula_to_string(t)})"
        case UnaryPred(UPred.ARTIST, t): return f"artist({formula_to_string(t)})"
        case BinaryPred(BPred.ACTS, t1, t2): return f"acts({formula_to_string(t1)}, {formula_to_string(t2)})"
        case BinaryPred(BPred.DIRECTS, t1, t2): return f"directs({formula_to_string(t1)}, {formula_to_string(t2)})"
        case BinaryPred(BPred.EQ, t1, t2): return f"{formula_to_string(t1)} = {formula_to_string(t2)}"
        case Variable(v): return v
        case Constant(v):
            v = v.replace("\\", "\\\\")
            if "'" not in v:
                return f"'{v}'"
            else:
                v = v.replace("\"", "\\\"")
                return f"\"{v}\""
            
        case _:
            return 'Error'