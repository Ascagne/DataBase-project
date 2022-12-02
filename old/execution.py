# -*- coding: utf-8 -*-
"""
Created on Tue Oct 25 13:36:19 2022

@author: Julien
"""

# from fo_formulas import *
from src.fo_parser import formula_parser
from create_db_from_file import DB
from src.visitor import Visitor


FORMULAS = ["∃ys. film(ys)",\
            "forall x. film(x) or artist(x)",
            "forall x. film(x) or exist z. forall y.film(y) and director(z)",
            # "acts('O\\\'Hara Maureen', x)",
            ]

def eval_formula(f):
    return(f.eval(DB, {}))


    
def visitor_pattern(f):
    pass
    #Idem mais on met le code dans une seule classe
    


STR = [formula_parser(formula) for formula in FORMULAS]
V = Visitor(DB, {})

for fs in STR:
    for f in fs:
        print(f'Query : {formula_to_string(f)}')
        print(f' - Built-in eval : {f.eval(DB, {})}')
        print(f' - Function eval : {eval_formula_v2(f,DB, {})}')
        print(f' - Visitor eval : {V(f)}')
        print('\n')
