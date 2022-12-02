# -*- coding: utf-8 -*-
"""
Created on Tue Sep 20 16:21:54 2022

@author: Julien
"""

class Function:
    def __init__(self, name:str, formula):
        """
        Instantiate a Function object. 
        This framework is well suited if one wants to identify functions by their name.

        Parameters
        ----------
        name : str
            Name of the function.
        formula : function
            Formula of the function, can be really different from one function to another.

        Returns
        -------
        None.

        """
        self.name = name
        self.formula = formula
        
    def __call__(self, *args):
        return self.formula(*args) 
    
    