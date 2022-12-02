# -*- coding: utf-8 -*-
"""
Created on Tue Oct 11 16:41:36 2022

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

from src.structure.table import Table
from examples.exampleFunctions import FUNCTIONS

class TestTable:
    def test_init(self):
        T = Table('My Table', [(1,2),(3,4), (5,6)])
        
        assert T.name == 'My Table'
        assert T.data == [(1,2),(3,4), (5,6)]
        assert T.functions == []
        assert T.functions_to_index == []
        assert T.indexes == {}
        
    def test_indexing(self):
        T = Table('My Table', [(1,2),(2,-7), (0,0)], FUNCTIONS, ['Max'])
        
        assert T.indexes['Max'] == {
            2:[(1, 2), (2, -7)],
            0:[(0, 0)]
            }
        
    def test_sequential_search_(self):
        T = Table('My Table', [(1,2),(2,-7), (0,0)], FUNCTIONS, ['Max'])
        
        assert T._sequential_search('Sum', -5) == [(2, -7)]
        assert T._sequential_search('First Value', 0) == [(0, 0)]
        
    def test_smart_search(self):
        T = Table('My Table', [(1,2),(2,-7), (0,0)], FUNCTIONS, ['Sum', 'Max'])
        
        assert T._sequential_search('Sum', -5) == T._smart_search('Sum', -5)
        assert T._sequential_search('Sum', 4) == T._smart_search('Sum', 4)
        assert T._sequential_search('Min', -5) == T._smart_search('Min', -5)
        assert T._sequential_search('Min', -7) == T._smart_search('Min', -7)
        
    def test_conditional_search(self):
        T = Table('My Table', [(4,2),(2,-7), (0,0), (4,4), (4, -3), (5, 8)], FUNCTIONS, ['Sum', 'Max'])
        
        assert T._conditional_search(['Max', 'First Value'], [4, 4]) == [(4, 2), (4, 4), (4, -3)]
        
        
        