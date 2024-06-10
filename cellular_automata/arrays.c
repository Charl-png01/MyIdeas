//
// Created by Charles Kokofi on 5/18/23.
//

#include "arrays.h"
#include <stdbool.h>
#include <stdlib.h>

int row_major(int row, int col, int width) {
    return row * width + col;
}

bool **malloc_2d(int width, int height) {
    bool **array = malloc(height * sizeof(bool *));
    for (int i = 0; i < height; i++) {
        array[i] = malloc(width * sizeof(bool));
    }
    return array;
}

void free_2d(bool **array, int height) {
    for (int i = 0; i < height; i++) {
        free(array[i]);
    }
    free(array);
}

bool *malloc_row_major(int width, int height) {
    return malloc(width * height * sizeof(bool));
}

void free_row_major(bool *array) {
    free(array);
}
