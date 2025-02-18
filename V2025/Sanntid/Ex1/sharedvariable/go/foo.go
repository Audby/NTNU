// Use `go run foo.go` to run your program

package main

import (
	"fmt"
	"runtime"
)

type operation int

const (
	increment operation = iota
	decrement
	get
	quit
)

type request struct {
	op   operation
	resp chan int
}

func numberServer(reqChan chan request) {
	var i int = 0
	for {
		req := <-reqChan
		switch req.op {
		case increment:
			i++
		case decrement:
			i--
		case get:
			req.resp <- i
		case quit:
			// Optionally signal termination if needed
			close(reqChan)
			return
		}
	}
}

func incrementing(incrementChan chan bool) {
	for j := 0; j < 1000000; j++ {
		reqChan <- request{op: increment}
	}
}

func decrementing(decrementChan chan bool) {
	for j := 0; j < 1000000; j++ {
		reqChan <- request{op: decrement}
	}
}

func main() {

	runtime.GOMAXPROCS(2)

	reqChan := make(chan request)
	go numberServer(reqChan)

	go incrementing(reqChan)
	go decrementing(reqChan)

	var dummy string
	fmt.Scanln(&dummy)

	respChan := make(chan int)
	reqChan <- request{op: get, resp: respChan}
	finalValue := <-respChan

	fmt.Println("The magic number is:", finalValue)
}
