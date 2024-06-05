//
// Created by Charles Kokofi on 5/11/23.
//

#include "pw_generator.h"
#include <stdlib.h>

void generate_password(char *password, int length, char *alphabet, int alphabet_len) {
    for (int i = 0; i < length; i++) {
        password[i] = alphabet[rand() % alphabet_len];
    }
    password[length] = '\0';
}