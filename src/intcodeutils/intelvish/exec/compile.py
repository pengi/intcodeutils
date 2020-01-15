from intcodeutils.intelvish import IlvsParser, IlvsLexer, IlvsError, compile_ast
import argparse
import sys

parser = argparse.ArgumentParser(description='Intevlish compiler')

parser.add_argument(
    'intelvish_file',
    metavar='INTELVISH',
    type=argparse.FileType('r'),
    help='Intevlish file')

parser.add_argument(
    '-o', '--out',
    metavar='OUTPUT',
    type=argparse.FileType('w'),
    default=sys.stdout,
    help='Output file. Default stdout')


def main():
    args = parser.parse_args()

    ilv_lexer = IlvsLexer()
    ilv_parser = IlvsParser()

    ast = ilv_parser.parse(ilv_lexer.tokenize(args.intelvish_file.read()))

    print(str(compile_ast(ast.simplify())), file=args.out)
