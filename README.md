IntUtils
========

Intcode toolchain for Advent of Code 2019 intcode computer

The toolchain originates around the intelf format, a format understandable by the Elfs maintaining the intcode computer

Advent of Code
--------------
An advent calender with programming puzzles, made by Eric Wastl

Author of intutils is not affiliated with Advent of Code

More information about Advent of Code is available their [homepage](https://adventofcode.com)

Installation
------------
Recommended method of testing is using pip, in an virtualenv

Run in a shell:
```
$ virtualenv venv
$ . venv/bin/activate
$ pip install git+https://github.com/pengi/intutils.git
```

Commands available are:
```
$ intcode-asm
$ intcode-ld
$ intcode-objcopy
```

Since intutils is under development, it is not recommended to install outside a virtualenv.

More information about virtualenv is available on their [homepage](https://virtualenv.pypa.io)

intcode
-------
A big part of the Advent of Code 2019 puzzles was the intcode computer. The intcode computer enabled the possibility to hide puzzle logic from the user, but at the same time can be executed on the users computer.

The intcode computer is described in detail in the puzzles building the computer:
* [Day 2](https://adventofcode.com/2019/day/2) - opcode 1,2 and 99
* [Day 5](https://adventofcode.com/2019/day/5) - opcode 3,4 from part 1, 5,6,7,8 from part 2 and parameter mode 1
* [Day 9](https://adventofcode.com/2019/day/9) - opcode 9 and parameter mode 2

Note that the intcode computer contains a "base reference" from day 9. In intutils, it is called "stack pointer" or "sp".

The intcode files is handled by intutils as described in the puzzles, using the file extension .intcode

An example:
```
109,72,21101,0,9,0,1105,1,40,1101,9,0,30,1006,30,29,1001,30,-1,30,1001,30,31,25,4,0,1105,1,13,99,0,10,101,100,111,99,116,110,105,32,109,1,104,72,104,101,104,108,104,108,104,111,109,-1,2106,0,0,14,72,101,108,108,111,32,105,110,116,99,111,100,101,10
```

intelf
------
To be able to link mulitple files, a file that can be read by the intcode-[elf](https://en.wikipedia.org/wiki/Elf)s is requred, containing linking information. For non-intcode computers, the [elf](https://en.wikipedia.org/wiki/Executable_and_Linkable_Format) files exists.

For intcode, an intelf file is available, containing intcode with relocation information, and symbol names

The format is divided in section. A section is atomic, and is not intended to be split. A section can contain symbols, wich is named offsets within the section. The sections should be unique within the intelf, and consecently int the intcode project.

An example file:
```
.section.a: 1,2,3,4,5,6,7
sym_a.offset: 4

.section.b: 1,2,3,4,5,6,7
sym_b.offset: 4
```

The file contains two sections, named ".section.a" and ".section.b"

The symbol "sym_a" points to the number "5" in the ".section.a" block, since all addresses starts at 0

Also, symbol-relative values can be added:
```
.text: 1101,2,3,dest+2
main.offset: 0

.data: 0,0,0,0
var.offset: 0
```

intcode-asm
-----------

Assembler for assembly language to intelf

The syntax used for intcode-asm is as follows:

```
@section .section.a
    add [2],[3],[4]
sym_a:
    jt [6],[7]

@section .section.b
    add [2],[3],[4]
sym_b:
    jt [6],[7]
```

There are three kinds of lines:

1. `@section` starts a section
2. `label:` defines a label (which currently also is a symbol...)
3. `op arg1,arg2,arg3` is an instruction, which will be converted to intcode

Available instructions are:

| Instruction | Description                                                         |
| ----------- | ------------------------------------------------------------------- |
| `add a,b,c` | Add `a` and `b`, store at `c`                                       |
| `mul a,b,c` | Multiply `a` and `b`, store at `c`                                  |
| `in a`      | Input a value, store at `a`                                         |
| `out a`     | Output value `a`                                                    |
| `jt a,b`    | Jump to `b` if `a` is not zero (is true)                            |
| `jf a,b`    | Jump to `b` if `a` is zero (is false)                               |
| `lt a,b,c`  | Compare `a` and `b`, store `1` in `c` if `a<b`, store `0` otherwise |
| `eq a,b,c`  | Compare `a` and `b`, store `1` in `c` if `a=b`, store `0` otherwise |
| `addsp a`   | Increases stack pointer with `a`                                    |
| `halt`      | Halt the intcode computer                                           |

Values can be written in 5 formats:

| Format                          | Example         | Description                                        |
| ------------------------------- | --------------- | -------------------------------------------------- |
| Immediate                       | `32`, `-12`     | Contant value                                      |
| Symbol relative                 | `var`, `var+12` | Contant address                                    |
| Memory lookup, constant address | `[32]`          | Value at contant memory location                   |
| Memory lookup, symbol relative  | `[var+12]`      | Value at address relative to symbol                |
| Memory lookup, stack relative   | `[%sp+12]`      | Value at address relative to current stack pointer |
