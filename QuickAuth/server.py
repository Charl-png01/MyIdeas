import socket
import threading
import sys
import datetime
import time



print_lock = threading.Lock()  # mutex lock for display access


def print_msg(msg):
    '''
    Print a message with current timestamp
    msg: the message string
    '''
    time_str = "\033[91m\033[1m%s\033[0m" % datetime.datetime.fromtimestamp(int(time.time()))
    with print_lock:
        print(time_str + "  " + "\033[91m\033[1m" + msg + "\033[0m")
            

def handle_client(client_socket, client_ip, client_port):
    '''
    Handles connection from a client
    client_socket: socket to use to read/write to client
    client_ip:     IP address of client
    client_port:   port number of client connection
    '''

    print_msg("Connection from " + client_ip + ":" + client_port)

    # Generate server's Diffie-Hellman parameters
    dh_params = dh.get_dh_parameters()

    # Send server's public key to the client
    client_socket.sendall(dh_params.pub_key)

    # Receive client's public key
    client_pub_key = client_socket.recv(1024)

    # Derive the shared secret key
    session_key = dh_params.derive_shared_key(client_pub_key)

    # Print session key
    if session_key is None:
        print_msg("No session key established!")
    else:
        print_msg("Established session key: " + str(binascii.hexlify(session_key)))

    # Close the connection (must always be done)
    if client_socket:
        client_socket.close()
    print_msg("Connection closed to " + client_ip + ":" + client_port)
        
        
        
if __name__ == '__main__':

    host = '127.0.0.1'   # ip to use to accept connections
    port = 5000          # port number to use to accept connections


    # Create a server socket
    server_socket = socket.socket()
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((host, port))  

    # Allow only five clients at a time 
    server_socket.listen(5)

    print_msg("Listening for connection on " + host + ":" + str(port))


    while True:
        try:
            client_socket, address = server_socket.accept()  # accept new connection
            client_ip = address[0]
            client_port = str(address[1])

            # Start a thread to handle client connection
            threading.Thread(target=handle_client, args=(client_socket, client_ip, client_port), daemon=True).start()
            
        except KeyboardInterrupt:  # CTRL+C
            print("")
            print_msg("Server stopped")

            if server_socket:
                server_socket.close()
            if client_socket:
                client_socket.close()
            sys.exit(0)
        except Exception as e:
            print_msg("Exception: " + str(e))
            
            if server_socket:
                server_socket.close()
            if client_socket:
                client_socket.close()
            sys.exit(1)

