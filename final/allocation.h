//
// Created by Charles Kokofi on 6/3/23.
//

#ifndef C_PROJECT_ALLOCATION_H
#define C_PROJECT_ALLOCATION_H
typedef struct {
    int *a;
    int ***b;
    int x;
    int y;
    int z;
} Thing;

Thing *malloc_thing(int x, int y, int z);
void free_thing(Thing *t);
#endif