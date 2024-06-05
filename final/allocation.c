//
// Created by Charles Kokofi on 6/3/23.
//

#include "allocation.h"
#include <stdlib.h>

Thing *malloc_thing(int x, int y, int z) {
    Thing *ret = malloc(sizeof(Thing));
    ret->x = x;
    ret->y = y;
    ret->z = z;
    ret->a = malloc(sizeof(int));
    ret->b  = malloc(x * sizeof(int **));
    for (int i = 0; i < x; ++i) {
        ret->b[i] = malloc(y * sizeof(int *));
        for (int j = 0; j < y; ++j) {
            ret->b[i][j] = malloc(z * sizeof(int));
        }
    }
    return ret;
}

void free_thing(Thing *t) {
    // Fill in this part
    // Make sure to fully and completely free up the struct pass in as a parameter
    //this function ensure complete deallocations of memory assign to "Thing struct && associated arrays
    free(t->a);
    for (int i = 0; i < t->x; ++i) {
        for (int j = 0; j < t->y; ++j) {
            free(t->b[i][j]);
        }
        free(t->b[i]);
    }
    free(t->b);
    free(t);
}