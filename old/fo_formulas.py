from enum import Enum
from create_db_from_file import DB

class Evaluable:
    def eval(self, model, env):
       pass 

class Quantifier(Enum):
    FORALL = 1
    EXISTS = 2


class Quantified(Evaluable):
    __match_args__ = ('quantifier', 'bound_var', 'formula')

    def __init__(self, quantifier, var, f):
        self.quantifier = quantifier
        self.bound_var = var
        self.formula = f

    def get_quantifier(self):
        return self.quantifier

    def get_var(self):
        return self.bound_var
    
    def get_formula(self):
        return self.formula

    def modify_env(self, env, x):
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
            
class Binop(Enum):
    OR = 1
    AND = 2

class BinaryOp(Evaluable):
    __match_args__ = ('op', 'left', 'right')

    def __init__(self, op, f1, f2):
        self.op = op
        self.left = f1
        self.right = f2

    def get_op(self):
        return self.op

    def get_left(self):
        return self.left

    def get_right(self):
        return self.right

    def eval(self, model, env):
        match self.get_op():
            case Binop.OR: 
                return self.get_left().eval(model, env) | self.get_right().eval(model, env)
            case Binop.AND:
                return self.get_left().eval(model, env) & self.get_right().eval(model, env)


class Neg(Evaluable):
    def __init__(self, f):
        self.formula = f

    def eval(self, model, env):
        return not self.get_sub_formula().eval(model, env)

    def get_sub_formula(self):
        return self.formula


class BPred(Enum):
    EQ = 1
    ACTS = 2
    DIRECTS = 3


class BinaryPred(Evaluable):
    __match_args__ = ('predicate', 'arg1', 'arg2')

    def __init__(self, pred, t1, t2):
        self.predicacte = pred
        self.arg1 = t1
        self.arg2 = t2

    def get_predicate(self):
        return self.predicate

    def get_arg1(self):
        return self.arg1

    def get_arg2(self):
        return self.arg2

    def eval(self, model, env):
        v1 = self.get_arg1().eval(model, env)
        v2 = self.get_arg2().eval(model, env)
        
        match self.predicacte:
            case BPred.EQ: return v1 == v2
            case BPred.ACTS: return model.acts_in(v1, v2)
            case BPred.DIRECTS: return model.directs(v1, v2)


class UPred(Enum):
    ACTOR = 1
    FILM = 2
    ARTIST = 3
    DIRECTOR = 4

class UnaryPred(Evaluable):
    __match_args__ = ('predicate', 'arg')

    def __init__(self, pred, t):
        self.predicate = pred
        self.arg = t

    def get_predicate(self):
        return self.predicate

    def get_arg(self):
        return self.arg

    def eval(self, model, env):
        v = self.get_arg().eval(model, env)
        match self.predicate:
            case UPred.ACTOR: return model.is_actor(v) # is v in the table Actor of the model
            case UPred.FILM: return model.is_film(v)
            case UPred.ARTIST: return model.is_artist(v)
            case UPred.DIRECTOR: return model.is_director(v)

class Variable(Evaluable):
    __match_args__ = ('name',)

    def __init__(self, name):
        self.name = name

    def eval(self, model, env):
        return env[self.get_name()]

    def get_name(self):
        return self.name


class Constant(Evaluable):
    __match_args__ = ('value',)

    def __init__(self, val):
        self.value = val

    def eval(self, model, env):
        return self.value

    def get_value(self):
        return self.value


# faire une fonction eval formula
# faire une méthode visitor