# -*- coding: utf-8 -*-
"""
Created on Tue Oct 25 10:54:20 2022

@author: Julien
"""

from enum import Enum
from .evaluable import Evaluable

class Quantifier(Enum):
    FORALL = 1
    EXISTS = 2

class Quantified(Evaluable):
    __match_args__ = ('quantifier', 'bound_var', 'formula')

    def __init__(self, quantifier, var, f):
        """
        Implementation of quantified evaluables.

        Parameters
        ----------
        quantifier : Quantifier
            A quantifier object (either FORALL or EXISTS).
        var : TYPE
            DESCRIPTION.
        f : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

        """
        self.quantifier = quantifier
        self.bound_var = var
        self.formula = f

    def get_quantifier(self):
        """
        Getter method of the attribute quantifier.

        Returns
        -------
        Quantifier
            A quantifier object (either FORALL or EXISTS)..

        """
        return self.quantifier

    def get_var(self):
        """
        Getter method of the attribute var.

        Returns
        -------
        Variable
            The quantified variable.

        """
        return self.bound_var
    
    def get_formula(self):
        """
        Getter method of the attribute formula.

        Returns
        -------
        Formula
            The formula one wants to evaluate.

        """
        return self.formula

    def modify_env(self, env, x):
        """
        Modify the current environment.

        Parameters
        ----------
        env : dict
            Current environment.
        x : TYPE
            DESCRIPTION.

        Returns
        -------
        env : dict
            Modified version of the environment.

        """
        env[self.get_var()] = x
        
        return env
    
    def eval(self, model, env):
        env_var = env.get(self.get_var())
        
        res = None
        
        match self.get_quantifier():
            case Quantifier.FORALL:
                res = all(self.get_formula().eval(model, self.modify_env(env, x)) for x in model.get_domain())
            case Quantifier.EXISTS:
                res = any(self.get_formula().eval(model, self.modify_env(env, x)) for x in model.get_domain())
        
        env[self.get_var()] = env_var
        
        return res