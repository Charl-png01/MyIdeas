//
// Created by Charles Kokofi on 5/22/23.
//
#include <stdio.h>
#include "ppm.h"
#include "steganography.h"
#include <stdlib.h>
#include <inttypes.h>

int encode_payload(const char *inputFile, const char *payloadFile, const char *outputFile) {
    FILE *input = fopen(inputFile, "rb");
    if (!input) {
        fprintf(stderr, "Failed to open input file: %s\n", inputFile);
        return 0;
    }

    FILE *payload = fopen(payloadFile, "rb");
    if (!payload) {
        fprintf(stderr, "Failed to open payload file: %s\n", payloadFile);
        fclose(input);
        return 0;
    }

    FILE *output = fopen(outputFile, "wb");
    if (!output) {
        fprintf(stderr, "Failed to create output file: %s\n", outputFile);
        fclose(input);
        fclose(payload);
        return 0;
    }

    PPM_Header header;
    if (!read_ppm_header(input, &header)) {
        fprintf(stderr, "Failed to read input PPM header.\n");
        fclose(input);
        fclose(payload);
        fclose(output);
        return 0;
    }

    if (header.width * header.height < 16) {
        fprintf(stderr, "Invalid input PPM dimensions. Cannot encode payload.\n");
        fclose(input);
        fclose(payload);
        fclose(output);
        return 0;
    }

    write_ppm_header(output, &header);

    // Encode payload size
    uint16_t payloadSize;
    fseek(payload, 0, SEEK_END);
    payloadSize = ftell(payload);
    fseek(payload, 0, SEEK_SET);
    fwrite(&payloadSize, sizeof(uint16_t), 1, output);

    PPM_Pixel pixel;
    int bitCount = 0;
    int byte;
    while ((byte = fgetc(payload)) != EOF) {
        for (int bit = 0; bit < 8; bit++) {
            if (read_ppm_pixel(input, &pixel)) {
                uint8_t payloadBit = (byte >> bit) & 0x01;
                pixel.blue = (pixel.blue & 0xFE) | payloadBit;
                write_ppm_pixel(output, &pixel);
                bitCount++;

                if (bitCount == payloadSize * 8) {
                    // Payload fully encoded
                    fclose(input);
                    fclose(payload);
                    fclose(output);
                    return 1;
                }
            } else {
                fprintf(stderr, "Failed to read input PPM pixel.\n");
                fclose(input);
                fclose(payload);
                fclose(output);
                return 0;
            }
        }
    }

    fprintf(stderr, "Payload size exceeds available space in the input PPM.\n");
    fclose(input);
    fclose(payload);
    fclose(output);
    return 0;
}

int decode_payload(const char *inputFile, const char *outputFile) {
    FILE *input = fopen(inputFile, "rb");
    if (!input) {
        fprintf(stderr, "Failed to open input file: %s\n", inputFile);
        return 0;
    }

    FILE *output = fopen(outputFile, "wb");
    if (!output) {
        fprintf(stderr, "Failed to create output file: %s\n", outputFile);
        fclose(input);
        return 0;
    }

    PPM_Header header;
    if (!read_ppm_header(input, &header)) {
        fprintf(stderr, "Failed to read input PPM header.\n");
        fclose(input);
        fclose(output);
        return 0;
    }

    if (header.width * header.height < 16) {
        fprintf(stderr, "Invalid input PPM dimensions. No payload to decode.\n");
        fclose(input);
        fclose(output);
        return 0;
    }

    // Read payload size
    uint16_t payloadSize;
    if (fread(&payloadSize, sizeof(uint16_t), 1, input) != 1) {
        fprintf(stderr, "Failed to read payload size from input PPM.\n");
        fclose(input);
        fclose(output);
        return 0;
    }

    PPM_Pixel pixel;
    uint8_t byte = 0;
    int bitCount = 0;
    while (bitCount < payloadSize * 8 && read_ppm_pixel(input, &pixel)) {
        uint8_t payloadBit = pixel.blue & 0x01;
        byte |= (payloadBit << (bitCount % 8));

        if ((bitCount + 1) % 8 == 0) {
            fputc(byte, output);
            byte = 0;
        }

        bitCount++;
    }

    if (bitCount < payloadSize * 8) {
        fprintf(stderr, "Failed to fully decode payload. Incomplete data.\n");
        fclose(input);
        fclose(output);
        return 0;
    }

    fclose(input);
    fclose(output);
    return 1;
}

void encode_bit(PPM_Pixel *p, uint8_t bit) {
    uint8_t green_lsb = p->green & 1;  // Extract the LSB of green
    uint8_t blue_lsb = p->blue & 1;    // Extract the LSB of blue

    if (green_lsb ^ blue_lsb != bit) {
        // Toggle the LSB of blue
        p->blue ^= 1;
    }
}


