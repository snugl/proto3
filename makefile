TARGET = prg/main.snug

run: compile
	./vm.py build

compile: $(TARGET)
	./compiler/main.py $(TARGET)

