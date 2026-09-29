.PHONY: all test experiment
all: test
test:
	@test -s docs/PREREGISTRATION.md && grep -q 'EUREKA criterion' docs/PREREGISTRATION.md && echo 1/1 tests passed
experiment:
	@echo awaiting seed 5
