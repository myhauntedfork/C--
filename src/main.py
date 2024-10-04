from lexer import Lexer, LexerError
from parser import Parser, ParserError
from semantic import SemanticAnalyzer, SemanticError
from ast_nodes import *

def main():
    code = '''
    print("Hello, World!");
    x = 4;
    if x > 5 {
        print("x is greater than 5");
    } else if x == 5 {
        print("x is equal to 5");
    } else {
        print("x is less than 5");
    }
    '''

    try:
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        print("Tokens:")
        for token in tokens:
            print(token)

        parser = Parser(tokens)
        ast = parser.parse()
        print("\nAbstract Syntax Tree (AST):")
        for node in ast:
            print(node)

        semantic_analyzer = SemanticAnalyzer()
        for node in ast:
            semantic_analyzer.analyze(node)
        print("\nSemantic analysis completed successfully.")

    except LexerError as le:
        print(le)
    except ParserError as pe:
        print(pe)
    except SemanticError as se:
        print(se)

if __name__ == "__main__":
    main()
