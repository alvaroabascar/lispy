def tokenize(program):
    """Split the program into tokens (words, ")" and "(")."""
    return program.replace("(", " ( ").replace(")", " ) ").split()

def atom(token):
    return token

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
    return read_from_tokens(tokenize(program))

if __name__ == '__main__':
    import sys
    print(parse(sys.argv[1]))
