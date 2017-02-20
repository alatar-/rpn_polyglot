import logging


def configure_loggers():
    default_format = '%(asctime)s %(levelname)s\t%(name)s:\t%(message)s'
    default_date_format = '%H:%M:%S'
    default_formatter = logging.Formatter(default_format, default_date_format )

    logging.basicConfig(
        level=logging.INFO,
        format=default_format,
        datefmt=default_date_format
    )

    requestsFileHandler = logging.FileHandler("./logs/requests.log")
    requestsFileHandler.setFormatter(None)
    requestsFileHandler.setLevel(logging.DEBUG)
    requestsLogger = logging.getLogger("requestsLogger")
    requestsLogger.setLevel(logging.DEBUG)
    requestsLogger.addHandler(requestsFileHandler)

    consoleLogger = logging.getLogger("consoleLogger")
    consoleLogger.setLevel(logging.INFO)
