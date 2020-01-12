import argparse
from intutils import parse_intasm, parse_intelf, output_intelf, merge_intelfs
import sys

parser = argparse.ArgumentParser(description='IntCode linker')

parser.add_argument(
    'elf_files',
    metavar='INTELF',
    nargs='+',
    type=argparse.FileType('r'),
    help='Intcode elf files')

parser.add_argument(
    '-l', '--ld-file',
    metavar='INTLD',
    type=argparse.FileType('r'),
    help='Linker script',
    required=True)

parser.add_argument(
    '-o', '--out',
    metavar='OUTPUT',
    type=argparse.FileType('w'),
    default=sys.stdout,
    help='Output file. Default stdout')

def main():
    args = parser.parse_args()
    elfs = []
    for elf_file in args.elf_files:
        elfs.append(parse_intelf(elf_file))
    output_elf = merge_intelfs(args.ld_file, elfs).clone_resolve_symbols()
    output_intelf(output_elf, file=args.out)