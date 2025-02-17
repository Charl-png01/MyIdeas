import socket
import json
import sys
from socket import socket, SOCK_STREAM, AF_INET
import select


def print_error(e, f=" "):
    print("Error in %s!" % (f))
    print(e)
    print(type(e))


def send_data(tcp_sock, data):
    try:
        json_data = json.dumps(data)
        ret = tcp_sock.send(json_data.encode('utf-8'))
        print("Sent %d bytes" % ret)
    except KeyboardInterrupt:
        raise KeyboardInterrupt()
    except Exception as e:
        print("Error sending data:", str(e))


def recv_data(tcp_sock):
    try:
        data = tcp_sock.recv(4096)
        data = data.decode('utf-8')
        print("Received %d bytes `%s'" % (len(data), data))
        return data
    except Exception as e:
        print_error(e, "recv")


def connect_to_server(host, port, user_name, rooms):
    try:
        tcp_sock = socket(AF_INET, SOCK_STREAM)
        tcp_sock.connect((host, port))
        print("Connected to the server.")

        connection_data = {
            "action": "connect",
            "user_name": "@" + user_name,
            "targets": ["#" + room for room in rooms]
        }

        print(json.dumps(connection_data))  # Print the connection data
        send_data(tcp_sock, connection_data)
        return tcp_sock
    except Exception as e:
        print_error(e, "connect_to_server")


def listen_to_server(tcp_sock):
    try:
        while True:
            readable, _, _ = select.select([tcp_sock, sys.stdin], [], [])
            for s in readable:
                if s is tcp_sock:
                    data = recv_data(tcp_sock)
                    if not data:
                        print("Server disconnected.")
                        sys.exit(0)
                    process_server_message(data)
                elif s is sys.stdin:
                    user_input = input("Enter data to send (or 'quit' to disconnect): ")
                    if user_input == 'quit':
                        disconnect(tcp_sock)
                        sys.exit(0)
                    else:
                        send_user_message(tcp_sock, user_input)
    except KeyboardInterrupt:
        disconnect(tcp_sock)
        print("Disconnected from the server.")
    except Exception as e:
        print_error(e, "listen_to_server")


def process_server_message(data):
    try:
        message = json.loads(data)
        if message.get("status") == "error":
            print("Error: " + message["message"])
        else:
            target = message.get("target")
            sender = message.get("from")
            message_text = message.get("message")
            if target and sender and message_text:
                print(f"Message from {sender} to {target}: {message_text}")
    except Exception as e:
        print_error(e, "process_server_message")


def send_user_message(tcp_sock, message_text):
    try:
        message_data = {
            "action": "message",
            "user_name": "@" + user_name,
            "target": "Specify the room or user you want to send the message to",
            "message": message_text
        }
        send_data(tcp_sock, message_data)
        print(f"Sent to server: {message_text}")  # Print sent message
    except Exception as e:
        print_error(e, "send_user_message")


def disconnect(tcp_sock):
    try:
        disconnect_data = {"action": "disconnect"}
        send_data(tcp_sock, disconnect_data)
        print("Disconnected from the server.")
    except Exception as e:
        print_error(e, "disconnect")


if __name__ == "__main__":
    host = sys.argv[1]
    port = int(sys.argv[2])
    user_name = input("Please enter your name: ")
    rooms_input = input("Enter the rooms you would like to listen to separated by commas: ")
    rooms = rooms_input.split(',')

    tcp_sock = connect_to_server(host, port, user_name, rooms)
    listen_to_server(tcp_sock)




