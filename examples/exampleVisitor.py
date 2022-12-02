# EXTERNAL LIBRARIES

import sys
import os
from pathlib import Path

# INTERNAL IMPORTS
      
sys.path.append(Path(os.path.realpath(__file__)).parent.parent)

from src.utils.fo_parser import formula_parser
from src.eval_methods.evalVisitor import Visitor
from examples.exampleFilmDatabase import DB
from examples.exampleFormulas import FORMULAS

STR = [formula_parser(formula) for formula in FORMULAS]

V = Visitor(DB, {})

for fs, f_string in zip(STR, FORMULAS):
    for f in fs:
        print(f'{f_string} -> {V(f)}')
