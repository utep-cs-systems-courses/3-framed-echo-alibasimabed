#! /usr/bin/env python3

# Echo client program
import socket, sys, re, time, os
sys.path.append("../lib")       # for params
#import params

switchesVarDefaults = (
    (('-s', '--server'), 'server', "127.0.0.1:50001"),
    (('-d', '--delay'), 'delay', "0"),
    (('-?', '--usage'), "usage", False), # boolean (set if present)
    )


#progname = "framedClient"
#paramMap = params.parseParams(switchesVarDefaults)

#server, usage  = paramMap["server"], paramMap["usage"]

#if usage:
#    params.usage()

server = '127.0.0.1:50001'
delay = 0

try:
    serverHost, serverPort = re.split(":", server)
    serverPort = int(serverPort)
except:
    print("Can't parse server:port from '%s'" % server)
    sys.exit(1)

s = None
for res in socket.getaddrinfo(serverHost, serverPort, socket.AF_UNSPEC, socket.SOCK_STREAM):
    af, socktype, proto, canonname, sa = res
    try:
        print("creating sock: af=%d, type=%d, proto=%d" % (af, socktype, proto))
        s = socket.socket(af, socktype, proto)
    except socket.error as msg:
        print(" error: %s" % msg)
        s = None
        continue
    try:
        print(" attempting to connect to %s" % repr(sa))
        s.connect(sa)
    except socket.error as msg:
        print(" error: %s" % msg)
        s.close()
        s = None
        continue
    break

if s is None:
    print('could not open socket')
    sys.exit(1)

delay = float(delay) # delay before reading (default = 0s)
if delay != 0:
    print(f"sleeping for {delay}s")
    time.sleep(int(delay))
    print("done sleeping")


#fd_1 = os.open('ff', os.O_RDONLY)
#s.send(os.read(fd_1,1024))


for i in sys.argv:
    file_ = os.open(i, os.O_RDONLY | os.O_CREAT)
    s.send(b'{' + bytes(i, 'utf-8') + b'}' + b',' +  b'{{' + os.read(file_, 1000) + b'}}')
    time.sleep(2)

#s.close()
