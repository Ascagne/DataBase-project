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

from examples.exampleFormulas import FORMULAS
from examples.exampleFilmDatabase import DB
from src.getVariables import getVariables
from src.utils.fo_parser import formula_parser
        
STR = [formula_parser(formula) for formula in FORMULAS]

class TestComputeVariables:
    def test_bound_only(self):
        for fs in STR:
            for f in fs:
                free_var, bound_var = getVariables(f)
                assert free_var == []
                assert bound_var != []
    def test_free_and_bound(self):
        F = [
            "film(x)", 
            "actor(y)",
            "acts(someActor, someFilm)"
        ]
        STR = [formula_parser(formula) for formula in F]
        for fs in STR:
            for f in fs:
                free_var, bound_var = getVariables(f)
                free_var.sort()
                bound_var.sort()
                assert free_var == bound_var
                
    def test_x_is_free(self):
        F = [
            "forall y. film(y) or actor(x)",
            "exist someActor. exist someFilm. acts(someActor, someFilm) and directs(x, someFilm)"
        ]
        STR = [formula_parser(formula) for formula in F]
        for fs in STR:
            for f in fs:
                free_var, bound_var = getVariables(f)
                assert free_var == ['x']