# -*- coding: utf-8 -*-

# EXTERNAL LIBRARIES

import sys
from pathlib import Path
import os
from lark import Lark, Transformer, logger
# import the module where you define the classes that implement the structure of first order logic formulae

# INTERNAL IMPORTS

sys.path.append(Path(os.path.realpath(__file__)).parent.parent)   

from src.evaluables.binaryop import *
from src.evaluables.binarypred import *
from src.evaluables.constant import *
from src.evaluables.neg import *
from src.evaluables.quantified import *
from src.evaluables.unarypred import *
from src.evaluables.variable import *

GRAMMAR = r"""
NEG:  "~" | "¬" | "!"
AND.2: "/\\" | "∧" | "and"i
OR.2: "\\/" | "∨" | "or"i
FORALL.2: "∀" | "forall"i
EXIST.2: "∃" | "exist"i
NEQ: "<>" | "~=" | "!=" | "≠"
EQ: "="
ACTOR.2: "actor"i
FILM.2: "film"i
ARTIST.2: "artist"i
DIRECTOR.2: "director"i
UNARYPRED.2: ACTOR | FILM | ARTIST | DIRECTOR
ACTS.2: "acts"i
DIRECTS.2: "directs"i
BINARYPRED.2: ACTS | DIRECTS
SYMBOLS: /[a-zA-Z0-9\-_]/
VAR: SYMBOLS+
QUOTE_NAME: /'([^'\\]|\\'|\\\\)+'/
DOUBLE_QUOTE_NAME: /\"([^\"\\]|\\\"|\\\\)+\"/


formulas: formula              -> one_formula
        | formulas "," formula -> s_formulas

formula: disjunction                            -> unpack
       | quantified_formula                     -> unpack
       | disjunction OR quantified_formula      -> disj
       | conjunction AND quantified_formula     -> conj
       | disjunction OR conjformula             -> disj

disjunction: conjunction                        -> unpack
           | disjunction OR conjunction         -> disj

conjformula: conjunction AND quantified_formula -> conj

conjunction: atom                               -> unpack
           | conjunction AND atom               -> conj

?atom: predicate                                -> unpack
    |  "(" formula ")"                          -> unpack
    | NEG atom                                  -> neg


predicate: UNARYPRED "(" term ")"               -> u_pred
         | BINARYPRED "(" term "," term ")"     -> b_pred
         | term EQ term                         -> eq
         | term NEQ term                        -> neq

term: VAR                                       -> var
    | QUOTE_NAME                                -> qconst
    | DOUBLE_QUOTE_NAME                         -> dconst


quantified_formula: FORALL VAR "." formula      -> forall
                  | EXIST VAR "."  formula      -> exist


%import common.WS
%ignore WS
"""

class BuildFormula(Transformer):
    """Class for compiling parse trees to First-Order Formulas."""

    def one_formula(self, ch):
        [f] = ch
        return [f]

    def s_formulas(self, ch):
        [fs,f] = ch
        fs.append(f)
        return fs

    def unpack(self, ch):
        [f] = ch
        return f

    def forall(self, ch):
        [_, v, f] = ch
        return Quantified(Quantifier.FORALL, v, f)

    def exist(self, ch):
        [_, v, f] = ch
        return Quantified(Quantifier.EXISTS, v, f)

    def disj(self, ch):
        [l, _, r] = ch
        return BinaryOp(Binop.OR, l, r)

    def conj(self, ch):
        [l, _, r] = ch
        return BinaryOp(Binop.AND, l, r)

    def neg(self, ch):
        [_, f] = ch
        return Neg(f)

    def u_pred(self, ch):
        [p, t] = ch
        match p:
            case "actor":
                return UnaryPred(UPred.ACTOR, t)
            case "film":
                return UnaryPred(UPred.FILM, t)
            case "artist":
                return UnaryPred(UPred.ARTIST, t)
            case "director":
                return UnaryPred(UPred.DIRECTOR, t)

    def b_pred(self, ch):
        [p, t1, t2] = ch
        match p:
            case "acts":
                return BinaryPred(BPred.ACTS, t1, t2)
            case "directs":
                return BinaryPred(BPred.DIRECTS, t1, t2)

    def eq(self, ch):
        [t1, _, t2] = ch
        return BinaryPred(BPred.EQ, t1, t2)

    def neq(self, ch):
        [t1, _, t2] = ch
        return Neg(BinaryPred(BPred.EQ, t1, t2))

    def var(self, ch):
        [v] = ch
        return Variable(v)

    def qconst(self, ch):
        [c] = ch
        return Constant(c[1:-1].replace("\\'", "'").replace("\\\\", "\\"))

    def dconst(self, ch):
        [c] = ch
        return Constant(c[1:-1].replace('\\"', '"').replace("\\\\", "\\"))


formula_parser = Lark(GRAMMAR,
                      start='formulas',
                      parser='lalr',
                      regex=True,
                      transformer=BuildFormula()).parse

def formula_parse_file(file_name):
    """Function helper that parses a file containing a formula."""
    with open(file_name, encoding='utf-8') as f:
        return formula_parser(f.read())
