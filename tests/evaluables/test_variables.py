# -*- coding: utf-8 -*-
"""
Created on Thu Dec  1 23:19:58 2022

@author: Julien
"""

# EXTERNAL LIBRARIES

import sys
from pathlib import Path
import os
import yaml

# INTERNAL IMPORTS

CONFIG_FILE = Path(os.path.realpath(__file__)).parent.parent.parent / 'etc/config.yml'

with open(CONFIG_FILE) as file:
    try:
        config = yaml.safe_load(file)
    except yaml.YAMLError as exc:
        print(exc)
        config = {}
        
sys.path.append(config.get('ROOT_DIR'))  

from src.utils.fo_parser import formula_parser
from examples.exampleFilmDatabase import DB

class TestVariables:
    def test_q1(self):
        FORMULAS = [
            "∃x. acts(x, y)",
            ]
        
        STR = [formula_parser(formula) for formula in FORMULAS]
        for fs in STR:  
            for f in fs:
                assert not f.eval(DB, {}) 