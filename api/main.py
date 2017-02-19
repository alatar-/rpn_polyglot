import logging
import threading

import zmq
from flask import Flask

from app import helpers


# flask setup
api = Flask(__name__)

# get loggers
requestsLogger = logging.getLogger("requestsLogger")
consoleLogger = logging.getLogger("consoleLogger")

# init local thread data
# both zmq context and sockets must be local
data = threading.local()

# threads-shared data
results = []


def sink_thread():
    global results

    # Init sink socket for getting results from workers
    data.context = zmq.Context()  # new thread – new context
    data.receiver = data.context.socket(zmq.PULL)
    data.receiver.bind("tcp://*:5558")
    
    consoleLogger.info("Sink process running!")
    while True:
        result = data.receiver.recv()
        results.append(str(result))


def api_thread():
    # Init socket for pushing input to workers
    data.context = zmq.Context()
    data.workers = data.context.socket(zmq.PUSH)
    data.workers.bind("tcp://*:5557")

    consoleLogger.info("API process running!")
    api.run()


@api.route("/rpn/solve", methods=['GET'])
def rpn_solve():
    data.workers.send_string("100")
    return "sent"


@api.route("/rpn/collect", methods=['GET'])
def rpn_get_result():
    return "".join(results)


if __name__ == '__main__':
    helpers.configure_loggers()
    thread = threading.Thread(target=sink_thread)
    thread.start()
    api_thread()
