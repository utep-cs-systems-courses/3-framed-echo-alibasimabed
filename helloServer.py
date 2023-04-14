#! /usr/bin/env python3

from threading import Thread, enumerate, Lock


files_open = set()
files_lock = Lock()

class Worker(Thread):
    def __init__(self, c__fd, c__addr):
        Thread.__init__(self);
        Worker.c_fd = c__fd
        Worker.c_addr = c__addr
    def run(self):
        pair(self.c_fd, self.c_addr)

def decode_data(data):
    msg = b''
    eof = False
    if b'/e' not in data:

        msg += data.replace(b'//', b'/')
    else:
        msg += data.split(b'/e')[0].replace(b'//', b'/')
        eof = True
    return msg, eof


def pair(fd, addr):
    msg = b''
    while True:
        data = fd.recv(100000)
        msg_, eof = decode_data(data)
        msg += msg_
        if eof:
            break


    msg = msg.split(b'{}e')
    print(msg)

    for i,k in zip(msg[0::2], msg[1::2]):
        if i not in files_open:
            files_lock.acquire()
            files_open.add(i)
            files_lock.release()
            fd = os.open( i, os.O_RDWR|os.O_CREAT )
            os.write(fd, k)
            os.close(fd)
            files_lock.acquire()
            files_open.remove(i)
            files_lock.release()

    print(files_open)
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

os.chdir('files')


while True:
    c_fd, c_addr = s.accept()
    print('new connection from', c_addr)
    work = Worker(c_fd,c_addr)
    work.start()


#print(decode_data(b'ajsksdvksv//ereun/efe'))

