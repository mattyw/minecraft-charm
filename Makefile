PROJECT_ROOT := $(shell cd ../..; pwd)

all: compose

compose:
	JUJU_REPOSITORY=$(PROJECT_ROOT) charm build -l debug

deploy:
	JUJU_REPOSITORY=$(PROJECT_ROOT) juju deploy local:trusty/minecraft


clean:
	$(RM) -r $(PROJECT_ROOT)/trusty/minecraft

.PHONY: all compose clean deploy
