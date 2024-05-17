# use the gloang:alpine base image
FROM golang:alpine

# set the working directory to /go/src/app
WORKDIR /go/src/app

# copy all the files from the current directory to the container working dir

ADD . /go/src/app/

# import dependencies using 'go mod init' 
# and build the application using 'go build -o helloworld'
RUN go mod init 
RUN go build -o helloworld

# expose the port 6111
EXPOSE 6111

# start the container by invoking the binary created earlier, which is  `./helloworld`
CMD [ "./helloworld" ]
