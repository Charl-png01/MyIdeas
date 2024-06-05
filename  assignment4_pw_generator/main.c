#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include "information_content.h"
#include "pw_generator.h"
#include "alphabet.h"

#define MAX_PASSWORD_LEN 100
#define MAX_ALPHABET_LEN 1000

int main(int argc, char *argv[]) {
    srand((unsigned) time(NULL));

    if (argc < 3) {
        printf("Usage: %s length quantity [-luds] [alphabet]\n", argv[0]);
        return 0;
    }

    int length = atoi(argv[1]);
    int quantity = atoi(argv[2]);
    char default_alphabet[] = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz";
    char *alphabet = malloc(sizeof(default_alphabet));

    // Set the -luds flags if no other alphabet is specified
    if (argc == 3) {
        strcat(alphabet, "abcdefghijklmnopqrstuvwxyz");
        strcat(alphabet, "ABCDEFGHIJKLMNOPQRSTUVWXYZ");
        strcat(alphabet, "0123456789");
        strcat(alphabet, "!@#$%^&*()-_=+[]{}\\|;:'\",.<>/?");
    } else {
        // Parse the -luds flags and the additional characters in the alphabet
        int i, j;
        for (i = 3, j = 0; i < argc; i++) {
            if (argv[i][0] == '-') {
                for (int k = 1; k < strlen(argv[i]); k++) {
                    switch (argv[i][k]) {
                        case 'l':
                            strcat(alphabet, "abcdefghijklmnopqrstuvwxyz");
                            break;
                        case 'u':
                            strcat(alphabet, "ABCDEFGHIJKLMNOPQRSTUVWXYZ");
                            break;
                        case 'd':
                            strcat(alphabet, "0123456789");
                            break;
                        case 's':
                            strcat(alphabet, "!@#$%^&*()-_=+[]{}\\|;:'\",.<>/?");
                            break;
                        default:
                            printf("Warning: unrecognized flag %c\n", argv[i][k]);
                            break;
                    }
                }
            } else {
                // Concatenate the additional characters to the alphabet
                int len = strlen(argv[i]);
                if (j + len >= MAX_ALPHABET_LEN - 1) {
                    printf("Error: alphabet too long\n");
                    return 0;
                }
                memcpy(alphabet + j, argv[i], len);
                j += len;
            }
        }
    }

    alphabet = realloc(alphabet, strlen(alphabet) + 1); // resize the allocated memory for the alphabet
    alphabet[strlen(alphabet)] = '\0'; // add null character at the end of the alphabet
    printf("Using alphabet: %s\n", alphabet);

    // Calculate union alphabet
    char union_alphabet[MAX_ALPHABET_LEN];
    int union_len = calculate_union_alphabet(union_alphabet, alphabet);
    if (union_len == 0) {
        fprintf(stderr, "Error: no valid characters to draw from\n");
        return 0;
    }
    printf("\n");

    // Generate passwords
    for (int i = 0; i < quantity; i++) {
        char password[MAX_PASSWORD_LEN];
        generate_password(password, length, union_alphabet, union_len);
        printf("Password %d:\n", i+1);
        printf("Password: %s\n", password);
        int alphabet_size = calculate_alphabet_size(union_alphabet);
        printf("Information content: %0.2f bits\n\n", calculate_information_content(password, alphabet_size));
    }

    free(alphabet);

    return 0;
}

