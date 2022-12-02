# -*- coding: utf-8 -*-
"""
Created on Tue Oct 25 14:13:32 2022

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

class TestQueries:
    def test_existence(self):
        FORMULAS = [
            "∃x. film(x)",
            "∃x. actor(x)",
            "∃x. artist(x)",
            "∃x. director(x)",
            "exist x. ¬film(x) and ¬actor(x) and ¬director(x)"
            ]
        STR = [formula_parser(formula) for formula in FORMULAS]
        for fs in STR:
            for f in fs:
                assert f.eval(DB, {})
                
    def test_non_trivial(self):
        FORMULAS = [
            "forall x. film(x)",
            "forall x. actor(x)",
            "forall x. artist(x)",
            "forall x. director(x)",
            ]
        STR = [formula_parser(formula) for formula in FORMULAS]
        for fs in STR:
            for f in fs:
                assert not f.eval(DB, {})
    
    def test_completeness(self):
        FORMULAS = [
            "forall x. artist(x) or film(x)",
            "forall x. ¬artist(x) or ¬film(x)",
            ]
        STR = [formula_parser(formula) for formula in FORMULAS]
        for fs in STR:
            for f in fs:
                assert f.eval(DB, {})
                
    def test_q1(self):
        FORMULAS = [
            "forall x. film(x) or exist z. forall y.film(y) and director(z)",
            ]
        STR = [formula_parser(formula) for formula in FORMULAS]
        for fs in STR:
            for f in fs:
                assert not f.eval(DB, {})
                
    def test_q2(self):
        FORMULAS = [
            "forall x. (¬film(x) or exist y. artist(y) and (acts(y, x) or directs(y, x)))",
            ]
        STR = [formula_parser(formula) for formula in FORMULAS]
        for fs in STR:
            for f in fs:
                assert f.eval(DB, {})
    
    def test_q3(self):
        FORMULAS = [
            "forall x. exist y. acts(y, x) or acts(x, y) or directs(x, y) ",
            ]
        STR = [formula_parser(formula) for formula in FORMULAS]
        for fs in STR:
            for f in fs:
                assert not f.eval(DB, {})
                
    def test_q3(self):
        FORMULAS = [
            "forall x. (¬film(x) and artist(x)) or (film(x) and ¬artist(x))",
            ]
        STR = [formula_parser(formula) for formula in FORMULAS]
        for fs in STR:
            for f in fs:
                assert f.eval(DB, {})
                
    def test_q4(self):
        FORMULAS = [
            "exist x. acts('Novak Kim', x)",
            "exist x. acts(x, 'Vertigo')",
            "exist x. directs('Hitchcock Alfred', x)",
            "exist x. directs(x, 'Vertigo')"
            ]
        STR = [formula_parser(formula) for formula in FORMULAS]
        for fs in STR:
            for f in fs:
                assert f.eval(DB, {})  
                
    def test_q5(self):
        FORMULAS = [
            "exist x. exist y. acts(x, y) and directs(x, y)",
            "exist x. acts('Stewart James', x) and acts('Novak Kim', x)",
            ]
        
        STR = [formula_parser(formula) for formula in FORMULAS]
        for fs in STR:  
            for f in fs:
                assert f.eval(DB, {}) 
                
    
        
        