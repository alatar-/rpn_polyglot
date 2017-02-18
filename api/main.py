import zmq
from flask import Flask

context = zmq.Context()
api = Flask(__name__)

socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5555")


@api.route('/')
def hello():
    socket.send(b"Hello", 0)

    i = 0
    err = 0
    while True:
        try:
            message = socket.recv(0)
            i += 1
            break
            if str(message) == 'World':
                break
            print(message)
        except:
            err += 1
            print("err++")
    return str(message) + " " + str(err)


if __name__ == "__main__":
    api.run(host='0.0.0.0', port=8005, debug=True)
