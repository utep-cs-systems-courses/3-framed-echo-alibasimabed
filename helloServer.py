#! /usr/bin/env python3

# Echo server program

def pair(fd, addr):
    while True:
        data = fd.recv(100000)
        if len(data) == 0:
            break
        
        f_name = data.split(b',')[0]
        f_content = data.split(b',')[1]
        
        
        f_fd = os.open(f_name[1:-1], os.O_RDWR | os.O_CREAT)
        print(os.write(f_fd, f_content[2:-2]))


        #print(f_name[1:-1])
        #print(f_content[2:-2])

    print('client {} has disconnected'.format(addr))

import socket, sys, re, os, time
sys.path.append("lib")       # for params
import params

switchesVarDefaults = (
    (('-l', '--listenPort') ,'listenPort', 50001),
    (('-?', '--usage'), "usage", False), # boolean (set if present)
    )



progname = "echoserver"
paramMap = params.parseParams(switchesVarDefaults)

listenPort = paramMap['listenPort']
listenAddr = ''       # Symbolic name meaning all available interfaces

if paramMap['usage']:
    params.usage()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((listenAddr, listenPort))
s.listen(1)              # allow only one outstanding request
# s is a factory for connected sockets

while True:
    c_fd, c_addr = s.accept()
    print('new connection from', c_addr)

    pid = os.fork()
    if pid > 0:
        # This is the parent process
        c_fd.close()
    else:
        # This is the child process
        pair(c_fd, c_addr)



