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
        


if __name__ == '__main__':
    host = '127.0.0.1'  # server ip
    port = 5000         # server port

    # Create a regular client socket
    client_socket = socket.socket()      

    # Establish connection with server
    print_msg("Establishing connection to " + host + ":" + str(port))
    try:
        client_socket.connect((host, port))  # connect to the server
    except Exception as e:
        print_msg("Error during connection: " + str(e))
        sys.exit(1)




    # TODO: Implement client side of authentication protocol and store established 
    #       session key in the session_key variable as a byte string
    session_key = None
    
    
    
    
    # Print session key
    if session_key is None:
        print_msg ("No session key established!")
    else:
        print_msg ("Established session key: " + str(binascii.hexlify(session_key)))

    # Close the connection
    if client_socket:
        client_socket.close()
    print_msg("Client stopped")
    sys.exit(0)
    