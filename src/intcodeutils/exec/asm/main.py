import argparse
from intcodeutils import parse_intasm
from intcodeutils import output_intelf
import sys

parser = argparse.ArgumentParser(description='IntCode assembly')

parser.add_argument(
    'file',
    metavar='FILE',
    type=argparse.FileType('r'),
    help='Intcode assembly files')

parser.add_argument(
    '-o', '--out',
    metavar='FILE',
    type=argparse.FileType('w'),
    default=sys.stdout,
    help='Output file. Default stdout')

def main():
    args = parser.parse_args()
    output_intelf(parse_intasm(args.file), file=args.out)