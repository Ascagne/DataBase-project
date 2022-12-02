# -*- coding: utf-8 -*-
"""
Created on Tue Sep 20 17:07:04 2022

@author: Julien
"""

from copy import deepcopy

class Table:
    def __init__(self, name:str, data:list, functions:list = [], functions_to_index:list=[]) -> None:
        """
        Instantiation of the Table class.
    
        Parameters
        ----------
        name : str
            Name of the table.
        data : list 
            Elements of the table.
        functions : list
            List of Function objects (cf Function class in structure/), contains all the functions that could be applied to this table.
        functions_to_index : list
            Name of the functions for which one indexes the table.
        

        Returns
        -------
        None

        """
        
        self.name = name
        self.data = data
        self.functions = functions
        self.functions_to_index = functions_to_index
        self.indexes = {}
        self._update_indexes()
        
    def set_functions_to_index(self, *args) -> None:
        self.functions_to_index = [*args]
        
    def _update_indexes(self) -> None:
        """
        Recompute the indexes of the functions.

        Returns
        -------
        None
            Inplace method.

        """
        for func_name in self.functions_to_index:
            self.indexes[func_name] = {}
            
            for elem in self.data:
                value = self.functions[func_name](elem)
                
                if value not in self.indexes[func_name]:
                    self.indexes[func_name][value] = [elem]
                else:
                    self.indexes[func_name][value].append(elem)
                    
                
    def _sequential_search(self, function_name:str, value, data = None) -> list:
        """
        Implementation of a sequential search on the table.

        Parameters
        ----------
        function_name : str
            Name of the function one is performing the search on.
        value : 
            Value searched.
        data : list, optional
            In case we want to perform a sequential scan on more restrictive data 
            than the whole content of the table. By default we take the whole data.

        Returns
        -------
        list
            Elements whose evaluation is the searched value.

        """
        if data == None: data = self.data
        
        return [elem for elem in data if self.functions[function_name](elem) == value] 
                
    def _smart_search(self, function_name:str, value):
        """
        A smart sequential search previously checking if the function is indexed.

        Parameters
        ----------
        function_name : str
            Name of the function one is performing the search on..
        value : TYPE
            Value searched.

        Returns
        -------
        list
            Elements whose evaluation is the searched value.

        """
        
        if function_name in self.indexes:
            return self.indexes[function_name].get(value) or []
            
        else:
            return self._sequential_search(function_name, value)
        
    def _conditional_search(self, list_of_functions:list, list_of_values:list) -> list:
        """
        A conditional search looking for the best indexed candidate functions to start with, 
        and then performing a sequential search.

        Parameters
        ----------
        list_of_functions : list
            Functions one searches on.
        list_of_values : list
            Values to be taken by the functions.

        Returns
        -------
        list
            A subset S of the whole data that verifies : forall x in S, forall (f, v) in our lists, f(x) = v.

        """
        
        list_of_functions = deepcopy(list_of_functions)
        list_of_values = deepcopy(list_of_values)
        
        # We look for the best candidate indexed function (smallest subset) to start with
        
        m = len(self.data)
        candidate_name = None
        candidate_value = None
        
        for func_name, value in zip(list_of_functions, list_of_values):
            if func_name in self.indexes and value in self.indexes[func_name]:
                
                p = len(self.indexes[func_name][value])
                if p < m:
                    m = p
                    candidate_name = func_name
                    candidate_value = value
                    
        # If we have found an appropriate candidate we remove it from the search
        
        if candidate_name:
            data = self.indexes[candidate_name][candidate_value]
            list_of_functions.remove(candidate_name)
            list_of_values.remove(candidate_value)
            
        else:
            data = self.data 
            
        # Then we successively perform sequential searches until the end (either of the functions or pf the searching subset)
        while len(data) != 0 and len(list_of_functions) > 0:
            data = self._sequential_search(list_of_functions[0], list_of_values[0], data)
            list_of_functions.pop(0)
            list_of_values.pop(0)
            
        return(data)
            