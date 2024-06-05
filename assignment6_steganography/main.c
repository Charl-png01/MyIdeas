#include <stdio.h>
#include <string.h>
#include "steganography.h"
#include "ppm.h"
#include <time.h>

int main(int argc, char *argv[]) {
    //Call test functions
    srand((unsigned) time(NULL));
    test_encode_bit();
    test_encode_bit1();
    test_encode_bit2();
    test_encode_bit3();
    test_encode_byte();
    test_encode_byte1();
    test_encode_byte2();
    test_encode_byte3();
    test_decode_bit1();
    test_decode_bit2();
    test_decode_byte();
    test_decode_byte1();
    test_encode_decode();
    test_encode_decode_random();

    if (argc < 4) {
        fprintf(stderr, "Usage: %s [encode|decode] input.ppm [payload.ext] output.ppm\n", argv[0]);
        return 1;
    }

    char *mode = argv[1];
    char *inputFile = argv[2];
    char *outputFile = argv[argc - 1];

    if (strcmp(mode, "encode") == 0) {
        if (argc != 5) {
            fprintf(stderr, "Invalid number of arguments for encode mode.\n");
            return 1;
        }

        char *payloadFile = argv[3];
        if (encode_payload(inputFile, payloadFile, outputFile)) {
            printf("Encoding successful. Output file: %s\n", outputFile);
        } else {
            fprintf(stderr, "Encoding failed.\n");
        }
    } else if (strcmp(mode, "decode") == 0) {
        if (argc != 4) {
            fprintf(stderr, "Invalid number of arguments for decode mode.\n");
            return 1;
        }

        if (decode_payload(inputFile, outputFile)) {
            printf("Decoding successful. Output file: %s\n", outputFile);
        } else {
            fprintf(stderr, "Decoding failed.\n");
        }
    } else {
        fprintf(stderr, "Invalid mode: %s. Must be 'encode' or 'decode'.\n", mode);
        return 1;
    }


    return 0;
}
