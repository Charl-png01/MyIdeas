//
// Created by Charles Kokofi on 4/28/23.
//
#include "percent.h"
#include <stdio.h>
#include <string.h>

void test_percent_encode1(void) {
    char input[] = "Hello world!";
    char expected_output[] = "Hello%20world%21";
    char output[strlen(expected_output) + 1];
    percent_encode(input, output);
    if (strcmp(output, expected_output) != 0) {
        printf("Error percent_encoding. Input = '%s'\n", input);
        printf("Expected: '%s'\n", expected_output);
        printf("Actual:   '%s'\n", output);
    }
}
void test_percent_encode2(void) {
    char input2[] = "Percent-encoding a %";
    char expected_output2[] = "Percent-encoding%20a%20%25";
    char output2[strlen(expected_output2) + 1];
    percent_encode(input2, output2);
    if (strcmp(output2, expected_output2) != 0) {
        printf("Error percent_encoding. Input = '%s'\n", input2);
        printf("Expected: '%s'\n", expected_output2);
        printf("Actual:   '%s'\n", output2);
    }
}

void test_percent_encode3(void) {
    char input3[] = "Testing 1 2 3";
    char expected_output3[] = "Testing%201%202%203";
    char output3[strlen(expected_output3) + 1];
    percent_encode(input3, output3);
    if (strcmp(output3, expected_output3) != 0) {
        printf("Error percent_encoding. Input = '%s'\n", input3);
        printf("Expected: '%s'\n", expected_output3);
        printf("Actual:   '%s'\n", output3);
    }
}

void test_percent_encode4(void) {
    char input4[] = "!@#$%";
    char expected_output4[] = "%21%40%23%24%25";
    char output4[strlen(expected_output4) + 1];
    percent_encode(input4, output4);
    if (strcmp(output4, expected_output4) != 0){
        printf("Error percent_encoding. Input = '%s'\n", input4);
        printf("Expected: '%s'\n", expected_output4);
        printf("Actual:   '%s'\n", output4);
    }
}
