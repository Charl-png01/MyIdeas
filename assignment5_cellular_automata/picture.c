//
// Created by Charles Kokofi on 5/18/23.
//

#include "picture.h"
#include <stdbool.h>
#include <stdio.h>
#include "rules.h"
#include "arrays.h"
#include "picture.h"
void initialize_first_row(bool *array, int width) {
    for (int col = 0; col < width; col++) {
        array[col] = false;
    }
    array[width / 2] = true;  // Set the middle element to true
}

void print_2d(bool **array, int width, int height) {
    for (int row = 0; row < height; row++) {
        for (int col = 0; col < width; col++) {
            printf("%c", array[row][col] ? 'X' : '.');
        }
        printf("\n");
    }
}

void print_row_major(bool *array, int width, int height) {
    for (int row = 0; row < height; row++) {
        for (int col = 0; col < width; col++) {
            printf("%c", array[row_major(row, col, width)] ? 'X' : '.');
        }
        printf("\n");
    }
}

void rule_18_picture(int width, int height) {
    bool **array = malloc_2d(width, height);

    initialize_first_row(array[0], width);
    for (int row = 1; row < height; row++) {
        for (int col = 0; col < width; col++) {
            bool left = (col > 0) ? array[row - 1][col - 1] : false;
            bool center = array[row - 1][col];
            bool right = (col < width - 1) ? array[row - 1][col + 1] : false;
            array[row][col] = rule_18(left, center, right);
        }
    }


    print_2d(array, width, height);

    free_2d(array, height);
}

void rule_57_picture(int width, int height) {
    bool **array = malloc_2d(width, height);

    initialize_first_row(array[0], width);
    for (int row = 1; row < height; row++) {
        for (int col = 0; col < width; col++) {
            bool left = (col > 0) ? array[row - 1][col - 1] : false;
            bool center = array[row - 1][col];
            bool right = (col < width - 1) ? array[row - 1][col + 1] : false;
            array[row][col] = rule_57(left, center, right);
        }
    }


    print_2d(array, width, height);

    free_2d(array, height);
}
void rule_60_picture(int width, int height) {
    bool *array = malloc_row_major(width, height);

    initialize_first_row(array, width);
    for (int row = 1; row < height; row++) {
        for (int col = 0; col < width; col++) {
            bool left = (col > 0) ? array[row_major(row - 1, col - 1, width)] : false;
            bool center = array[row_major(row - 1, col, width)];
            bool right = (col < width - 1) ? array[row_major(row - 1, col + 1, width)] : false;
            array[row_major(row, col, width)] = rule_60(left, center, right);
        }
    }


    print_row_major(array, width, height);

    free_row_major(array);
}

void rule_73_picture(int width, int height) {
    bool *array = malloc_row_major(width, height);

    initialize_first_row(array, width);
    for (int row = 1; row < height; row++) {
        for (int col = 0; col < width; col++) {
            bool left = (col > 0) ? array[row_major(row - 1, col - 1, width)] : false;
            bool center = array[row_major(row - 1, col, width)];
            bool right = (col < width - 1) ? array[row_major(row - 1, col + 1, width)] : false;
            array[row_major(row, col, width)] = rule_73(left, center, right);
        }
    }


    print_row_major(array, width, height);

    free_row_major(array);
}
