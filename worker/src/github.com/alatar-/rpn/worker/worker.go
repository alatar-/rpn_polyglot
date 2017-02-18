package main

import (
    zmq "github.com/pebbe/zmq4"
    "strconv"
    "time"
    "fmt"
)

func main() {
    context, _ := zmq.NewContext()
    
    //  Socket to receive messages on
    receiver, _ := context.NewSocket(zmq.PULL)
    defer receiver.Close()
    receiver.Connect("tcp://localhost:5557")

    //  Socket to send messages to task sink
    sender, _ := context.NewSocket(zmq.PUSH)
    defer sender.Close()
    sender.Connect("tcp://localhost:5558")

    fmt.Println("Server listening...")
    //  Process tasks forever
    for {
        msgbytes, _ := receiver.Recv(0)
        fmt.Printf("%s.\n", string(msgbytes))

        //  Do the work
        msec, _ := strconv.ParseInt(string(msgbytes), 10, 64)
        time.Sleep(time.Duration(msec) * 1e6)

        //  Send results to sink
        sender.Send(msgbytes, 0)

    }
}