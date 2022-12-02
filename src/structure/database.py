# -*- coding: utf-8 -*-
"""
Created on Tue Sep 20 15:59:27 2022

@author: Julien
"""

# EXTERNAL LIBRARIES

from copy import deepcopy
import sys
import os
from pathlib import Path

# INTERNAL IMPORTS
      
sys.path.append(Path(os.path.realpath(__file__)).parent.parent.parent)      
from src.structure.table import Table
            
class DataBase:
    def __init__(self, name:str, list_of_tables:list = None) -> None:
        """
        Instantiation of the Database class

        Parameters
        ----------
        name : str
            Name of the database.
        list_of_tables : list, optional
            List of tables of the database. The default is None.

        Returns
        -------
        None

        """
        self.name = name
        self.tables = {}
        for table in list_of_tables:
            self.tables[table.name] = table
      
            
    def _join_naive(self, table1_name:str, table2_name:str, list_f:list, list_g:list) -> list:
        """
        Naive join method. As it is slow it is not recommended to use it but it can interesting to use it
        as a reference for new faster join implementations.

        Parameters
        ----------
        table1_name : str
            Name of the first table to join on.
        table2_name : str
            Name of the second table to join on.
        list_f : list
            List of functions applied to the first table used to perform the join.
        list_g : list
            List of functions applied to the second table used to perform the join.

        Returns
        -------
        list
            Joined data.

        """
        
        S = []
            
        for row1 in self.tables[table1_name].data:
            for row2 in self.tables[table2_name].data:
                if [self.tables[table1_name].functions[func_name](row1) for func_name in list_f] == \
                   [self.tables[table2_name].functions[func_name](row2) for func_name in list_g]:
                        
                       S.append((row1, row2))
                       
        return(S)
    
    
    def _join_naive_improved(self, table1_name:str, table2_name:str, list_f:list, list_g:list) -> list:
        """
        Naive join method that only evaluates each function once on each element.

        Parameters
        ----------
        table1_name : str
            Name of the first table to join on.
        table2_name : str
            Name of the second table to join on.
        list_f : list
            List of functions applied to the first table used to perform the join.
        list_g : list
            List of functions applied to the second table used to perform the join.

        Returns
        -------
        list
            Joined data.

        """
        
        S = []
        
        values_f = {}
        values_g = {}
        
        for row1 in self.tables[table1_name].data:
            if row1 not in values_f:
                values_f[row1] = [self.tables[table1_name].functions[func_name](row1) for func_name in list_f] 
            for row2 in self.tables[table2_name].data:
               if row2 not in values_g:
                   values_g[row2] = [self.tables[table2_name].functions[func_name](row2) for func_name in list_g]
               if values_f[row1] == values_g[row2]:
                   S.append((row1, row2))
                   
        return(S)
    
    def _join_from_indexes(self, table1_name:str, table2_name:str, list_f:list, list_g:list) -> list:
        """
        Perform a join using the assumption that the second table is indexed. 
        Uses the conditional search method of the Table class.

        Parameters
        ----------
        table1_name : str
            Name of the first table to join on.
        table2_name : str
            Name of the second table to join on.
        list_f : list
            List of functions applied to the first table used to perform the join.
        list_g : list
            List of functions applied to the second table used to perform the join.

        Returns
        -------
        list
            Joined data.

        """
        # We assume that the functions of Table 2 are already indexed
        
        S = []
        
        for row1 in self.tables[table1_name].data:
            values1 = [self.tables[table1_name].functions[func_name](row1) for func_name in list_f]
            for row2 in self.tables[table2_name]._conditional_search(deepcopy(list_g), values1):
                S.append((row1, row2))
            
        return(S)

    def _join_from_keys(self, table1_name:str, table2_name:str, list_f:list, list_g:list) -> list:
        """
        Perform a join using the assumption that both tables are indexed. 
        Usually the most efficient method.

        Parameters
        ----------
        table1_name : str
            Name of the first table to join on.
        table2_name : str
            Name of the second table to join on.
        list_f : list
            List of functions applied to the first table used to perform the join.
        list_g : list
            List of functions applied to the second table used to perform the join.

        Returns
        -------
        list
            Joined data.

        """
        j, f, s, m = 0, 0, 0, 0
        
        for i in  range(len(list_f)):
            a = len(self.tables[table1_name].indexes[list_f[i]])
            b = len(self.tables[table2_name].indexes[list_g[i]])
            
            if a/b > m:
                m = a/b
                j = i
                f = 1
                s = 0
                
            elif b/a> m:
                m = b/a
                j = i
                f = 0
                s = 1
            else:
                pass
            
        if f == 0:
            
            indexes = (
                self.tables[table1_name].indexes,
                self.tables[table2_name].indexes
                )
            
            functions = (
                list_f,
                list_g
                )
        else:
            
            indexes = (
                self.tables[table2_name].indexes,
                self.tables[table1_name].indexes
                )
            
            functions = (
                list_g,
                list_f
                )
            
        S = []

        for key1 in indexes[f][functions[f][j]]:
            elem1 = indexes[f][functions[f][j]][key1]

            if key1 in indexes[s][functions[s][j]]:
                elem2 = indexes[s][functions[s][j]][key1]
                
                tmp = [(e1, e2) for e1 in elem1 for e2 in elem2]

                for i in range(len(list_f)):
                    if len(tmp) == 0: break
                
                    elif i != j:
                        
                        name_1 = functions[f][i]
                        name_2 = functions[s][i]
                        
                        tmp = [
                            elem for elem in tmp \
                            if self.tables[table1_name].functions[name_1](elem[0]) == self.tables[table2_name].functions[name_2](elem[1])
                        ]
                        
                    else:
                        pass
            

                S += tmp
            else:
                pass

        return(S)
        
    
    
    def create_new_table(self, name, data, functions, functions_to_index):        
        self.tables[name] = Table(name, data, functions, functions_to_index)
                
