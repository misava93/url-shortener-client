import argparse
import logging
import os
from src.utils.logging import get_logger
import requests
from typing import Dict, List

# constants
APP_NAME = "SkillshareURLShortenerClient"
BACKEND_HOST_DEFAULT = "localhost"
BACKEND_HOST_KEY = "APP_BACKEND_HOST"
BACKEND_PORT_DEFAULT = "8080"
BACKEND_PORT_KEY = "APP_BACKEND_PORT"


def get_app_config(logger: logging.Logger):
    """
    returns configuration for the application
    :param logger: logger
    :return: dictionary containing configuration
    """
    app_config = {}

    for key, default in [(BACKEND_HOST_KEY, BACKEND_HOST_DEFAULT), (BACKEND_PORT_KEY, BACKEND_PORT_DEFAULT)]:
        try:
            app_config[key] = os.environ[key]
        except KeyError:
            logger.warning("The environment is not properly configured for the application. "
                           f"Missing key: {key}. Using default: {default}")
            app_config[key] = default

    logger.info(f"Will connect to service at port {app_config[BACKEND_PORT_KEY]} and host "
                f"{app_config[BACKEND_HOST_KEY]}")

    return app_config


def get_parser() -> argparse.ArgumentParser:
    """
    returns a command-line parser object for the application
    :return: parser object
    """
    parser = argparse.ArgumentParser(
        description="Client component of the URL Shortener application. It exposes a command-line interface (CLI) "
                    "that can be used to manage shortened URLs")

    group = parser.add_mutually_exclusive_group()

    # add arguments supported by the cli
    group.add_argument("-s", "--shorten", nargs="?", metavar="URL", type=str,
                       help="Shortens the provided URL")
    group.add_argument("-t", "--stats", nargs="?", metavar="URL", type=str,
                       help="Retrieves statistics around the shortened URL")
    group.add_argument("-d", "--disable", nargs="?", metavar="URL", type=str,
                       help="Disables the provided shortened URL")
    group.add_argument("-e", "--enable", nargs="?", metavar="URL", type=str,
                       help="Enables the provided shortened URL")

    return parser


def print_stats_for_link(response: Dict):
    """
    helper function that prints all the metadata associated with a shortened URL
    :param response: response from the URL statistics API
    """
    short_url = response["shortUrl"]
    metadata: List = response["metadata"] if response["metadata"] is not None else []
    num_hits = len(metadata)

    print(f"Stats for link: {short_url}")
    print(f"Times link has been opened: {num_hits}")

    print("Details:")
    for data in metadata:
        print(f"\t- IP: {data['ip']} | Date: {data['datetimeStr']} | User-Agent: {data['userAgent']}")


if __name__ == "__main__":
    parser = get_parser()
    args = parser.parse_args()
    logger = get_logger(APP_NAME)

    # get backend endpoint that handles the URL Shortener requests from configuration
    config = get_app_config(logger)
    host = config[BACKEND_HOST_KEY]
    port = config[BACKEND_PORT_KEY]

    # determine the action specified
    if args.shorten:
        # API: shorten URL
        # Method: POST
        # REST resource: /url
        url = args.shorten
        data = {"originalUrl": url}
        endpoint = f"http://{host}:{port}/url"
        response = requests.post(url=endpoint, json=data)

        if response.status_code == 200:
            short_url = response.json()["shortUrl"]
            print(f"Link has been shortened successfully. Shortened link: {short_url}")
        else:
            print(f"Received error from backend. Status code: {response.status_code}. Message: {response.text}")
    elif args.stats:
        # API: URL statistics
        # Method: GET
        # REST resource: /stats
        # REST query params: url
        url = args.stats
        params = {"url": url}
        endpoint = f"http://{host}:{port}/stats"
        response = requests.get(url=endpoint, params=params)

        if response.status_code == 200:
            print_stats_for_link(response.json())
        else:
            print(f"Received error from backend. Status code: {response.status_code}. Message: {response.text}")
    elif args.disable:
        # API: disable URL
        # Method: POST
        # REST resource: /disable
        url = args.disable
        data = {"url": url}
        endpoint = f"http://{host}:{port}/disable"
        response = requests.post(url=endpoint, json=data)

        if response.status_code == 200:
            short_url = response.json()["shortUrl"]
            print(f"Link {short_url} has been disabled successfully")
        else:
            print(f"Received error from backend. Status code: {response.status_code}. Message: {response.text}")
    elif args.enable:
        # API: enable URL
        # Method: POST
        # REST resource: /enable
        url = args.enable
        data = {"url": url}
        endpoint = f"http://{host}:{port}/enable"
        response = requests.post(url=endpoint, json=data)

        if response.status_code == 200:
            short_url = response.json()["shortUrl"]
            print(f"Link {short_url} has been enabled successfully")
        else:
            print(f"Received error from backend. Status code: {response.status_code}. Message: {response.text}")
    else:
        parser.print_help()
