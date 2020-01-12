import argparse
from intcodeutils import parse_intasm, parse_intelf, output_intelf, merge_intelfs
import sys

parser = argparse.ArgumentParser(description='IntCode object copy/exporter')

parser.add_argument(
    'elf_file',
    metavar='INTELF',
    type=argparse.FileType('r'),
    help='Intcode elf file')

parser.add_argument(
    '-o', '--out',
    metavar='OUTPUT',
    type=argparse.FileType('w'),
    default=sys.stdout,
    help='Output file. Default stdout')

def main():
    args = parser.parse_args()
    elf = parse_intelf(args.elf_file)
    ints = elf.export()
    intcode = ",".join([str(value) for value in ints]) + "\n"
    print(intcode, file=args.out)