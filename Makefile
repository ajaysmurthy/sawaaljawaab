build:
	docker build -t mtg-docker.sb.upf.edu/sawaaljawaab .

push:
	docker push mtg-docker.sb.upf.edu/sawaaljawaab

all: build push

.PHONY: build push all
