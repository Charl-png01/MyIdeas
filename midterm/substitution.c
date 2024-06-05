//
// Created by Charles Kokofi on 4/28/23.
//
#include "substitution.h"
#include "substitution.h"
#include <ctype.h>
#include <string.h>

char encrypt_letter(char letter, char *key) {
    int index;
    if (isupper(letter)) {
        index = letter - 'A';
        return isupper(key[index]) ? key[index] : tolower(key[index]);
    }
    return letter;
}

void encrypt_string(char *input, char *key, char *output) {
    int length = strlen(input);
    for (int i = 0; i < length; i++) {
        if (isalpha(input[i])) {
            int index = toupper(input[i]) - 'A';
            output[i] = isupper(input[i]) ? key[index] : (char) tolower(key[index]);;
        } else {
            output[i] = input[i];
        }
    }
    output[length] = '\0';
}


