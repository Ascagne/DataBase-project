# -*- coding: utf-8 -*-
"""
Created on Tue Oct  4 17:04:42 2022

@author: Julien
"""

# EXTERNAL LIBRARIES

import sys
import os
from pathlib import Path

# INTERNAL IMPORTS
      
sys.path.append(Path(os.path.realpath(__file__)).parent.parent)

from src.filmDatabase import FilmDataBase
from src.structure.table import Table
from src.structure.function import Function
from data.films import *

TABLE_ARTISTS = Table(
    data = [artist for artist in artists],
    name = "Artists",
    functions_to_index = []
    )

TABLE_FILMS = Table(
    data = [film for film in films],
    name = "Films",
    functions_to_index = []
    )

TABLE_ACTORS = Table(
    data = [actor for actor in actors],
    name = "Actors",
    functions_to_index = []
    )

TABLE_DIRECTORS = Table(
    data = [director for director in directors],
    name = "Directors",
    functions_to_index = []
    )

TABLE_ACTS = Table(
    data = [act for act in acts],
    name = "Acts",
    functions_to_index = []
    )

TABLE_DIRECTS = Table(
    data = [direct for direct in directs],
    name = "Directs",
    functions_to_index = []
    )

TABLE_DOMAIN = Table(
    data = [elem for elem in domain],
    name = "Domain",
    functions_to_index = []
    )
 
DB = FilmDataBase(
    name = 'Movies',
    list_of_tables=[
        TABLE_ACTORS,
        TABLE_ACTS,
        TABLE_ARTISTS,
        TABLE_DIRECTORS,
        TABLE_DIRECTS,
        TABLE_FILMS,
        TABLE_DOMAIN
        ]
    )

# FUNCTIONS = {
    # 'is_actor':Function('is_actor', lambda DB, t: t in DB.tables['Actors'].data),
    # 'is_film':Function('is_film', lambda DB, t: t in DB.tables['Films'].data)
# }

# DB.tables['Domain'].set_functions_to_index('is_actor', 'is_film')
# DB.tables['Domain']._update_indexes()
