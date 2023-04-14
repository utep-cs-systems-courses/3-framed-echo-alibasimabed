#! /usr/bin/env python3


import socket, sys, re, time, os


switchesVarDefaults = (
    (('-s', '--server'), 'server', "127.0.0.1:50000"),
    (('-d', '--delay'), 'delay', "0"),
    (('-?', '--usage'), "usage", False), # boolean (set if present)
    )


server = '127.0.0.1:50000'
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



sys.argv.pop(0)

for i in sys.argv:
    file_ = os.open(i, os.O_RDONLY | os.O_CREAT)
    msg = os.read(file_, 1000)
    msg = msg.replace(b'/',b'//')
    msg = msg.replace(b'{}',b'{{}}')
    s.send(bytes(i,encoding='utf8'))
    s.send(b'{}e')
    s.send(msg)
    s.send(b'{}e')

s.send(b'/e')

s.close()
