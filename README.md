# Overview
This repository is part of a URL Shortener application for Skillshare, more specifically,
it exposes a command-line interface (CLI) that can be used to submit requests to the URL shortener service.

Relevant notes:
- The service is containerized using Docker
- This application currently can only be run locally out of the box
- CLI tool is implemented in Python 3

# Dependencies
The only dependencies needed to run this application locally are:
- [Docker](https://docs.docker.com/get-docker/)
- [GNU make tool](https://www.gnu.org/software/make/manual/make.html)

# Usage
In order to build and expose the backend service, run the following command:
```shell script
make docker-image-run
```

The above command will build the Docker image that contains the URL Shortener CLI and it will then expose it inside a
local container. Once the command finishes running you will have access to a terminal that can be used to interact
with the CLI.

## CLI functionality
The CLI exposes the following functionality:

> All the subsequent commands are meant to be run within the container created in previous step

### Shortening a URL
To shorten a URL, run the following command from the terminal:
```shell script
./bin/skillshare --shorten [URL]
```

Example:
```shell script
./bin/skillshare --shorten https://www.google.com
```

### URL Statistics
To return statistics about shortened URLs, run the following command from the terminal:
```shell script
./bin/skillshare --stats [original URL | shortened URL]
```

### Disable Shortened URL
To disable a shortened URL, run the following command from the terminal:
```shell script
./bin/skillshare --disable [original URL | shortened URL]
```
> A disabled shortened URL cannot be accessed, that is, it will not redirect you to the original URL associated with it

### Enable Shortened URL
To enable a shortened URL, run the following command from the terminal:
```shell script
./bin/skillshare --enable [original URL | shortened URL]
```
