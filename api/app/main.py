import logging
import threading
import time

import zmq
from flask import Flask, request, jsonify

# flask setup
api = Flask(__name__)

# threads-shared data
results = {}  # results obtained from the workers
last_job_id = 0  # last request job id

# get loggers
requestsLogger = logging.getLogger("requestsLogger")
consoleLogger = logging.getLogger("consoleLogger")

# init local thread data
# both zmq context and sockets must be local
thread_data = threading.local()


def sink_thread():
    """
    Thread responsible for obtaining results
    from workers, timing the requests and saving
    the output to `results`.
    """
    global results

    # Init sink socket for getting results from workers
    thread_data.context = zmq.Context()  # new thread – new context
    thread_data.receiver = thread_data.context.socket(zmq.PULL)
    thread_data.receiver.bind("tcp://*:5558")
    
    consoleLogger.info("Sink process running!")
    while True:
        # Recieve and decode response
        data = thread_data.receiver.recv()
        data = data.decode('utf-8').split("\n", 1)
        job_id, job_output = int(data[0]), data[1]
        consoleLogger.info("Recieved output for job {}".format(job_id))

        # store the result
        results[job_id]['time'] = time.time() - results[job_id]['time']
        results[job_id]['output'] = job_output

        # log to file
        requestsLogger.info("output job={}\n{} {:f}".format(job_id, job_output, results[job_id]['time']))


def api_thread():
    """Thread providing Flask-based API."""
    # Init socket for pushing input to workers
    thread_data.context = zmq.Context()
    thread_data.workers = thread_data.context.socket(zmq.PUSH)
    thread_data.workers.bind("tcp://*:5557")

    consoleLogger.info("API process running!")
    api.run()


@api.route("/rpn/solve", methods=['POST'])
def rpn_solve():
    """
    Endpoint to send input to RPN workers,
    stores current timestamp associated with
    job id for timing purposes.

    Returns 200 OK
    :rtype <json> (job_id)
    """
    if 'rpn' not in request.json:
        return "Wrong request", 400
    
    global last_job_id
    global results
    
    last_job_id += 1
    requestsLogger.info("input job=%d" % last_job_id)

    # process input
    input_rpn_data = request.json['rpn']
    # ... validate the input ...
    requestsLogger.info(input_rpn_data)

    results[last_job_id] = {'time': time.time()}
    thread_data.workers.send_string(
        "{:d}\n{}".format(last_job_id, input_rpn_data)
    )

    return jsonify({
        'message': "RPN solving request has been scheduled. Query for result with provided job id.",
        'job_id': last_job_id
    })


@api.route("/rpn/collect/<int:job_id>", methods=['GET'])
def rpn_get_result(job_id):
    """
    Endpoint for obtaining the results.

    Returns 200 OK (for completed request)
    :rtype <json>

    Returns 202 Accepted (for uncompleted request)
    """
    global results

    if not results.get(job_id):
        return "Bad request id.", 400

    if results[job_id].get('output'):
        return jsonify({
            'result': results.pop(job_id),
            'job_id': job_id
        })
    else:
        return jsonify({
            'message': "Results are not ready yet.",
            'job_id': job_id,
        }), 202
