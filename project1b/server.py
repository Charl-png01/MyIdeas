import socket
import struct
import random
import sys
import time
from concurrent.futures import ThreadPoolExecutor
import threading

BUF_SIZE = 65507
MAX_THREADS = 10
GAMES = {}
GAME_LOCKS = {}
TIMEOUT = 300  # 5 minutes timeout for inactive games

class Game:
    def __init__(self, player_name):
        self.board = [0] * 9
        self.player_name = player_name
        self.server_piece = None
        self.player_piece = None
        self.winner = None
        self.last_active = time.time()

    def make_move(self, position, piece):
        if self.board[position] == 0:
            self.board[position] = piece
            return True
        return False

    def check_winner(self):
        winning_combinations = [(0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6)]
        for combo in winning_combinations:
            if self.board[combo[0]] == self.board[combo[1]] == self.board[combo[2]] != 0:
                self.winner = "X" if self.board[combo[0]] == 1 else "O"
                return True
        return False

    def check_tie(self):
        return all(cell != 0 for cell in self.board)

    def get_game_state(self):
        state = 0
        for i in range(9):
            state |= self.board[i] << (2 * (8 - i))
        return state

    def set_game_state(self, state):
        for i in range(9):
            self.board[i] = (state >> (2 * (8 - i))) & 0b11
        self.last_active = time.time()

def decode_msg(data):
    header, message = struct.unpack('>Q{}s'.format(len(data) - 8), data)
    game_id = (header >> 40) & 0xFFFFFF
    msg_id = (header >> 32) & 0xFF
    flags = (header >> 18) & 0xFFFF
    game_state = header & 0x3FFFF
    return game_id, msg_id, flags, game_state, message.decode('utf-8')

def encode_msg(game_id, msg_id, flags, game_state, msg):
    header = (game_id << 40) | (msg_id << 32) | (flags << 18) | game_state
    packed_header = struct.pack('>Q', header)
    packed_message = msg.encode('utf-8')
    return packed_header + packed_message

def handle_client(client_socket, client_address, game_id, player_name):
    if game_id not in GAMES:
        GAMES[game_id] = Game(player_name)
        GAME_LOCKS[game_id] = threading.RLock()

    with GAME_LOCKS[game_id]:
        game = GAMES[game_id]
        game.set_game_state(0)
        msg_id = random.randint(0, 255)
        player_piece = random.choice(["X", "O"])
        server_piece = "X" if player_piece == "O" else "O"
        game.server_piece = server_piece
        game.player_piece = player_piece
        flags = 0b0000000000000001 if player_piece == "X" else 0b0000000000000010
        game_state = game.get_game_state()
        msg = f'You are playing as {player_piece}. Make your move.'
        response = encode_msg(game_id, msg_id, flags, game_state, msg)
        client_socket.sendto(response, client_address)

    # Handle the game's updates from the client
    while True:
        data, client_address = client_socket.recvfrom(BUF_SIZE)
        game_id, msg_id, client_flags, client_game_state, client_msg = decode_msg(data)

        game = GAMES[game_id]
        player_piece = game.player_piece
        server_piece = game.server_piece

        # Extract the move from the client_msg and update the game board
        if client_flags & 0x0000000000000001:
            row, col = map(int, client_msg.split(','))
            position = row * 3 + col
            if game.make_move(position, 1 if player_piece == "X" else 2):  # 1 for "X", 2 for "O"
                if game.check_winner():
                    flags = 0b0000000000000100 if game.winner == "X" else 0b0000000000001000
                    response = encode_msg(game_id, msg_id, flags, game.get_game_state(),
                                          f"Game over. {game.winner} won!")
                    client_socket.sendto(response, client_address)
                    break

            if game.check_tie():
                flags = 0b0000000000010000
                response = encode_msg(game_id, msg_id, flags, game.get_game_state(), "Game over. It's a tie!")
                client_socket.sendto(response, client_address)
                break

            # Server's move
            available_positions = [i for i, x in enumerate(game.board) if x == 0]
            if available_positions:
                server_move = random.choice(available_positions)
                game.make_move(server_move, 1 if server_piece == "X" else 2)

            if game.check_winner():
                flags = 0b0000000000000100 if game.winner == "X" else 0b0000000000001000
                response = encode_msg(game_id, msg_id, flags, game.get_game_state(), f"Game over. {game.winner} won!")
                client_socket.sendto(response, client_address)
                break

            if game.check_tie():
                flags = 0b0000000000010000
                response = encode_msg(game_id, msg_id, flags, game.get_game_state(), "Game over. It's a tie!")
                client_socket.sendto(response, client_address)
                break
        else:
            # Invalid client message, respond with an error
            flags = 0b00100000
            response = encode_msg(game_id, msg_id, flags, game.get_game_state(), "Invalid move format. Please use 'row,col'.")
            client_socket.sendto(response, client_address)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python server.py <IP_ADDRESS> <PORT>")
        sys.exit(1)

    ip_address = sys.argv[1]
    port = int(sys.argv[2])
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((ip_address, port))
    print(f"Server listening on {ip_address}:{port}")

    with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
        while True:
            data, client_address = server_socket.recvfrom(BUF_SIZE)
            game_id, msg_id, flags, game_state, player_name = decode_msg(data)
            executor.submit(handle_client, server_socket, client_address, game_id, player_name)

