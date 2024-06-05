//
// Created by Charles Kokofi on 5/22/23.
//
#include "ppm.h"
#include <stdio.h>
#include <string.h>

int  read_ppm_header(FILE *input, PPM_Header *header) {
    char magic_number[3];
    if (fscanf(input, "%2s\n", magic_number) != 1 || strcmp(magic_number, "P3") != 0) {
        fprintf(stderr, "Invalid PPM format. Only P3 format is supported.\n");
        return 0;
    }

    if (fscanf(input, "%d %d\n", &header->width, &header->height) != 2) {
        fprintf(stderr, "Failed to read PPM dimensions.\n");
        return 0;
    }

    int max_value;
    if (fscanf(input, "%d\n", &max_value) != 1 || max_value != 255) {
        fprintf(stderr, "Invalid color depth. Only 255 color depth is supported.\n");
        return 0;
    }

    return 1;
}

int read_ppm_pixel(FILE *input, PPM_Pixel *pixel) {
    if (fscanf(input, "%hhu %hhu %hhu ", &pixel->red, &pixel->green, &pixel->blue) != 3) {
        fprintf(stderr, "Failed to read PPM pixel.\n");
        return 0;
    }

    return 1;
}

int write_ppm_header(FILE *output, const PPM_Header *header) {
    fprintf(output, "P3\n%d %d\n255\n", header->width, header->height);
    return 1;
}
int write_ppm_pixel(FILE *output, const PPM_Pixel *pixel) {
    fprintf(output, "%hhu %hhu %hhu ", pixel->red, pixel->green, pixel->blue);
    return 1;
}
