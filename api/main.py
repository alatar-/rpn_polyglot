import threading

import zmq
from flask import Flask

# flask setup
api = Flask(__name__)

# init threading
data = threading.local()
lock = threading.Lock()


def sink_thread():
    print("Sink accessed!")
    data.context = zmq.Context()  # new thread – new context
    data.receiver = data.context.socket(zmq.PULL)
    data.receiver.bind("tcp://*:5568")
    while True:
        result = data.receiver.recv()
        print(result)


with lock:
    print("Inside lock")
    if globals().get('sink_thread_running', True):
        global sink_thread_running
        sink_thread_running = False
        print("Inside block scope")

        data.context = zmq.Context()  # both zmq context and sockets must be local
        data.workers = data.context.socket(zmq.PUSH)
        data.workers.bind("tcp://*:5557")
        
        thread = threading.Thread(target=sink_thread)
        thread.start()
    else:
        print("Inside second scope")
        data.context = zmq.Context()  # both zmq context and sockets must be local
        data.workers = data.context.socket(zmq.PUSH)
        data.workers.connect("tcp://localhost:5557")

print("Outside lock")


@api.route("/", methods=['POST'])
def rpn_solve():
    workers.send_string("100")
    return "sent"


@api.route("/", methods=['GET'])
def rpn_get_result():
    return "null"