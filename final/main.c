
#include "allocation.h"
#include "broken_sort.h"
#include <time.h>
#include <stdio.h>
#include <stdlib.h>

int main(void) {
    srand(time(0));

    // Call for part 1
    Thing *foo = malloc_thing(4, 5, 6);
    free_thing(foo);
    foo = NULL;

    // Call for part 2
    if (test_bubble_sort()) {
        printf("Successfully fixed sort\n");
    } else {
        printf("Sort still broken\n");
    }

    return 0;
}