void encode_byte(PPM_Pixel *p, uint8_t byte) {
    for (int i = 7; i >= 0; --i) {
        uint8_t bit = (byte >> i) & 0x1;
        encode_bit(&p[i], bit);
    }
}

uint8_t decode_bit(PPM_Pixel p) { return (p.green & 0x1) ^ (p.blue & 0x1); }

uint8_t decode_byte(PPM_Pixel *p) {
    uint8_t byte = 0;

    for (int i = 7; i >= 0; --i) {
        uint8_t bit = decode_bit(p[i]);
        byte |= bit << i;
    }

    return byte;
}

// All tests below
void test_encode_bit1(void) {
    PPM_Pixel p;
    p.red = 0;
    p.green = 0;
    p.blue = 0;
    uint8_t bit = 0;
    encode_bit(&p, bit);
    if (p.red != 0 || p.green != 0 || p.blue != 0) {
        printf("Error test_encode_bit 1\n");
    }
}
void test_encode_bit2(void) {
    PPM_Pixel p;
    p.red = 0;
    p.green = 0;
    p.blue = 0;
    uint8_t bit = 1;
    encode_bit(&p, bit);
    if (p.red != 0 || p.green != 0 || p.blue != 1) {
        printf("Error test_encode_bit 2\n");
    }
}
void test_encode_bit3(void) {
    PPM_Pixel p;
    p.red = 0;
    p.green = 0;
    p.blue = 1;
    uint8_t bit = 1;
    encode_bit(&p, bit);
    if (p.red != 0 || p.green != 0 || p.blue != 1) {
        printf("Error test_encode_bit 3\n");
    }
}

void test_encode_bit(void) {
    test_encode_bit1();
    test_encode_bit2();
    test_encode_bit3();
}
void test_encode_byte1(void) {
    int test_num = 1;
    PPM_Pixel p[8];
    p[0].red = 0;
    p[0].green = 0;
    p[0].blue = 0;
    p[1].red = 0;
    p[1].green = 0;
    p[1].blue = 0;
    p[2].red = 0;
    p[2].green = 0;
    p[2].blue = 0;
    p[3].red = 0;
    p[3].green = 0;
    p[3].blue = 0;
    p[4].red = 0;
    p[4].green = 0;
    p[4].blue = 0;
    p[5].red = 0;
    p[5].green = 0;
    p[5].blue = 0;
    p[6].red = 0;
    p[6].green = 0;
    p[6].blue = 0;
    p[7].red = 0;
    p[7].green = 0;
    p[7].blue = 0;

    PPM_Pixel p_copy[8];
    for (int i = 0; i < 8; ++i) {
        p_copy[i] = p[i];
    }

    uint8_t byte = 0xFF;

    encode_byte(p_copy, byte);

    // Ensure red / green not modified
    for (int i = 0; i < 8; ++i) {
        if (p[i].red != p_copy[i].red) {
            printf("Error test_encode_byte %i, pixel %i has differing red values\n",
                   test_num, i);
        }
        if (p[i].green != p_copy[i].green) {
            printf("Error test_encode_byte %i, pixel %i has differing green values\n",
                   test_num, i);
        }
    }

    // Ensure blue matches what it should
    if (p_copy[0].blue != 1 || p_copy[1].blue != 1 || p_copy[2].blue != 1 ||
        p_copy[3].blue != 1 || p_copy[4].blue != 1 || p_copy[5].blue != 1 ||
        p_copy[6].blue != 1 || p_copy[7].blue != 1) {
        printf("Error test_encode_byte %i, blue values not expected\n", test_num);
    }
}
void test_encode_byte2(void) {
    int test_num = 2;
    PPM_Pixel p[8];
    p[0].red = 255;
    p[0].green = 255;
    p[0].blue = 255;
    p[1].red = 255;
    p[1].green = 255;
    p[1].blue = 255;
    p[2].red = 255;
    p[2].green = 255;
    p[2].blue = 255;
    p[3].red = 255;
    p[3].green = 255;
    p[3].blue = 255;
    p[4].red = 255;
    p[4].green = 255;
    p[4].blue = 255;
    p[5].red = 255;
    p[5].green = 255;
    p[5].blue = 255;
    p[6].red = 255;
    p[6].green = 255;
    p[6].blue = 255;
    p[7].red = 255;
    p[7].green = 255;
    p[7].blue = 255;

    PPM_Pixel p_copy[8];
    for (int i = 0; i < 8; ++i) {
        p_copy[i] = p[i];
    }

    uint8_t byte = 0xFF;

    encode_byte(p_copy, byte);

    // Ensure red / green not modified
    for (int i = 0; i < 8; ++i) {
        if (p[i].red != p_copy[i].red) {
            printf("Error test_encode_byte %i, pixel %i has differing red values\n",
                   test_num, i);
        }
        if (p[i].green != p_copy[i].green) {
            printf("Error test_encode_byte %i, pixel %i has differing green values\n",
                   test_num, i);
        }
    }

    // Ensure blue matches what it should
    if (p_copy[0].blue != 254 || p_copy[1].blue != 254 || p_copy[2].blue != 254 ||
        p_copy[3].blue != 254 || p_copy[4].blue != 254 || p_copy[5].blue != 254 ||
        p_copy[6].blue != 254 || p_copy[7].blue != 254) {
        printf("Error test_encode_byte %i, blue values not expected\n", test_num);
    }
}
void test_encode_byte3(void) {
    int test_num = 3;
    PPM_Pixel p[8];
    p[0].red = 255;
    p[0].green = 255;
    p[0].blue = 255;
    p[1].red = 255;
    p[1].green = 255;
    p[1].blue = 255;
    p[2].red = 255;
    p[2].green = 255;
    p[2].blue = 255;
    p[3].red = 255;
    p[3].green = 255;
    p[3].blue = 255;
    p[4].red = 255;
    p[4].green = 255;
    p[4].blue = 255;
    p[5].red = 255;
    p[5].green = 255;
    p[5].blue = 255;
    p[6].red = 255;
    p[6].green = 255;
    p[6].blue = 255;
    p[7].red = 255;
    p[7].green = 255;
    p[7].blue = 255;

    PPM_Pixel p_copy[8];
    for (int i = 0; i < 8; ++i) {
        p_copy[i] = p[i];
    }

    uint8_t byte = 0xAA;

    encode_byte(p_copy, byte);

    // Ensure red / green not modified
    for (int i = 0; i < 8; ++i) {
        if (p[i].red != p_copy[i].red) {
            printf("Error test_encode_byte %i, pixel %i has differing red values\n",
                   test_num, i);
        }
        if (p[i].green != p_copy[i].green) {
            printf("Error test_encode_byte %i, pixel %i has differing green values\n",
                   test_num, i);
        }
    }

    // Ensure blue matches what it should
    if (p_copy[0].blue != 255 || p_copy[1].blue != 254 || p_copy[2].blue != 255 ||
        p_copy[3].blue != 254 || p_copy[4].blue != 255 || p_copy[5].blue != 254 ||
        p_copy[6].blue != 255 || p_copy[7].blue != 254) {
        printf("Error test_encode_byte %i, blue values not expected\n", test_num);
    }
}
void test_encode_byte(void) {
    test_encode_byte1();
    test_encode_byte2();
    test_encode_byte3();
}

