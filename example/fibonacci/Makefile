APP = fibonacci

LDFILE = loader.intld
SOURCES = \
	loader.intasm \
	main.intasm

OBJECTS = $(SOURCES:.intasm=.intelf)

all: $(APP).intcode

clean:
	rm -f $(APP).intcode $(APP).intelf $(OBJECTS)

$(APP).intelf: $(LDFILE) $(OBJECTS)
	intcode-ld -o $@ -l $(LDFILE) $(OBJECTS)

%.intcode: %.intelf
	intcode-objcopy -o $@ $^

%.intelf: %.intasm
	intcode-asm -o $@ $^