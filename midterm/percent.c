//
// Created by Charles Kokofi on 4/28/23.
//
#include "percent.h"
#include <ctype.h>
#include <stdio.h>
#include <string.h>

void percent_encode(char *input, char *output) {
    char hex[3] = {0};
    int input_len = strlen(input);
    int output_index = 0;

    for (int  count= 0; count < input_len; count++) {
        if (isalnum(input[count]) || input[count] == '-' || input[count] == '.' ||
            input[count] == '_' || input[count] == '*') {

            output[output_index++] = input[count];
        } else if (input[count] == ' ') {
            // Space character is represented as "%20"
            output[output_index++] = '%';
            output[output_index++] = '2';
            output[output_index++] = '0';
        } else if (isgraph(input[count])) {
            snprintf(hex, sizeof(hex), "%02x", input[count]);
            output[output_index++] = '%';
            output[output_index++] = hex[0];
            output[output_index++] = hex[1];
        }
    }

    output[output_index] = '\0';
}