void test_decode_bit1(void) {
    PPM_Pixel p;
    p.red = 0;
    p.green = 0;
    p.blue = 0;
    if (decode_bit(p) != 0) {
        printf("Error test_decode_bit 1\n");
    }
}
//intentional to make it failed red=0, green=0
void test_decode_bit2(void) {
    PPM_Pixel p;
    p.red = 0;
    p.green = 0;
    p.blue = 1;
    if (decode_bit(p) != 1) {
        printf("Error test_decode_bit 2\n");
    }
}

void test_decode_bit(void) {
    test_decode_bit1();
    test_decode_bit2();
}

void test_decode_byte1(void) {
    int test_num = 1;
    PPM_Pixel p[8];
    p[0].red = 0;
    p[0].green = 0;
    p[0].blue = 0;
    p[1].red = 0;
    p[1].green = 0;
    p[1].blue = 0;
    p[2].red = 0;
    p[2].green = 0;
    p[2].blue = 0;
    p[3].red = 0;
    p[3].green = 0;
    p[3].blue = 0;
    p[4].red = 0;
    p[4].green = 0;
    p[4].blue = 0;
    p[5].red = 0;
    p[5].green = 0;
    p[5].blue = 0;
    p[6].red = 0;
    p[6].green = 0;
    p[6].blue = 0;
    p[7].red = 0;
    p[7].green = 0;
    p[7].blue = 0;

    uint8_t byte = decode_byte(p);
    uint8_t expected = 0x00;

    if (byte != expected) {
        printf("Error test_decode_byte %d\n", test_num);
    }
}

void test_decode_byte(void) { test_decode_byte1(); }

void test_encode_decode(void) {
    for (int i = 0; i < 100; ++i) {
        test_encode_decode_random();
    }
}
void test_encode_decode_random(void) {
    // Generate an array of random pixels
    PPM_Pixel pixels[8];
    for (int i = 0; i < 8; ++i) {
        pixels[i].red = (uint8_t)rand() % UINT8_MAX;
        pixels[i].green = (uint8_t)rand() % UINT8_MAX;
        pixels[i].blue = (uint8_t)rand() % UINT8_MAX;
    }

    // Generate a random byte
    uint8_t byte = (uint8_t)rand() % UINT8_MAX;

    // Encode
    encode_byte(pixels, byte);

    // Decode
    uint8_t decoded = decode_byte(pixels);

    // Verify
    if (byte != decoded) {
        printf("Error in encode_decode_random\n");
        printf("Started with %x\n", byte);
        printf("Decoded %x\n", decoded);
    }
}
