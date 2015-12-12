from numbers import Number
import math
import operator as op

# a symbol is anything that can hold a value. We represent it as a string.
Symbol = str

class Procedure:
    """
    A procedure is just a function. It is composed by a set of parameters,
    a body (which will be evaluated) and an environment.
    """
    def __init__(self, args, body, env):
        self.args = args
        self.body = body
        self.env = env

    def __call__(self, *values):
        local_env = Env(upper_env=self.env)
        local_env.update(zip(self.args, values))
        return eval(self.body, local_env)

class Env(dict):
    """
    A lispy environment. It is instantiated with a set of symbols (params),
    the corresponding values (values), and an upper environment (upper_env),
    which is the parent environment (or None if this is the uppermost
    environment).

    """
    def __init__(self, params=[], values=[], upper_env=None):
        self.update(zip(params, values))
        self.upper = upper_env

    def find(self, param):
        """
        Returns the lowermost environment which contains the provided symbol
        (param), starting from the current environment and tracing upwards.
        """
        return self if param in self else self.upper.find(param)

def eval(x, env):
    """Evaluate an expression (x) given a certain environment (env)."""

    if isinstance(x, Number):
        return x

    # is it a variable?
    elif isinstance(x, Symbol):
        return env.find(x)[x]

    # is it a definition?
    # (define name value)
    elif x[0] == "define": # (define variable value)
        _, var, expr = x
        env[var] = eval(expr, env)

    # is it a conditional?
    # (if (condition) (consequence) (alternative))
    elif x[0] == "if":
        _, cond, conseq, alt = x
        if eval(cond, env):
            return eval(conseq, env)
        else:
            return eval(alt, env)

    # is it a lambda function?
    # (lambda (args...) (body))
    elif x[0] == "lambda":
        _, args, body = x
        return Procedure(args, body, env)

    # is it a direct quotation? return argument(s) without evaluating
    # (quote a b c)
    elif x[0] == "quote":
        return x[1:]

    # is it a set? (definition of already existing variable)
    elif x[0] == "set!":
        _, var, expr = x
        env.find(var)[var] = eval(expr, env)
    # it must be a function
    else:
        proc, args = eval(x[0], env), x[1:]
        args = [eval(arg, env) for arg in args]
        return proc(*args)

def tokenize(program):
    """Split the program into tokens (words, ")" and "(")."""
    return program.replace("(", " ( ").replace(")", " ) ").split()

def atom(token):
    try:
        return int(token)
    except ValueError:
        try:
            return float(token)
        except ValueError:
            return Symbol(token)

def read_from_tokens(tokens):
    """
    Turn the list of tokens into a list (of nested lists) representing the
    abstract syntax tree.
    """
    if not tokens:
        raise SyntaxError("Encountered EOF while reading")
    token = tokens.pop(0)
    # beginning of a lisp list
    if token == "(":
        L = []
        while tokens[0] != ")":
            L.append(read_from_tokens(tokens))
        # remove ")"
        tokens.pop(0)
        return L
    elif token == ")":
        raise SyntaxError('Unexpected ")"')
    else:
        return atom(token)

def parse(program):
    """Go from the raw program code to the abstract syntax tree."""
    tokens = tokenize(program)
    while (tokens):
        yield read_from_tokens(tokens)

def standard_env():
    env = Env()
    env.update(vars(math))
    env.update({
        '*': op.mul,
        '/': op.truediv,
        '+': op.add,
        '-': op.sub,
        '>=': op.ge,
        '<=': op.le,
        '>': op.gt,
        '<': op.lt,
        '=': op.eq
        })
    return env

def repl(env, prompt='lispy> '):
    expr = input(prompt)
    for statement in parse(expr):
        res = eval(statement, env)
        if res != None:
            print(res)
        repl(env, prompt)

if __name__ == '__main__':
    import sys
    env = standard_env()
    # if no arguments, run REPL
    if len(sys.argv) <= 1:
        repl(env)
    # if argument, run program passed as first argument
    else:
        with open(sys.argv[1]) as fd:
            # print(list(parse(fd.read())))
            for statement in parse(fd.read()):
                eval(statement, env)
