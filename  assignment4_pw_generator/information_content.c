//
// Created by Charles Kokofi on 5/11/23.
//

#include "information_content.h"
#include <string.h>
#include <math.h>

double calculate_information_content(char *str, int alphabet_size) {
    size_t length = strlen(str);
    double randomness = length * log2(alphabet_size);
    return randomness;
}
