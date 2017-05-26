def server(port):
    # create a communicator object
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    #binds to available interfaces
    serversocket.bind(('', int(port)))

    #listens for conncetions and accept
    serversocket.listen(5)
    sock, addr= serversocket.accept()
    threading.Thread(target=optionHandler, args=[sock]).start()
    threading.Thread(target=optionReceive, args=[sock]).start()

    
def client(port, server):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((server, int(port)))
    threading.Thread(target=optionHandler, args=[sock]).start()
    threading.Thread(target=optionReceive, args=[sock]).start()
    
def optionHandler(sock):
    while(True):
        opt = input("Enter an option ('m', 'f', 'x'):\n"
                    " (M)essage (send)\n"
                    " (F)ile (request)\n"
                    "e(X)it\n")

        if opt.lower() == 'f':
            sock.send(opt.encode())
            recvFile(sock)

        elif opt.lower() == 'm':
            sock.send(opt.encode())
            sendMessage(sock)

        elif opt.lower() == 'x':
            break
    
def optionReceive(sock):
    while(True):
        msg = sock.recv(1024)
        if msg.decode().lower() == 'f':
            sendFile(sock)

        elif msg.decode().lower() == 'm':
            recvMessage(sock)
            
        elif msg.decode().lower() == 'x':
            print('exit')


def sendMessage(sock):
    msg = sys.stdin.readline()
    sock.send(msg.encode())
        
def recvMessage(sock):
    msg = sock.recv(1024)
    print(msg.decode(), end='')
        
def sendFile(sock):
    fileName = sock.recv(1024)
    f = open(fileName, 'rb')
    l = f.read()
    f.close()
    print("Sending...")
    sock.sendall(l)
    sock.shutdown(socket.SHUT_WR)
    print("Done sending")

def recvFile(sock):
    fileName = input("What file do you want to receive?: ")
    sock.send(fileName.encode())
    f = open(fileName, 'wb')
    l = sock.recv(1024)
    while (l):
        print("Writing..")
        f.write(l)
        l = sock.recv(1024)
    f.close()
    print("Done writing")

if __name__ == "__main__":
    import getopt
    import sys
    import threading
    import socket

    #gets command line arguments
    opts, args = getopt.getopt(sys.argv[1:], "l:")

    #run server if the command line includes '-l'
    if len(opts) == 1:
        server(opts[0][1])
    #runs client if there is no '-l' argument
    else:
        client(args[0], args[1])

