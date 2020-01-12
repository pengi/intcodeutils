# Fibonacci calculation example

Simple example using make and intutils to build a program calculating fibonacci numbers

To assemble and link the program, make sure `make` is installed, as well as having intutils available. Then run

```
make
```

The output should look like:
```
$ make
intcode-asm -o loader.intelf loader.intasm
intcode-asm -o main.intelf main.intasm
intcode-ld -o fibonacci.intelf -l loader.intld loader.intelf main.intelf
intcode-objcopy -o fibonacci.intcode fibonacci.intelf
```

The result is then available in `fibonacci.intcode`
