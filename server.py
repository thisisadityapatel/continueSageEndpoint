import uvicorn
import certifi, ssl
import logging
import sys

# Setting up logging
logger = logging.getLogger(__name__)


def setup_logging():
    FORMAT = (
        "%(levelname)s:%(name)s: %(message)s (%(asctime)s; %(filename)s:%(lineno)d)"
    )
    DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
    LEVEL = logging.INFO
    STREAM = sys.stdout
    logging.basicConfig(
        level=LEVEL,
        format=FORMAT,
        datefmt=DATE_FORMAT,
        stream=STREAM,
    )


if __name__ == "main__":
    setup_logging()
    sslcontext = ssl.create_default_context(cafile=certifi.where())
    uvicorn.run("main:app", port=11434)
