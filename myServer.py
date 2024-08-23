import socket
import threading

client_sockets = []

HOST = "192.168.1.43"
PORT = 5123

server_socket = socket.socket()
server_socket.bind((HOST, PORT))
server_socket.listen(5)
print(f"Server listening on {HOST}:{PORT}")

def handle_client(client_socket):
    while True:
        message = client_socket.recv(1024).decode()
        if not message:
            break
        else:
            for socket in client_sockets:
                if socket != client_socket:
                    socket.send(message.encode())
    client_socket.close()
    client_sockets.remove(client_socket)
    print("Client disconnected.")

while True:
        client_socket, address = server_socket.accept()
        print(f"Accepted connection from {address}")
        client_sockets.append(client_socket)
        thread = threading.Thread(target=handle_client, args=(client_socket,))
        thread.start()