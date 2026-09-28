.PHONY: test all
# Builds and tests every algorithm; fails if any fails.
test:
	@set -e; for d in algorithms/*/; do echo "== $$d"; $(MAKE) -C $$d test; done
all:
	@set -e; for d in algorithms/*/; do echo "== $$d"; $(MAKE) -C $$d all; done
