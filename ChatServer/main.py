import socket
import json
import select

# Define size limits
USER_NAME_LIMIT = 60
TARGET_LIMIT = 60
MESSAGE_LIMIT = 3800
MAX_MESSAGE_SIZE = 4096

# Create a dictionary to store connected clients, subscriptions, and message queues
clients = {}
subscriptions = {}
message_queues = {}

def validate_message(message):
    try:
        message_dict = json.loads(message)
        if (
            "action" in message_dict
            and "user_name" in message_dict
            and "target" in message_dict
        ):
            return message_dict
    except json.JSONDecodeError:
        return None
    return None


def handle_client(client_socket):
    client_buffer = b""

    welcome_message = {
        "status": "connected",
        # "message": "Welcome to the chat server! You are now connected."
    }
    send_message(client_socket, welcome_message)

    while True:
        readable, _, _ = select.select([client_socket], [], [], 0.1)

        for sock in readable:
            data = sock.recv(4096)
            if not data:
                print(f"Client {client_socket.getpeername()} disconnected")
                disconnect_client(client_socket)
                return

            client_buffer += data

            while b"\n" in client_buffer:
                message, client_buffer = client_buffer.split(b"\n", 1)
                message_str = message.decode("utf-8")
                message_dict = validate_message(message_str)

                if message_dict:
                    handle_message(client_socket, message_dict)
                else:
                    send_error(client_socket, "Malformed JSON")


def handle_message(client_socket, message):
    action = message["action"]

    if action == "connect":
        handle_connect(client_socket, message)
    elif action == "message":
        handle_message_send(client_socket, message)
    elif action == "disconnect":
        disconnect_client(client_socket)
    else:
        send_error(client_socket, "Unknown action")

def handle_connect(client_socket, message):
    user_name = message["user_name"]
    targets = message["targets"]

    if user_name not in clients:
        clients[user_name] = client_socket

    for target in targets:
        if target not in subscriptions:
            subscriptions[target] = set()
        subscriptions[target].add(user_name)

def handle_message_send(client_socket, message):
    user_name = message["user_name"]
    target = message["target"]
    message_text = message["message"]

    # Check if the target is connected
    if target in clients:
        if clients[target] != client_socket:
            # If the target is connected, update the existing message history
            if target in message_queues:
                message_queues[target]["history"].append({
                    "target": user_name,
                    "from": user_name,
                    "message": message_text,
                })
            else:
                # If the target doesn't have a message queue, create a new one
                message_queues[target] = {
                    "status": "chat",
                    "history": [
                        {
                            "target": user_name,
                            "from": user_name,
                            "message": message_text,
                        }
                    ],
                }
            # Send the updated message to the target
            send_message(clients[target], message_queues[target])
    elif target in subscriptions:
        # If the target is a group, send the message to all subscribers
        for user in subscriptions[target]:
            if user != user_name:
                # Update the existing message history for each subscriber
                if user in message_queues:
                    message_queues[user]["history"].append({
                        "target": user_name,
                        "from": user_name,
                        "message": message_text,
                    })
                else:
                    # If the subscriber doesn't have a message queue, create a new one
                    message_queues[user] = {
                        "status": "chat",
                        "history": [
                            {
                                "target": user_name,
                                "from": user_name,
                                "message": message_text,
                            }
                        ],
                    }
                # Send the updated message to the subscriber
                send_message(clients[user], message_queues[user])


def disconnect_client(client_socket):
    user_name_to_remove = None  # Initialize the variable

    for user_name, sock in clients.items():
        if sock == client_socket:
            user_name_to_remove = user_name
            break

    if user_name_to_remove is not None:
        del clients[user_name_to_remove]

    # Update the subscriptions after removing the client
    for target, users in subscriptions.items():
        if user_name_to_remove in users:
            users.remove(user_name_to_remove)

    client_socket.close()


def send_message(sock, message):
    message_json = json.dumps(message) + "\n"
    sock.send(message_json.encode("utf-8"))

def send_error(sock, error_message):
    error_data = {"status": "error", "message": error_message}
    send_message(sock, error_data)

if __name__ == "__main__":
    host = "127.0.0.1"  # Change this to your server's IP address
    port = 7775  # Change this to your desired port

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"Server is listening on {host}:{port}")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Accepted connection from {addr}")
        client_socket.setblocking(0)
        handle_client(client_socket)

