PROJECT_ROOT := $(shell cd ../..; pwd)

all: compose

compose:
	JUJU_REPOSITORY=$(PROJECT_ROOT) charm build -l debug

deploy:
	JUJU_REPOSITORY=$(PROJECT_ROOT) juju deploy local:trusty/minecraft

clean:
	$(RM) -r $(PROJECT_ROOT)/trusty/minecraft

proof:
	JUJU_REPOSITORY=$(PROJECT_ROOT) charm proof

test: compose
	(cd $(PROJECT_ROOT)/trusty/minecraft; ./tests/01-listening)

.PHONY: all compose clean deploy test proof
