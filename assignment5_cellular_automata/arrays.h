//
// Created by Charles Kokofi on 5/18/23.
//

#ifndef C_PROJECT_ARRAYS_H
#define C_PROJECT_ARRAYS_H
#include <stdbool.h>
#include "arrays.h"
#include "picture.h"
bool **malloc_2d(int width, int height);
void free_2d(bool **array, int height);
bool *malloc_row_major(int width, int height);
void free_row_major(bool *array);
int row_major(int row, int col, int width);
#endif //C_PROJECT_ARRAYS_H
