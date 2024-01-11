# client.py
import socket
import threading

def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            print(message)
        except Exception as e:
            print(f"Error receiving message: {e}")
            break

def main():
    host = input("Enter server IP: ")
    port = 5000

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    username = input("Enter your username: ")
    room = input("Enter room name: ")

    join_data = {'username': username, 'room': room}
    client_socket.send(str(join_data).encode('utf-8'))

    receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
    receive_thread.start()

    while True:
        message = input()
        if message.lower() == 'exit':
            leave_data = {'username': username, 'room': room}
            client_socket.send(str(leave_data).encode('utf-8'))
            break
        else:
            send_data = {'msg': message, 'room': room}
            client_socket.send(str(send_data).encode('utf-8'))

    receive_thread.join()
    client_socket.close()

if __name__ == '__main__':
    main()
