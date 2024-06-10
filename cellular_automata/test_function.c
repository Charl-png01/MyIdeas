//
// Created by Charles Kokofi on 5/18/23.
//
#include "test_function.h"
#include <stdbool.h>
#include <stdio.h>
#include "rules.h"

void test_rule_18(void) {

    if (rule_18(true, true, true) != false) {
        printf("Error rule 18 TTT\n");
    }
    if (rule_18(true, true, false) != false) {
        printf("Error rule 18 TTF\n");
    }
    if (rule_18(true, false, true) != false) {
        printf("Error rule 18 TFT\n");
    }
    if (rule_18(true, false, false) != true) {
        printf("Error rule 18 TFF\n");
    }
    if (rule_18(false, true, true) != false) {
        printf("Error rule 18 FTT\n");
    }
    if (rule_18(false, true, true) != false) {
        printf("Error rule 18FTT\n");
    }
    if (rule_18(false, false, true) != true) {
        printf("Error rule 18 FFT\n");
    }
    if (rule_18(false, false, false) != false) {
        printf("Error rule 18 FFF\n");
    }
}
void test_rule_57(void) {

    if (rule_57(true, true, true) != false) {
        printf("Error rule 57 TTT\n");
    }
    if (rule_57(true, true, false) != false) {
        printf("Error rule 57 TTF\n");
    }
    if (rule_57(true, false, true) != true) {
        printf("Error rule 57 TFT\n");
    }
    if (rule_57(true, false, false) != true) {
        printf("Error rule 57 TFF\n");
    }
    if (rule_57(false, true, true) != true) {
        printf("Error rule 57 FTT\n");
    }
    if (rule_57(false, true, true) != true) {
        printf("Error rule 57 FTT\n");
    }
    if (rule_57(false, false, true) != false) {
        printf("Error rule 57 FFT\n");
    }
    if (rule_57(false, false, false) != true) {
        printf("Error rule 57 FFF\n");
    }
}
void test_rule_60(void) {

    if (rule_60(true, true, true) != false) {
        printf("Error rule 60 TTT\n");
    }
    if (rule_60(true, true, false) != false) {
        printf("Error rule 60 TFF\n");
    }
    if (rule_60(true, false, true) != true) {
        printf("Error rule 60 TFF\n");
    }
    if (rule_60(true, false, false) != true) {
        printf("Error rule 60 TTT\n");
    }
    if (rule_60(false, true, true) != true) {
        printf("Error rule 60 TTT\n");
    }
    if (rule_60(false, true, true) != true) {
        printf("Error rule 60 TTT\n");
    }
    if (rule_60(false, false, true) != false) {
        printf("Error rule 60 TTT\n");
    }
    if (rule_60(false, false, false) != false) {
        printf("Error rule 60 TTT\n");
    }
}
void test_rule_73(void) {

    if (rule_73(true, true, true) != false) {
        printf("Error rule 73 TTT\n");
    }
    if (rule_73(true, true, false) != true) {
        printf("Error rule 73 TTF\n");
    }
    if (rule_73(true, false, true) != false) {
        printf("Error rule 73 TFT\n");
    }
    if (rule_73(true, false, false) != false) {
        printf("Error rule 73 TFF\n");
    }
    if (rule_73(false, true, true) != true) {
        printf("Error rule 73 FTT\n");
    }
    if (rule_73(false, true, false) != false) {
        printf("Error rule 73 FTT\n");
    }
    if (rule_73(false, false, true) != false) {
        printf("Error rule 73 FFT\n");
    }
    if (rule_73(false, false, false) != true) {
        printf("Error rule 73 FFF\n");
    }
}

