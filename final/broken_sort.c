//
// Created by Charles Kokofi on 6/3/23.
//

#include "broken_sort.h"
#include <stdio.h>
#include <stdlib.h>

void bubble_sort(int *array, int size) {
    bool swapped;
    do {
        swapped = false;
        for (int i = 1; i < size; ++i) {
            if (array[i - 1] > array[i]) {
                int temp = array[i - 1];  // Changed swap() to a temporary variable to prevent overwriting of values
                array[i - 1] = array[i];
                array[i] = temp;
                swapped = true;
            }
        }
    } while (swapped);
}

void shuffle(int *array, int size) {
    for (int i = size - 1; i >= 0; --i) {
        int j = rand() % (i + 1);
        if (i != j) {
            array[i] ^= array[j];
            array[j] ^= array[i];
            array[i] ^= array[j];
        }
    }
}

bool test_bubble_sort(void) {
    int size = 15;

    bool all_passed = true;

    for (int trial = 0; trial < 10; ++trial) {
        int *array = malloc(size * sizeof(int));
        for (int i = 0; i < size; ++i) {
            array[i] = i;
        }

        shuffle(array, size);

        bubble_sort(array, size);

        printf("Trial %d\n{", trial);
        for (int i = 0; i < size; ++i) {
            printf("%d ", array[i]);
        }

        printf("}\n");
        for (int i = 0; i < size; ++i) {
            if (array[i] != i) {
                printf("Trial %d failed at index %d\n", trial, i);
                all_passed = false;
                break;
            }
        }
        free(array);
    }
    return all_passed;
}