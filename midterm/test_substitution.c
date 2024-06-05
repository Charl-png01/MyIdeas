//
// Created by Charles Kokofi on 4/28/23.
//
#include <stdio.h>
#include <string.h>
#include "substitution.h"

void test_encrypt_letter1(void) {
    char letter = 'A';
    char key[] = "ZYXWVUTSRQPONMLKJIHGFEDCBA";
    char expected = 'Z';
    char actual = encrypt_letter(letter, key);
    if (actual != expected) {
        printf("Error encrypt_letter. Letter = '%c', key = '%s'\n", letter, key);
        printf("Expected: '%c'\n", expected);
        printf("Actual:   '%c'\n", actual);
    }
}

void test_encrypt_letter2(void) {
    char letter = 'a';
    char key[] = "ZYXWVUTSRQPONMLKJIHGFEDCBA";
    char expected = 'a';
    char actual = encrypt_letter(letter, key);
    if (actual != expected) {
        printf("Error encrypt_letter. Letter = '%c', key = '%s'\n", letter, key);
        printf("Expected: '%c'\n", expected);
        printf("Actual:   '%c'\n", actual);
    }
}

void test_encrypt_string1(void) {
    char input[] = "Attack at dawn";
    char key1[] = "XYZABCDEFGHIJKLMNOPQRSTUVW";
    char output[100];
    char expected1[] = "Xqqxzh xq axtk";
    encrypt_string(input, key1, output);
    if (strcmp(output, expected1) != 0) {
        printf("Error encrypt_string. Input = '%s', key = '%s'\n", input, key1);
        printf("Expected: '%s'\n", expected1);
        printf("Actual:   '%s'\n", output);
    }

}

void test_encrypt_string2(void) {
    char input[] = "Attack at Dawn";
    char key[] = "ZYXWVUTSRQPONMLKJIHGFEDCBA";
    char output[100];
    char expected[] = "Zggzxp zg Wzdm";
    encrypt_string(input, key, output);
    if (strcmp(output, expected) != 0) {
        printf("Error encrypt_string. Input = '%s', key = '%s'\n", input, key);
        printf("Expected: '%s'\n", expected);
        printf("Actual:   '%s'\n", output);
    }
}

void test_encrypt_string3(void) {
    char input[] = "Attack at Dawn";
    char key[] = "mviszlwcoanfubxtejkyqdhrpg";
    char output[100];
    char expected[] = "myymin my smhb";
    encrypt_string(input, key, output);
    if (strcmp(output, expected) != 0) {
        printf("Error encrypt_string. Input = '%s', key = '%s'\n", input, key);
        printf("Expected: '%s'\n", expected);
        printf("Actual:   '%s'\n", output);
    }
}
void test_encrypt_string4(void) {
    char input[] = "my love is pure";
    char key[] = "phgvcauqfornxmtjiwlszdkeby";
    char output[100];
    char expected[] = "xb ntdc fl jzwc";
    encrypt_string(input, key, output);
    if (strcmp(output, expected) != 0) {
        printf("Error encrypt_string. Input = '%s', key = '%s'\n", input, key);
        printf("Expected: '%s'\n", expected);
        printf("Actual:   '%s'\n", output);
    }
}

