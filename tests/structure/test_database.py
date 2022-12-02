# -*- coding: utf-8 -*-
"""
Created on Fri Oct 14 09:41:10 2022

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

from src.structure.database import DataBase
from examples.exampleTables import T1, T2

class TestDataBase:        
    def test_init(self):
        db = DataBase('My database', [T1, T2])
        n1 = T1.name
        n2 = T2.name
        
        assert db.name == 'My database'
        assert n1 in db.tables and n2 in db.tables
        assert T1 == db.tables[n1] and T2 == db.tables[n2]
        
    def test_join_naive(self):
        db = DataBase('My database', [T1, T2])
        
        n1 = T1.name
        n2 = T2.name
        
        list_f = ['Min', 'First Value']
        list_g = ['Second Value', 'Max']
        
        assert db._join_naive(
            n1, n2, list_f, list_g
            ).sort() == db._join_naive_improved(
                n1, n2, list_f, list_g
                ).sort()
                
    def test_join_from_indexes(self):
        db = DataBase('My database', [T1, T2])
        
        n1 = T1.name
        n2 = T2.name
        
        list_f = ['Min', 'First Value']
        list_g = ['Second Value', 'Max']
        
        assert db._join_naive_improved(
            n1, n2, list_f, list_g
            ).sort() == db._join_from_indexes(
                n1, n2, list_f, list_g
                ).sort()
    
    def test_join_from_keys(self):
        db = DataBase('My database', [T1, T2])
        
        n1 = T1.name
        n2 = T2.name
        
        list_f = ['Min', 'First Value']
        list_g = ['Second Value', 'Max']
        
        assert db._join_naive_improved(
            n1, n2, list_f, list_g
            ).sort() == db._join_from_keys(
                n1, n2, list_f, list_g
                ).sort()
                
    def test_new_table(self):
        db = DataBase('My database', [T1])
        
        db.create_new_table(T2.name, T2.data, T2.functions, T2.functions_to_index)
        
        assert T2.name in db.tables
        assert db.tables[T2.name].data == T2.data
        assert db.tables[T2.name].functions == T2.functions
        assert db.tables[T2.name].functions_to_index == T2.functions_to_index