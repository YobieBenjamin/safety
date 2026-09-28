.PHONY: all test experiment
# Pre-registration stage: the only artifact is docs/PREREGISTRATION.md (monitors and analysis are added later).
all: test
test:
	@test -s docs/PREREGISTRATION.md && grep -q 'decision rules' docs/PREREGISTRATION.md && echo 1/1 tests passed
experiment:
	@echo experiment not yet implemented
