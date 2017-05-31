def server(port):
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    serversocket.bind(('', int(port)))

    serversocket.listen(5)
    sock, addr= serversocket.accept()
    threading.Thread(target=messageListen, args=[sock]).start()

    serversocket.listen(5)
    fileListenerSock, addr= serversocket.accept()
    threading.Thread(target=serverFileListener, args=[fileListenerSock, serversocket]).start()

    while(True):
        print("Enter an option ('m', 'f', 'x'):\n"
              " (M)essage (send)\n"
              " (F)ile (request)\n"
              "e(X)it")
        opt = sys.stdin.readline()[:-1]

        if opt.lower() == 'f':
            print("Enter the name of the file you want: ")
            fileName = sys.stdin.readline()[:-1]
            fileListenerSock.send(fileName.encode())

            serversocket.listen(5)
            fileTransferSock, addr= serversocket.accept()

            fileWriter(fileTransferSock, fileName)
            
        elif opt.lower() == 'm':
            msg = sys.stdin.readline()
            sock.send(msg.encode())
            
        elif opt.lower() == 'x':
            sock.shutdown(socket.SHUT_WR)
            fileListenerSock.shutdown(socket.SHUT_WR)
            fileListenerSock.close()
            sock.close()
            sys.exit()
        
def client(port, server):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((server, int(port)))
    threading.Thread(target=messageListen, args=[sock]).start()

    fileListenerSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    fileListenerSock.connect((server, int(port)))
    threading.Thread(target=clientFileListener, args=[fileListenerSock, port, server]).start()
        
    while(True):
        print("Enter an option ('m', 'f', 'x'):\n"
              " (M)essage (send)\n"
              " (F)ile (request)\n"
              "e(X)it")
        opt = sys.stdin.readline()[:-1]

        if opt.lower() == 'f':
            print("Enter the name of the file you want: ")
            fileName = sys.stdin.readline()[:-1]
            fileListenerSock.send(fileName.encode())
            
            fileTransferSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            fileTransferSock.connect((server, int(port)))

            fileWriter(fileTransferSock, fileName)
            
        elif opt.lower() == 'm':
            msg = sys.stdin.readline()
            sock.send(msg.encode())
            
        elif opt.lower() == 'x':
            sock.shutdown(socket.SHUT_WR)
            fileListenerSock.shutdown(socket.SHUT_WR)
            fileListenerSock.close()
            sock.close()
            sys.exit()

def messageListen(sock):
    try:
       while(True):
            msg = sock.recv(1024)
            if(len(msg)):
                print("Other user: "+msg.decode(), end='')
            else:
                print("Connection has ended.")
                sys.exit()
                break
    except:
        print("Connection has ended.")
        sys.exit()

def serverFileListener(fileListenerSock, serversocket):
    try:
        while True:
            fileName = fileListenerSock.recv(1024).decode()
            if(len(fileName)):
                serversocket.listen(5)
                fileTransferSock, addr= serversocket.accept()
                try:
                    f = open(fileName, 'rb')
                    l = f.read()
                    fileTransferSock.sendall(l)
                    f.close()
                    print("Done sending.")
                    fileTransferSock.shutdown(socket.SHUT_WR)
                    fileTransferSock.close()
                except FileNotFoundError:
                    print("File not found.")
                    fileTransferSock.shutdown(socket.SHUT_WR)
                    fileTransferSock.close()
            else:
                print("Connection has ended.")
                sys.exit()
                break
    except:
        print("Connection has ended.")
        sys.exit()

def clientFileListener(fileListenerSock, port, server):
    try:
        while True:
            fileName = fileListenerSock.recv(1024).decode()
            if(len(fileName)):
                fileTransferSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                fileTransferSock.connect((server, int(port)))
                try:
                    f = open(fileName, 'rb')
                    l = f.read()
                    fileTransferSock.sendall(l)
                    f.close()
                    print("Done sending.")
                    fileTransferSock.shutdown(socket.SHUT_WR)
                    fileTransferSock.close()
                except FileNotFoundError:
                    print("File not found.")
                    fileTransferSock.shutdown(socket.SHUT_WR)
                    fileTransferSock.close()
            else:
                print("Connection has ended.")
                sys.exit()
                break
    except:
        print("Connection has ended.")
        sys.exit()
    

def fileWriter(fileTransferSock, fileName):
    fileBytes = fileTransferSock.recv(1024) 
    f = open(fileName, 'wb')
    while(fileBytes):
        f.write(fileBytes)
        fileBytes = fileTransferSock.recv(1024)
    f.close()
    if(os.stat(fileName).st_size == 0):
        os.remove(fileName)
        print("File not found.")
    else:
        print("Finished writing")

if __name__ == "__main__":
    import getopt
    import sys
    import threading
    import socket
    import os

    opts, args = getopt.getopt(sys.argv[1:], "l:s:p:")
    if(opts[0][0] == '-l'):
        port = opts[0][1]
    else:
        print("Incorrect usage.\n"
              "For servers, enter the following: py messenger.py -l <port number>"
              "For clients, enter the following: py messenger.py -l <port number> -s <server address>")
    if(len(opts) == 1): server(port)
    elif(len(opts) == 2):
        if(opts[1][0] == '-s'):
            serverAddress = opts[1][1]
            client(port, serverAddress)
        else:
            print("Incorrect usage.\n"
              "For servers, enter the following: py messenger.py -l <port number>"
              "For clients, enter the following: py messenger.py -l <port number> -s <server address>")
            




           
