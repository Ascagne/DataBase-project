# -*- coding: utf-8 -*-

# EXTERNAL LIBRARIES

import sys
import os
from pathlib import Path

# INTERNAL IMPORTS
      
sys.path.append(Path(os.path.realpath(__file__)).parent.parent)

from src.structure.function import Function

# EXAMPLES

FUNCTIONS = {
    'First Value':Function('First Value', lambda t: t[0]), 
    'Second Value':Function('Second Value', lambda t: t[1]), 
    'Max':Function('Max', lambda t: max(t)),
    'Min':Function('Min', lambda t: min(t)),
    'Sum':Function('Sum', lambda t: sum(t)),
}