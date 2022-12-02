from fo_formulas import *
from fo_parser import *
from create_db_from_file import DB
from visitor import Visitor

def formula_to_string(f):
    match f:
        case BinaryOp(Binop.AND, f1, f2): return f"({formula_to_string(f1)} ∧ {formula_to_string(f2)})"
        case BinaryOp(Binop.OR, f1, f2): return f"({formula_to_string(f1)} ∨ {formula_to_string(f2)})"
        case Neg(f): return f"¬{formula_to_string(f)}"
        case Quantified(Quantifier.FORALL, v, f): return f"(∀ {v}. {formula_to_string(f)})"
        case Quantified(Quantifier.EXISTS, v, f): return f"(∃ {v}. {formula_to_string(f)})"
        case UnaryPred(UPred.ACTOR, t): return f"actor({formula_to_string(t)})"
        case UnaryPred(UPred.DIRECTOR, t): return f"director({formula_to_string(t)})"
        case UnaryPred(UPred.FILM, t): return f"film({formula_to_string(t)})"
        case UnaryPred(UPred.ARTIST, t): return f"artist({formula_to_string(t)})"
        case BinaryPred(BPred.ACTS, t1, t2): return f"acts({formula_to_string(t1)}, {formula_to_string(t2)})"
        case BinaryPred(BPred.DIRECTS, t1, t2): return f"directs({formula_to_string(t1)}, {formula_to_string(t2)})"
        case BinaryPred(BPred.EQ, t1, t2): return f"{formula_to_string(t1)} = {formula_to_string(t2)}"
        case Variable(v): return v
        case Constant(v):
            v = v.replace("\\", "\\\\")
            if "'" not in v:
                return f"'{v}'"
            else:
                v = v.replace("\"", "\\\"")
                return f"\"{v}\""



FORMULAS = ["∃ys. film(ys)",\
            "forall x. film(x) or artist(x)",
            "forall x. film(x) or exist z. forall y.film(y) and director(z)",
            # "acts('O\\\'Hara Maureen', x)",
            ]

def eval_formula(f):
    return(f.eval(DB, {}))

def eval_formula_v2(formula, model, env):
    match formula:
        case Quantified(Quantifier.FORALL, v, f): 
            env_var = env.get(v)
            res = all(eval_formula_v2(f, model, formula.modify_env(env, x))  for x in model.get_domain())
            env[v] = env_var
            return res
        
        case Quantified(Quantifier.EXISTS, v, f): 
            env_var = env.get(v)
            res = any(eval_formula_v2(f, model, formula.modify_env(env, x)) for x in model.get_domain())
            env[v] = env_var
            return res
        
        case BinaryOp(Binop.AND, f1, f2): return eval_formula_v2(f1, model, env) & eval_formula_v2(f2, model, env)
        case BinaryOp(Binop.OR, f1, f2): return eval_formula_v2(f1, model, env) | eval_formula_v2(f2, model, env)
        case Neg(f): return not eval_formula_v2(f, model, env)
        case UnaryPred(UPred.ACTOR, t): return model.is_actor(eval_formula_v2(t, model, env))
        case UnaryPred(UPred.DIRECTOR, t): return model.is_director(eval_formula_v2(t, model, env))
        case UnaryPred(UPred.FILM, t): return model.is_film(eval_formula_v2(t, model, env))
        case UnaryPred(UPred.ARTIST, t): return model.is_artist(eval_formula_v2(t, model, env))
        case BinaryPred(BPred.ACTS, t1, t2): return model.acts_in(t1, t2)
        case BinaryPred(BPred.DIRECTS, t1, t2): return model.directs(t1, t2)
        case BinaryPred(BPred.EQ, t1, t2): return t1 == t2
        case Variable(v): return env.get(v)
        case Constant(v): 
            v = v.replace("\\", "\\\\")
            if "'" not in v:
                return f"'{v}'"
            else:
                v = v.replace("\"", "\\\"")
                return f"\"{v}\""
            
        case _:
            RaiseError
    #Idem mais on reprend le code à l'intérieur de la fonction
    
def visitor_pattern(f):
    pass
    #Idem mais on met le code dans une seule classe
    


STR = [formula_parser(formula) for formula in FORMULAS]
V = Visitor(DB, {})

for fs in STR:
    for f in fs:
        print(formula_to_string(f))
        print(eval_formula(f))
        print(eval_formula_v2(f, DB, {}))
        print(V(f))
