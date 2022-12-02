# -*- coding: utf-8 -*-
"""
Created on Tue Oct 25 16:02:49 2022

@author: Julien
"""

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
from src.eval_methods.evalVisitor import Visitor
from src.utils.fo_parser import formula_parser
from src.eval_methods.evalPatternMatching import eval_pattern_matching


STR = [formula_parser(formula) for formula in FORMULAS]
        
class TestEvals:
    # We will compare the execution of the different eval methods.
    
    def test_pattern_vs_visitor(self):
        V = Visitor(DB, {})
        for fs in STR:
            for f in fs:
                assert eval_pattern_matching(f, DB, {}) == V(f)
                
    def test_eval_vs_visitor(self):
        V = Visitor(DB, {})
        for fs in STR:
            for f in fs:
                assert f.eval(DB, {}) == V(f)
                
    def test_pattern_vs_eval(self):
        for fs in STR:
            for f in fs:
                assert f.eval(DB, {}) == eval_pattern_matching(f, DB, {})