//
// Created by Charles Kokofi on 5/11/23.
//
#include "alphabet.h"
#include <string.h>
#include <ctype.h>

int calculate_alphabet_size(char *password) {
    int alphabet_size = 0;
    int used_chars[4] = {0}; // index 0 for lowercase, index 1 for uppercase, index 2 for digits, index 3 for symbols

    for (int i = 0; password[i] != '\0'; i++) {
        if (islower(password[i])) {
            used_chars[0]++;
        }
        else if (isupper(password[i])) {
            used_chars[1]++;
        }
        else if (isdigit(password[i])) {
            used_chars[2]++;
        }
        else {
            used_chars[3]++;
        }
    }

    if (used_chars[0] > 0) { //if alphabet is lower add +26
        alphabet_size += 26;
    }
    if (used_chars[1] > 0) { //  if alphabet is upper add +26
        alphabet_size += 26;
    }

    if (used_chars[2] > 0) { //if isdigit add +10 (0 to 9)
        alphabet_size += 10;
    }

    if (used_chars[3] > 0) { //if its symbol add +32
        alphabet_size += 32;
    }

    return alphabet_size;
}


int calculate_union_alphabet(char *union_alphabet, char *alphabet) {
    int union_len = 0;
    for (int i = 0; i < strlen(alphabet); i++) {
        if (!strchr(union_alphabet, alphabet[i])) {
            union_alphabet[union_len++] = alphabet[i];
        }
    }
    union_alphabet[union_len] = '\0';
    return union_len;
}