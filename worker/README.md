## Req

- _go_ (`brew install go`)
- _zeromq_ (`brew install zeromq`)A

## Setup

- set Go workspace (`set -U GOPATH (pwd)`)
- add `$GOPATH/bin` to your `$PATH`
- install _godep_ (`go get godep`)
- install dependencies (`godep restore` in package dir)

## Run

You can run multiple workers at the same time.

	./bin/worker

