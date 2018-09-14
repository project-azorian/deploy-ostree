ifeq ($(OS),Windows_NT)
	PYTHON := py -3
else
	PYTHON := python3
endif

all: lint test/unit test/provisioners build/wheel build/docker test/integration test/integration_long

# local checks
define pytest
    $(PYTHON) -m pytest \
		--verbose \
		--junitxml=build/test.xml \
		$(1)
endef

build:
	mkdir -p build

lint: build
	flake8 .
	mypy --junit-xml=build/mypy.xml .

test/unit:
	$(call pytest,tests/unit)

test/provisioners:
	$(call pytest,tests/builtin_provisioners)

test/_local/integration:
	$(call pytest,tests/integration)

test/_local/integration_long:
	$(call pytest,tests/integration_long)

# package
build/wheel: clean/wheels
	$(PYTHON) setup.py bdist_wheel

build/docker:
	docker build -t $(IMAGE_TAG) --build-arg PACKAGE=$(shell ls -1 dist/*.whl | xargs basename) .

# dockerized tests
IMAGE_TAG := deploy-ostree

define docker_test
	docker run --rm -i \
		--privileged \
		--volume /ostree \
		--volume /tmp/deploy-ostree.test/sysroot \
		--volume $(shell pwd):/src \
		--workdir /src \
		$(IMAGE_TAG) \
		make $(1)
endef

test/integration:
	$(call docker_test,test/_local/integration)

test/integration_long:
	$(call docker_test,test/_local/integration_long)

# push to PyPI
release/test:
	twine upload --repository-url https://test.pypi.org/legacy/ dist/*.whl

release/pypi:
	twine upload --repository-url https://upload.pypi.org/legacy/ dist/*.whl

# cleanup
clean: clean/wheels
	-rm -rf build
	-docker image rm $(IMAGE_TAG)

clean/wheels:
	-rm -rf dist/*.whl
