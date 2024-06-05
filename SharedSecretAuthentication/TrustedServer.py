import socket
import threading

class TrustedNodeServer:
    def __init__(self, host='localhost', port=65432):
        self.host = host
        self.port = port
        self.hmacs = {}

    def handle_client(self, conn, addr):
        print(f"Connected by {addr}")
        data = conn.recv(1024)
        if not data:
            return

        sender, hmac_part, nonce = data.split(b',')
        self.hmacs[sender] = (hmac_part, nonce)

        if len(self.hmacs) == 2:
            hmac_a, nonce_a = self.hmacs[b'A']
            hmac_b, nonce_b = self.hmacs[b'B']
            if hmac_a == hmac_b:
                conn.sendall(b'MATCH')
            else:
                conn.sendall(b'NO_MATCH')
        conn.close()

    def start(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.host, self.port))
            s.listen()
            print("Server listening on", self.host, self.port)
            while True:
                conn, addr = s.accept()
                thread = threading.Thread(target=self.handle_client, args=(conn, addr))
                thread.start()

if __name__ == "__main__":
    server = TrustedNodeServer()
    server.start()
