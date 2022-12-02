# -*- coding: utf-8 -*-
"""
Created on Tue Oct  4 17:04:42 2022

@author: Julien
"""

# EXTERNAL LIBRARIES

import sys
from pathlib import Path
import os

# INTERNAL IMPORTS 

sys.path.append(Path(os.path.realpath(__file__)).parent.parent)   

from src.structure.database import DataBase

class FilmDataBase(DataBase):
    def __init__(self, name, list_of_tables, functions_to_index = []):
        super().__init__(name, list_of_tables)
        
        self.indexes = {}
        self._index_actors()
        self._index_films()
        self._index_directors()
        self._index_artists()
        self._index_acts_in()
        self._index_directs()
        
    def _index_actors(self):
        self.indexes['is_actor'] = dict(zip(self.tables['Actors'].data, [True]*len(self.tables['Actors'].data)))
        
    def _index_films(self):
        self.indexes['is_film'] = dict(zip(self.tables['Films'].data, [True]*len(self.tables['Films'].data)))

    def _index_directors(self):
        self.indexes['is_director'] = dict(zip(self.tables['Directors'].data, [True]*len(self.tables['Directors'].data)))

            
    def _index_artists(self):
        self.indexes['is_artist'] = dict(zip(self.tables['Artists'].data, [True]*len(self.tables['Artists'].data)))

            
    def _index_acts_in(self):
        self.indexes['acts_in'] = dict(zip(self.tables['Acts'].data, [True]*len(self.tables['Acts'].data)))

            
    def _index_directs(self):
        self.indexes['Directs'] = dict(zip(self.tables['Directs'].data, [True]*len(self.tables['Directs'].data)))

            
    def get_domain(self):
        return self.tables['Domain'].data
    
    def is_actor(self, x) -> bool:
        if 'is_actor' in self.indexes:
            return self.indexes['is_actor'].get(x) or False
        else:
            return x in self.tables['Actors'].data
    
    def is_artist(self, x) -> bool:
        if 'is_artist' in self.indexes:
            return self.indexes['is_artist'].get(x) or False
        else:
            return x in self.tables['Artists'].data
    
    def is_director(self, x) -> bool:
        if 'is_director' in self.indexes:
            return self.indexes['is_director'].get(x) or False
        else:
            return x in self.tables['Directors'].data
    
    def is_film(self, x) -> bool:
        if 'is_film' in self.indexes:
            return self.indexes['is_film'].get(x) or False
        else:
            return x in self.tables['Films'].data
    
    def acts_in(self, x, y) -> bool:
        if 'acts_in' in self.indexes:
            return self.indexes['acts_in'].get((x, y)) or False
        else:
            return (x, y) in self.tables['Acts'].data
    
    def directs(self, x, y) -> bool:
        if 'directs' in self.indexes:
            return self.indexes['directs'].get((x, y)) or False
        else:
            return (x, y) in self.tables['Directs'].data
        