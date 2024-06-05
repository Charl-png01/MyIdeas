import socket
import json
import sys


# Function to send JSON message to server
def send_message(sock, message):
    try:
        sock.sendall(message.encode())
    except Exception as e:
        print("Error sending message:", str(e))
        sys.exit(1)


# Function to receive JSON message from server
def receive_message(sock):
    try:
        data = sock.recv(4096).decode()
        return json.loads(data)
    except Exception as e:
        print("Error receiving message:", str(e))
        sys.exit(1)
    return None


# Get user input
username = input("Enter username: ")
targets = input("Enter channels separated by commas: ").split(",")

# Connect to server
server_host = ""
server_port = 7775
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    sock.connect((server_host, server_port))
except Exception as e:
    print("Connection error:", str(e))
    sys.exit(1)

# Send connect message
connect_data = {
    "action": "connect",
    "user_name": "@" + username,
    "targets": ["#" + t for t in targets]
}
send_message(sock, json.dumps(connect_data))

# Main loop to get user input and send messages
while True:
    message = input("Enter message: ")
    target = input("Enter target room or user: ")

    message_data = {
        "action": "message",
        "user_name": "@" + username,
        "target": target,
        "message": message
    }

    send_message(sock, json.dumps(message_data))

    # Check for incoming messages
    data = receive_message(sock)
    if not data:
        continue

    if data.get("status") == "disconnect":
        print("Server disconnected.")
        sock.close()
        break

    # Print any incoming messages
    if data.get("status") == "chat":
        print(f"{data['target']} {data['from']}: {data['message']}")

    elif data.get("status") == "error":
        print(f"Error: {data['message']}")

print("Disconnected")

