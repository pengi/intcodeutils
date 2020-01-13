from intcodeutils.intelvish import IntelvishParser, IntelvishLexer, IntelvishError
import argparse
import sys

parser = argparse.ArgumentParser(description='Intevlish AST printer')

parser.add_argument(
    'intelvish_file',
    metavar='INTELVISH',
    type=argparse.FileType('r'),
    help='Intevlish file')

parser.add_argument(
    '-s', '--simplify',
    action='store_const',
    const=True, default=False,
    help='Simplify tree')

parser.add_argument(
    '-o', '--out',
    metavar='OUTPUT',
    type=argparse.FileType('w'),
    default=sys.stdout,
    help='Output file. Default stdout')


def main():
    args = parser.parse_args()

    ilv_lexer = IntelvishLexer()
    ilv_parser = IntelvishParser()

    ast = ilv_parser.parse(ilv_lexer.tokenize(args.intelvish_file.read()))

    if args.simplify:
        ast = ast.simplify()

    print(str(ast), file=args.out)
