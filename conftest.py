# -*- coding: utf-8 -*-
"""
Created on Fri Dec  2 09:34:23 2022

@author: Julien
"""

import sys


def pytest_configure(config):
    sys._called_from_test = True

def pytest_unconfigure(config):
    del sys._called_from_test