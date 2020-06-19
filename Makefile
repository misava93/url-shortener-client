# constants
APP = skillshare-url-shortener-client
DOCKER_GEN_REQ_TARGET = generate-requirements
DOCKER_TARGET = url-shortener-cli

.PHONY: docker-image-build-gen-requirements
docker-image-build-gen-requirements: Dockerfile
	@echo "Building Docker image used to generate requirements file with python pinned dependencies"
	docker build --target ${DOCKER_GEN_REQ_TARGET} -t ${APP}/${DOCKER_GEN_REQ_TARGET} .

.PHONY: generate-image-run-gen-requirements
generate-image-run-gen-requirements: docker-image-build-gen-requirements
	@echo "Cleaning containers"
	docker container prune -f
	@echo "Running Docker container to generate requirements file with python pinned dependencies"
	docker run --volume ${CURDIR}/requirements:/requirements --rm --name ${DOCKER_GEN_REQ_TARGET} ${APP}/${DOCKER_GEN_REQ_TARGET}

requirements/main.txt: requirements/main.in
	${MAKE} generate-image-run-gen-requirements
	touch requirements/main.txt

.PHONY: docker-image-build
docker-image-build: Dockerfile
	@echo "Building Docker image with containerized URL Shortener Client (CLI)"
	docker build --target ${DOCKER_TARGET} -t ${APP}/${DOCKER_TARGET} .

.PHONY: docker-image-run
docker-image-run: docker-image-build
	@echo "Cleaning containers"
	docker container prune -f
	@echo "Running Docker container with containerized URL Shortener Client (CLI"
	docker run -it --network skillshare-net --rm --name ${DOCKER_TARGET} ${APP}/${DOCKER_TARGET}
