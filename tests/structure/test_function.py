# -*- coding: utf-8 -*-
"""
Created on Tue Oct 11 16:31:56 2022

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

from src.structure.function import Function

class TestFunction:
    def test_init(self):
        F = Function('My Function', lambda t: t)
        
        assert F.name == "My Function"
        assert F(10) == 10
    
    def test_max(self):
        F = Function('Max', lambda t: max(t))
        
        assert F.name == "Max"
        assert F((1,2,3)) == 3