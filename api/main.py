import threading

import zmq
from flask import Flask

# flask setup
api = Flask(__name__)

# init local thread data
# both zmq context and sockets must be local
data = threading.local()

# threads-shared results
results = []


def sink_thread():
    global results

    # Init sink socket
    data.context = zmq.Context()  # new thread – new context
    data.receiver = data.context.socket(zmq.PULL)
    data.receiver.bind("tcp://*:5558")
    
    print("Sink process running!")
    while True:
        result = data.receiver.recv()
        results.append(str(result))


def api_thread():
    data.context = zmq.Context()
    data.workers = data.context.socket(zmq.PUSH)
    data.workers.bind("tcp://*:5557")

    print("API process running!")
    api.run()


@api.route("/solve_rpn", methods=['GET'])
def rpn_solve():
    data.workers.send_string("100")
    return "sent"


@api.route("/get_rpn_result", methods=['GET'])
def rpn_get_result():
    return "".join(results)


if __name__ == '__main__':
    thread = threading.Thread(target=sink_thread)
    thread.start()
    api_thread()
