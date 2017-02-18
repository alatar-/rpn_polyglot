package main

import (
    zmq "github.com/pebbe/zmq4"
    "time"
    "fmt"
)

func main() {
    context, _ := zmq.NewContext()
    socket, _ := context.NewSocket(zmq.REP)
    // defer context.Close()
    defer socket.Close()
    socket.Bind("tcp://*:5555")

    fmt.Println("Server listening...")
    // Wait for messages
    for {
        msg, _ := socket.Recv(0)
        println("Received ", string(msg))

        // foo := "Fooo"
        // socket.Send(foo, 1)
        // socket.Send(foo, 1)
        // socket.Send(foo, 1)
        // socket.Send(foo, 1)
        // for i := 0; i < 2; i++ {
            
        //     // subscribers don't get all messages if publisher is too fast
        //     // a one microsecond pause may still be too short
        //     time.Sleep(time.Second)
        // }

        // do some fake "work"
        time.Sleep(time.Microsecond)

        // send reply back to client
        reply := "World"
        socket.Send(reply, 0)
    }
}