# -*- coding: utf-8 -*-
"""
Created on Tue Oct 25 16:15:11 2022

@author: Julien
"""

# Some formulas that can be used to test our evaluation functions.

FORMULAS = [
    "∃x. film(x)",
    "∃x. actor(x)",
    "∃x. artist(x)",
    "∃x. director(x)",
    "exist x. ¬film(x) and ¬actor(x) and ¬director(x)",
    "forall x. film(x)",
    "forall x. actor(x)",
    "forall x. artist(x)",
    "forall x. director(x)",
    "forall x. artist(x) or film(x)",
    "forall x. ¬artist(x) or ¬film(x)",
    "forall x. film(x) or exist z. forall y.film(y) and director(z)",
    "forall x. (¬film(x) or exist y. acts(y, x) or directs(y, x))",
    "forall x. exist y. acts(y, x) or acts(x, y) or directs(x, y) ",
    "forall x. (¬film(x) and artist(x)) or (film(x) and ¬artist(x))",
    "exist x. acts('Novak Kim', x)",
    "exist x. acts(x, 'Vertigo')",
    "exist x. directs('Hitchcock Alfred', x)",
    "exist x. directs(x, 'Vertigo')",
    "exist x. exist y. acts(x, y) and directs(x, y)",
    "exist x. acts('Stewart James', x) and acts('Novak Kim', x)",
    ]
