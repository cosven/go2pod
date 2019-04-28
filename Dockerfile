FROM golang:1.12.4-alpine
ENV GO111MODULE auto
ENV HTTP_PROXY http://172.17.0.1:8123
ENV HTTPS_PROXY http://172.17.0.1:8123
RUN apk add --no-cache git wget
RUN go get github.com/elves/elvish
WORKDIR /go/src/github.com/elves/elvish
RUN go build
