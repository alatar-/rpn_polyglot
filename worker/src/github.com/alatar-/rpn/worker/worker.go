package main

import (
    zmq "github.com/pebbe/zmq4"
    rpn "github.com/irlndts/go-rpn"
    "bytes"
    "strings"
    "strconv"
    "time"
    "math/rand"
    "log"
)

func main() {
    context, _ := zmq.NewContext()
    
    log.Println("Connecting to incoming data socket (PULL)...")
    receiver, _ := context.NewSocket(zmq.PULL)
    defer receiver.Close()
    receiver.Connect("tcp://localhost:5557")

    log.Println("Connecting to outgoing results [sink] socket (PUSH)...")
    sender, _ := context.NewSocket(zmq.PUSH)
    defer sender.Close()
    sender.Connect("tcp://localhost:5558")

    for {
        log.Println("Worker ready...")

        msgbytes, _ := receiver.Recv(0)
        log.Println("Received new job, processing...")

        msgstr := string(msgbytes)
        req := strings.Split(msgstr, "\n")
        // ... handle request validation ...
        jobId, jobNumStr, jobInputs := req[0], req[1], req[2:]
        log.Println("ID", jobId, "| processing", jobNumStr, "RPNs")
        jobNum, _ := strconv.Atoi(jobNumStr)

        var response bytes.Buffer
        response.WriteString(jobId)

        for i := 0; i < jobNum; i++ {
            rpnResult, _ := rpn.Calc(jobInputs[i])
            rpnResultStr := strconv.FormatFloat(rpnResult, 'f', 10, 64)
            response.WriteString("\n")
            response.WriteString(rpnResultStr)

            log.Println("ID", jobId, "|", i, "|", rpnResult)
        }

        time.Sleep(time.Duration(rand.Intn(500)) * time.Millisecond)

        log.Println("Processing finished. Sending output...")
        sender.Send(response.String(), 0)
    }
}