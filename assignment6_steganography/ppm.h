//
// Created by Charles Kokofi on 5/22/23.
//

#ifndef C_PROJECT_PPM_H
#define C_PROJECT_PPM_H
#include <stdio.h>
#include <stdbool.h>
#include <stdlib.h>

typedef struct {
    int width;
    int height;
} PPM_Header;

int read_ppm_header(FILE *input, PPM_Header *header);


typedef struct {
    uint8_t red;
    uint8_t green;
    uint8_t blue;
} PPM_Pixel;

int read_ppm_pixel(FILE *input, PPM_Pixel *pixel);

int write_ppm_pixel(FILE *output, const PPM_Pixel *pixel);

int write_ppm_header(FILE *output, const PPM_Header *header);

#endif
