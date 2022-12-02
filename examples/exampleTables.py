# EXTERNAL LIBRARIES

import numpy as np
import sys
import os
from pathlib import Path

# INTERNAL IMPORTS
      
sys.path.append(Path(os.path.realpath(__file__)).parent.parent)

from src.structure.table import Table
from examples.exampleFunctions import FUNCTIONS

# CONSTANTS

N_POINTS = 1_000
N_DIMENSIONS = 2
L_BOUND = 0
U_BOUND = 100
SEED_1 = 42
SEED_2 = 0

# FUNCTION

def generate_data(l_bound:int, u_bound:int, n:int, m:int, seed:int) -> list:
    """
    Randomly generate integers to be used to test Table class.

    Parameters
    ----------
    l_bound : int
        Lower bound.
    u_bound : int
        Uppêr bound.
    n : int
        Number of vectors to generate.
    m : int
        Dimension of the vectors to be generated.
    seed : int
        Random seed, useful for reproducibility.

    Returns
    -------
    list of tuples
        A list of tuples (vectors of integers).

    """
    
    rng = np.random.default_rng(seed)
    array = rng.integers(l_bound, u_bound, (n, m))
    return [tuple(elem) for elem in array]

# DATA EXAMPLES

DATA_1 = generate_data(L_BOUND, U_BOUND, N_POINTS, N_DIMENSIONS, SEED_1)
DATA_2 = generate_data(L_BOUND, U_BOUND, N_POINTS, N_DIMENSIONS, SEED_2)

# TABLE EXAMPLES

T1 = Table('Table 1', DATA_1, FUNCTIONS, ['First Value', 'Min', 'Sum'])
T2 = Table('Table 2', DATA_2, FUNCTIONS, ['Second Value', 'Max', 'Sum'])