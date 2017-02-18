import zmq
from flask import Flask

# flask setup
api = Flask(__name__)

# zmq setup
context = zmq.Context()
workers = context.socket(zmq.PUSH)
workers.bind("tcp://*:5557")
receiver = context.socket(zmq.PULL)
receiver.bind("tcp://*:5568")


@api.route("/", methods=['POST'])
def rpn_solve():
    workers.send_string("100")
    return "sent"


@api.route("/", methods=['GET'])
def rpn_get_result():
    result = receiver.recv()
    return result
