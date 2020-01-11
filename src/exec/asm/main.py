import argparse
from intutils import parse_intasm 

parser = argparse.ArgumentParser(description='IntCode assembly')

parser.add_argument(
    'files',
    metavar='FILE',
    type=argparse.FileType('r'),
    nargs='+',
    help='Intcode assembly files')

def main():
    args = parser.parse_args()
    for f in args.files:
        print(parse_intasm(f).__dict__)