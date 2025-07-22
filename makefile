TARGET = prg/main.snug


run: build


build: $(TARGET)
	./compiler/main.py $(TARGET)

