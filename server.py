# server.py

import socket
import threading

HOST = '127.0.0.1'
PORT = 1234
LISTENER_LIMIT = 5
active_clients = []
active_clients_lock = threading.Lock()
all_messages = []  # nova lista za sve poruke

def broadcast(message, sender_username):
    with active_clients_lock:
        for user in active_clients:
            if user[0] != sender_username:
                send_message_to_client(user[1], message)

def send_message_to_client(client, message):
    client.sendall(message.encode())

def send_all_messages_to_client(client):
    with active_clients_lock:
        for message in all_messages:
            send_message_to_client(client, message)

def handle_client(client, username):
    with active_clients_lock:
        active_clients.append((username, client))

    try:
        send_all_messages_to_client(client)  # šalje sve poruke klijentu kada se poveže
        while True:
            message = client.recv(2048).decode('utf-8')
            if not message:
                break
            formatted_message = f"{username}: {message}"
            broadcast(formatted_message, username)
            all_messages.append(formatted_message)  # dodaj poruku u listu svih poruka
    except Exception as e:
        print(f"Error handling client {username}: {e}")
    finally:
        with active_clients_lock:
            active_clients.remove((username, client))
        client.close()

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        server.bind((HOST, PORT))
        print(f"Running the server on {HOST}:{PORT}")
    except Exception as e:
        print(f'Unable to bind to host {HOST} and port {PORT}: {e}')

    server.listen(LISTENER_LIMIT)

    while True:
        client, address = server.accept()
        print(f'Successfully connected to client {address[0]} {address[1]}')

        username = client.recv(2048).decode('utf-8')
        if username:
            threading.Thread(target=handle_client, args=(client, username)).start()
        else:
            print("Client username is empty")

if __name__ == '__main__':
    main()
