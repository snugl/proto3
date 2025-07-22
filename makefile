TARGET = prg/fib.snug

run: compile


compile: $(TARGET)
	./compiler/main.py $(TARGET)

