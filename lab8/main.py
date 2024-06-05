import socket
import threading
from threading import Lock
import random
import time

# Use UDP for communication
HOST = '127.0.0.1'
PORT = 9999

# Dictionary to track active games
games = {}
# Locks to prevent concurrent access to game data
game_locks = {}

def handle_client(conn, addr):
    print(f"New connection from {addr}")
    while True:
        data, _ = conn.recvfrom(1024)
        if not data:
            break

        game_id = int.from_bytes(data[:3], byteorder='big')
        msg_id = int.from_bytes(data[3:4], byteorder='big')
        flags = int.from_bytes(data[4:7], byteorder='big')
        game_state = int.from_bytes(data[7:10], byteorder='big')
        msg = data[10:].decode()

        if game_id not in games:
            # New game
            if msg_id != 0 or flags != 0 or game_state != 0:
                # Invalid initial message
                send_error(conn, game_id, "Invalid initial message")
                continue

            print(f"Starting new game {game_id}")
            games[game_id] = {
                'board': [0] * 9,
                'next_player': random.choice(['X', 'O']),
                'msg_id': random.randint(0, 255),
                'last_activity': time.time()
            }
            game_locks[game_id] = Lock()

        else:
            # Existing game
            if msg_id != games[game_id]['msg_id']:
                # Invalid message ID
                send_error(conn, game_id, "Invalid message ID")
                continue

            with game_locks[game_id]:
                # Critical section
                if games[game_id]['board'][game_state] != 0:
                    # Invalid move
                    send_error(conn, game_id, "Invalid move")
                    continue

                games[game_id]['board'][game_state] = 'X' if games[game_id]['next_player'] == 'O' else 'O'
                games[game_id]['msg_id'] += 1

        # Handle game over
        if check_win(games[game_id]['board']):
            send_msg(conn, game_id, games[game_id]['msg_id'], 2 if games[game_id]['next_player'] == 'X' else 4, games[game_id]['board'],
                     f"{games[game_id]['next_player']} wins!")
            del games[game_id]
            del game_locks[game_id]
            break
        if check_tie(games[game_id]['board']):
            send_msg(conn, game_id, games[game_id]['msg_id'], 16, games[game_id]['board'], "Game tie!")
            del games[game_id]
            del game_locks[game_id]
            break

        # Make computer move
        with game_locks[game_id]:
            computer_move = find_computer_move(games[game_id]['board'])
            if computer_move is None:
                # No valid moves
                send_msg(conn, game_id, games[game_id]['msg_id'], 16, games[game_id]['board'], "Game tie!")
                del games[game_id]
                del game_locks[game_id]
                break

            games[game_id]['board'][computer_move] = games[game_id]['next_player']
            games[game_id]['next_player'] = 'X' if games[game_id]['next_player'] == 'O' else 'O'
            games[game_id]['msg_id'] += 1

        # Check for computer win
        if check_win(games[game_id]['board']):
            send_msg(conn, game_id, games[game_id]['msg_id'], 2 if games[game_id]['next_player'] == 'X' else 4, games[game_id]['board'],
                     f"{games[game_id]['next_player']} wins!")
            del games[game_id]
            del game_locks[game_id]
            break

        send_msg(conn, game_id, games[game_id]['msg_id'], 1 if games[game_id]['next_player'] == 'X' else 8, games[game_id]['board'],
                 f"{games[game_id]['next_player']}'s turn")

    conn.close()

def send_msg(conn, game_id, msg_id, flags, game_state, msg):
    data = game_id.to_bytes(3, byteorder='big')
    data += msg_id.to_bytes(1, byteorder='big')
    data += flags.to_bytes(3, byteorder='big')
    data += game_state.to_bytes(3, byteorder='big')
    data += msg.encode()
    conn.sendto(data, addr)

def send_error(conn, game_id, error):
    send_msg(conn, game_id, 0, 32, 0, error)

def check_win(board):
    # Check rows
    for i in range(0, 9, 3):
        if board[i] != 0 and board[i] == board[i + 1] == board[i + 2]:
            return True

    # Check columns
    for i in range(3):
        if board[i] != 0 and board[i] == board[i + 3] == board[i + 6]:
            return True

    # Check diagonals
    if board[0] != 0 and board[0] == board[4] == board[8]:
        return True
    if board[2] != 0 and board[2] == board[4] == board[6]:
        return True

    return False

def check_tie(board):
    return all(square != 0 for square in board)

def find_computer_move(board):
    # Implement computer strategy here
    for i in range(9):
        if board[i] == 0:
            return i

    return None

def purge_old_games():
    while True:
        time.sleep(300)  # Every 5 minutes
        current_time = time.time()
        for game_id in list(games.keys()):
            if current_time - games[game_id]['last_activity'] > 300:
                del games[game_id]
                del game_locks[game_id]

if __name__ == "__main__":
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.bind((HOST, PORT))
        print(f"Server listening on {HOST}:{PORT}")

        thread = threading.Thread(target=purge_old_games)
        thread.start()

        while True:
            data, addr = s.recvfrom(1024)
            thread = threading.Thread(target=handle_client, args=(s, addr))
            thread.start()
