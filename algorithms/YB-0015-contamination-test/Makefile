.PHONY: all build test experiment clean
export PYTHONPATH := .:src
all: test experiment
build: src/libcore.so
src/libcore.so: src/vitals.c
	gcc -O2 -Wall -Wextra -Werror -shared -fPIC -o $@ $< -lm
test: build
	python3 -m py_compile src/*.py tests/*.py
	python3 tests/test_core.py
experiment: build
	python3 tests/experiment.py
clean:
	rm -f src/libcore.so
