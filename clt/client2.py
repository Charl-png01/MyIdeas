import socket
import struct
import random
import sys

BUF_SIZE = 65507

def encode_msg(game_id, msg_id, flags, game_state, msg):
    header = (game_id << 40) | (msg_id << 32) | (flags << 18) | game_state
    packed_header = struct.pack('>Q', header)
    final_message = packed_header + msg.encode('utf-8')
    return final_message

def decode_msg(data):
    header_part = data[:8]
    message_part = data[8:]
    header = struct.unpack('>Q', header_part)[0]
    game_id = (header >> 40) & 0xFFFFFF
    msg_id = (header >> 32) & 0xFF
    flags = (header >> 18) & 0xFFFF
    game_state = header & 0x3FFFF
    return game_id, msg_id, flags, game_state, message_part.decode('utf-8')

def get_bit(row, col):
   return (row * 3 + col) * 2

def is_valid_move(game_state, move):
   try:
       row, col = move.split(",")
       row = int(row)
       col = int(col)
       if row >= 0 and row <= 2 and col >= 0 and col <= 2:
           bit = get_bit(row, col)
           cell_state = (game_state >> bit) & 0x3
           return cell_state == 0
       else:
           return False
   except:
       return False

def update_state(game_state, move, player):
   row, col = move.split(",")
   row = int(row)
   col = int(col)
   bit = get_bit(row, col)
   if player == "X":
       move_state = 0x1
   else:
       move_state = 0x2
   mask = move_state << bit
   return game_state | mask

def show_board(game_state):
   symbols = [' ', 'X', 'O']
   for row in range(3):
       for col in range(3):
           bit = get_bit(row, col)
           cell_state = (game_state >> bit) & 0x3
           print(symbols[cell_state], end="")
           if col != 2:
               print('|', end="")
       print()

def get_player(flag):
   if flag & (1 << 13):
       return "X"
   else:
       return "O"

def process_server_message(flags, msg):
    if flags & 0x20:
        print("An error occurred.")
    elif flags & (1 << 2):
        print("Game over. Server says:", msg)
    elif flags & (1 << 3):
        print("Game over. It's a tie!")
    elif flags & (1 << 4):
        print("Invalid move format. Please use 'row,col'.")
    else:
        print("Server says:", msg)

def play_game(ip_address, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    game_id = random.randint(0, 0xFFFFFF)
    msg_id = 0
    name = input("Enter name: ")
    msg = encode_msg(game_id, msg_id, 0, 0, name)
    s.sendto(msg, (ip_address, port))

    while True:
        data, addr = s.recvfrom(BUF_SIZE)
        game_id, received_msg_id, flags, game_state, msg = decode_msg(data)
        show_board(game_state)
        process_server_message(flags, msg)

        if not (flags & 0x20) and not (flags & (1 << 2)):
            player = get_player(flags)
            move = input("Your move: ")

            while not is_valid_move(game_state, move):
                print("Wrong move. Try again.")
                move = input("Your move: ")

            game_state = update_state(game_state, move, player)
            msg_id = received_msg_id + 1 & 0xFF

            msg_to_send = encode_msg(game_id, msg_id, 0, game_state, "")
            s.sendto(msg_to_send, (ip_address, port))

            # Log the message being sent
            print("Client sends:", msg_to_send)

        if flags & (1 << 2) or flags & 0x20:
            print("Game ended. Bye!")
            break

if __name__ == "__main__":
   if len(sys.argv) != 3:
       print("Usage: python file_name.py <IP> <PORT>")
   else:
       ip = sys.argv[1]
       port = int(sys.argv[2])
       play_game(ip, port)
