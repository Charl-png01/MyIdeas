import socket
import struct
import random
import sys

BUFFER_SIZE = 65507

def encode_game_message(game_id, message_id, game_flags, game_state, message):
   header = (game_id << 40) | (message_id << 32) | (game_flags << 18) | game_state
   packed_header = struct.pack('>Q', header)
   final_message = packed_header + message.encode('utf-8')
   return final_message

def decode_game_message(data):
   header_part = data[:8]
   message_part = data[8:]
   header = struct.unpack('>Q', header_part)[0]
   game_id = (header >> 40) & 0xFFFFFF
   message_id = (header >> 32) & 0xFF
   game_flags = (header >> 18) & 0xFFFF
   game_state = header & 0x3FFFF
   return game_id, message_id, game_flags, game_state, message_part.decode('utf-8')

def get_bit(row, col):
   return (row * 3 + col) * 2

def is_valid_move(game_state, move):
   try:
       row, col = move.split(",")
       row = int(row)
       col = int(col)
       if 0 <= row <= 2 and 0 <= col <= 2:
           bit = get_bit(row, col)
           cell_state = (game_state >> bit) & 0x3
           return cell_state == 0
       else:
           return False
   except:
       return False

def update_game_state(game_state, move, player):
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

def display_game_board(game_state):
   symbols = [' ', 'X', 'O']
   for row in range(3):
       for col in range(3):
           bit = get_bit(row, col)
           cell_state = (game_state >> bit) & 0x3
           print(symbols[cell_state], end="")
           if col != 2:
               print('|', end="")
       print()

def get_player(player_flags):
   if player_flags & (1 << 13):
       return "X"
   else:
       return "O"

def play_game_with_server(ip_address, port):
   s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
   game_id = random.randint(0, 0xFFFFFF)
   message_id = 0
   player_name = input("Enter your name: ")

   game_message = encode_game_message(game_id, message_id, 0, 0, player_name)
   s.sendto(game_message, (ip_address, port))

   while True:
       data, addr = s.recvfrom(BUFFER_SIZE)
       game_id, received_message_id, flags, game_state, message = decode_game_message(data)
       display_game_board(game_state)
       print("Server says:", message)

       if flags & 0x20:
           print("An error occurred.")
           break
       if flags & (1 << 2) or flags & (1 << 3) or flags & (1 << 4):
           print("Game over. Server says:", message)
           break

       player = get_player(flags)
       move = input("Your move: ")

       while not is_valid_move(game_state, move):
           print("Invalid move. Try again.")
           move = input("Your move: ")

       game_state = update_game_state(game_state, move, player)
       message_id = received_message_id + 1 & 0xFF

       message_to_send = encode_game_message(game_id, message_id, 0, game_state, "")
       s.sendto(message_to_send, (ip_address, port))

   print("Game is over, Bye")
   s.close()

if __name__ == "__main__":
   if len(sys.argv) != 3:
       print("Usage: python file_name.py <IP> <PORT>")
   else:
       ip_address = sys.argv[1]
       port = int(sys.argv[2])
       play_game_with_server(ip_address, port)
