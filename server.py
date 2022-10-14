import socket
import threading

HOST = '127.0.0.1'
PORT = 9090

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))

server.listen()

clients = []
nicknames = []


def broadcast(message):
    '''
        Sends one message to all the connected clients.
        Passes an encoded message and send it directly to all the clients
    '''
    for client in clients:
        client.send(message)

def handle(client):
    '''
        handle individual connections to the client
        (once a client is being accepted in the server, the whole connection and handling of connection is going to be written here)
    '''
    while True:
        try:
            message = client.recv(1024)
            print(f"{nicknames[clients.index(client)]} says {message}")
            broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            print(f"{nicknames[clients.index(client)]} left the chat")
            broadcast(message)
            nickname = nicknames[index]
            nicknames.remove(nickname)
            break


def receive():
    '''
        Accepts new connections, new clients connecting.
    '''
    while True:
        client, address = server.accept()
        print(f"Connected with {str(address)}!")

        client.send("NICK".encode('utf-8'))
        nickname = client.recv(1024)
        nicknames.append(nickname)
        clients.append(client)

        print(f"Nickname of the client is: {nickname}")
        broadcast(f"{nickname} joined chat!\n".encode('utf-8'))
        client.send("Connected to the server".encode('utf-8'))

        thread = threading.Thread(target = handle, args = (client,))
        thread.start()


print("Server running...")
receive()