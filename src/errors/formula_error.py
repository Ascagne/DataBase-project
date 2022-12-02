# -*- coding: utf-8 -*-
"""
Created on Tue Oct 25 17:30:33 2022

@author: Julien
"""

class Error(Exception):
    """Base class for exceptions in this module."""
    pass

class FormulaError(Error):
    """Exception raised for errors in the formula.

    Attributes:
        expression -- input expression in which the error occurred
        message -- explanation of the error
    """

    def __init__(self, expression, message):
        self.expression = expression
        self.message = message