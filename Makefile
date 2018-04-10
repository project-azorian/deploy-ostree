ifeq ($(OS),Windows_NT)
	PYTHON := py -3
else
	PYTHON := python3
endif

dummy:
	@echo please select a target explicitly

# plain linting/test targets
lint:
	flake8 .
	mypy . \
		--ignore-missing-imports \
		--check-untyped-defs

run-tests:
	$(PYTHON) setup.py test

qc/host: lint run-tests

# Debian
image/debian:
	docker build -t deploy-ostree-debian -f Dockerfile.debian .

qc/debian: image/debian
	docker run --rm -it --privileged deploy-ostree-debian

# combined targets for all Docker versions
qc: qc/debian
