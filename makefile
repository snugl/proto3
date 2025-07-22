TARGET = prg/fib.snug

run: build


build: $(TARGET)
	./compiler/main.py $(TARGET)

