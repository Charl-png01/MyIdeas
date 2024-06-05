from string import ascii_lowercase as letters
from itertools import product

# Define the length of the password
password_length = 5

# Generate all possible passwords of length 5
all_possible_passwords = [''.join(candidate) for candidate in product(letters, repeat=password_length)]

# Now, the 'all_possible_passwords' list contains all 11,881,376 possible passwords.


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
