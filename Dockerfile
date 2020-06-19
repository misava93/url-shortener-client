# Docker image stage to update and generate requirements file containing python pinned dependencies
# NOTE: when running the image within a container, it expects a volume containing a 'requirements' directory
# to be mounted at the image's final working directory. This directory should contain the below
# pip-tools requirements file
FROM python:3.7.6-slim AS generate-requirements
RUN pip install pip-tools
CMD ["pip-compile", "--generate-hashes", "--output-file", "requirements/main.txt", "requirements/main.in"]

# Docker image stage with recipe to build containerized Skillshare Url Shortener Client (i.e. CLI) application
FROM python:3.7.6-slim AS url-shortener-cli
# specify configuration to be passed at image build time
ARG USER=skillshare
ARG HOME=/home/$USER
# set default endpoint to localhost
ARG BACKEND_ENDPOINT="127.0.0.1"

# set environmental variables for the image
ENV USER=${USER}
ENV HOME=${HOME}
ENV BACKEND_ENDPOINT=${BACKEND_ENDPOINT}
ENV APP_BACKEND_HOST="url-shortener-service"
ENV APP_BACKEND_PORT="8080"

# change default shell to bash
SHELL ["/bin/bash", "-c"]

# setup steps that require root access
## setup user that will be used for subsequent non-sudo commands and to run the application
RUN groupadd -r ${USER} && useradd -r -g ${USER} ${USER}
RUN mkdir ${HOME}
RUN chown ${USER} ${HOME}

# setup steps that dont require root access
## change user
USER ${USER}:${USER}
RUN echo "USER: ${USER}"
## setup working directory
WORKDIR ${HOME}
RUN echo "HOME: ${HOME}"

# application-level steps
## copy relevant source code
ENV APP_DIR=${HOME}/skillshare-url-shortener-client
RUN mkdir ${APP_DIR}
WORKDIR ${APP_DIR}
## copy files that contain pip-tools requirement files with python dependencies needed
COPY --chown=${USER}:${USER} requirements requirements

## activate virtual env and install core dependencies
RUN python -m venv .venv
RUN source .venv/bin/activate && pip install --upgrade pip && pip install pip-tools
## activate virtual env and install app dependencies
RUN source .venv/bin/activate && pip-sync requirements/main.txt
## only copy needed assets
COPY --chown=${USER}:${USER} bin bin
COPY --chown=${USER}:${USER} src src

ENV PYTHONPATH="${APP_DIR}:${APP_DIR}/.venv/lib/python3.7/site-packages/"

CMD ["/bin/bash"]
