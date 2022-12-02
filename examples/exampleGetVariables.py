# -*- coding: utf-8 -*-

# EXTERNAL LIBRARIES

import sys
import os
from pathlib import Path

# INTERNAL IMPORTS
      
sys.path.append(Path(os.path.realpath(__file__)).parent.parent)

from examples.exampleFormulas import FORMULAS
from src.getVariables import getVariables
from src.utils.fo_parser import formula_parser

STR = [formula_parser(formula) for formula in FORMULAS]

for (fs, formula) in zip(STR, FORMULAS):
    for f in fs:
        free_var, bound_var = getVariables(f)
        print(formula)
        print(f'Free variables: {free_var}')
        print(f'Bound variables: {bound_var}\n')
    
