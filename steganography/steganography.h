//
// Created by Charles Kokofi on 5/22/23.
//

#ifndef C_PROJECT_STEGANOGRAPHY_H
#define C_PROJECT_STEGANOGRAPHY_H
#include "ppm.h"
int encode_payload(const char *inputFile, const char *payloadFile, const char *outputFile);
int decode_payload(const char *inputFile, const char *outputFile);
void test_encode_decode_random(void);

// Function prototypes for test functions
void encode_bit(PPM_Pixel *p, uint8_t bit);
void test_encode_bit(void);
void test_encode_bit1(void);
void test_encode_bit2(void);
void test_encode_bit3(void);

void encode_byte(PPM_Pixel *p, uint8_t byte);
void test_encode_byte(void);
void test_encode_byte1(void);
void test_encode_byte2(void);
void test_encode_byte3(void);

uint8_t decode_bit(PPM_Pixel p);
void test_decode_bit1(void);
void test_decode_bit2(void);


uint8_t decode_byte(PPM_Pixel *p);
void test_decode_byte(void);
void test_decode_byte1(void);

void test_encode_decode(void);
void test_encode_decode_random(void);

#endif
