//
// Created by Charles Kokofi on 5/18/23.
//
#ifndef C_PROJECT_PICTURE_H
#define C_PROJECT_PICTURE_H
#include <stdio.h>
#include <stdbool.h>
#include "arrays.h"
#include "rules.h"
void print_2d(bool **array, int width, int height);
void print_row_major(bool *array, int width, int height);
void initialize_first_row(bool *array, int width);
void rule_18_picture(int width, int height);
void rule_57_picture(int width, int height);
void rule_60_picture(int width, int height);
void rule_73_picture(int width, int height);
#endif //C_PROJECT_PICTURE_H
