import sys
import zmq
import random
import time

context = zmq.Context()
workers = context.socket(zmq.PUSH)
workers.bind("tcp://*:5557")

for task_nbr in range(100):
    workload = random.randint(1, 100)
    workers.send_string(u'%i' % task_nbr)
    print("Sending workload %d" % workload)


# Socket to receive messages on
receiver = context.socket(zmq.PULL)
receiver.bind("tcp://*:5558")

# Start our clock now
tstart = time.time()

# Process 100 confirmations
for task_nbr in range(100):
    s = receiver.recv()
    if task_nbr % 10 == 0:
        sys.stdout.write(':')
    else:
        sys.stdout.write('.')
    sys.stdout.flush()

# Calculate and report duration of batch
tend = time.time()
print("Total elapsed time: %d msec" % ((tend-tstart)*1000))
