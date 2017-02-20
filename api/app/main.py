import logging
import threading

import zmq
from flask import Flask

# flask setup
api = Flask(__name__)

# threads-shared data
results = []

# get loggers
requestsLogger = logging.getLogger("requestsLogger")
consoleLogger = logging.getLogger("consoleLogger")

# init local thread data
# both zmq context and sockets must be local
data = threading.local()


def sink_thread():
    """
    Thread responsible for obtaining results
    from workers, timing the requests and saving
    the output to `results`.
    """
    # Init sink socket for getting results from workers
    data.context = zmq.Context()  # new thread – new context
    data.receiver = data.context.socket(zmq.PULL)
    data.receiver.bind("tcp://*:5558")
    
    consoleLogger.info("Sink process running!")
    while True:
        result = data.receiver.recv()
        results.append(str(result))


def api_thread():
    """Thread providing Flask-based API."""
    # Init socket for pushing input to workers
    data.context = zmq.Context()
    data.workers = data.context.socket(zmq.PUSH)
    data.workers.bind("tcp://*:5557")

    consoleLogger.info("API process running!")
    api.run()


@api.route("/rpn/solve", methods=['GET'])
def rpn_solve():
    """
    Endpoint to send input to RPN workers,
    stores current timestamp associated with
    job id for timing purposes.

    Returns 200 OK
    :rtype <json> (job_id)
    """
    data.workers.send_string("100")
    consoleLogger.info("100")
    return "sent"


@api.route("/rpn/collect", methods=['GET'])
def rpn_get_result():
    """
    Endpoint for obtaining the results.

    Returns 200 OK (for completed request)
    :rtype <json>

    Returns 202 Accepted (for uncompleted request)
    """
    consoleLogger.info("".join(results))
    return "".join(results)
