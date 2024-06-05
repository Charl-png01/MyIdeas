
#include <stdio.h>
#include <stdlib.h>
#include "picture.h"
#include "test_function.h"

static void print_drawing_message(int width, int height) {
    printf("Drawing %d x %d:\n", width, height);
}

int main(int argc, char* argv[]) {
    if (argc < 3) {
        printf("Usage: %s <width> <height> [rule]\n", argv[0]);
        return 1;
    }

    int width = (int) strtol(argv[1], NULL, 10);
    int height = (int) strtol(argv[2], NULL, 10);

    if (width <= 0 || height <= 0) {
        printf("Invalid width or height\n");
        return 1;
    }

    int rule = 0;
    if (argc >= 4) {
        rule = (int) strtol(argv[3], NULL, 10);
    }

    print_drawing_message(width, height);

    if (rule == 0) {
        printf("Rule 18:\n");
        rule_18_picture(width, height);

        printf("\nRule 57:\n");
        rule_57_picture(width, height);

        printf("\nRule 60:\n");
        rule_60_picture(width, height);

        printf("\nRule 73:\n");
        rule_73_picture(width, height);
    } else {
        switch (rule) {
            case 18:
                rule_18_picture(width, height);
                break;
            case 57:
                rule_57_picture(width, height);
                break;
            case 60:
                rule_60_picture(width, height);
                break;
            case 73:
                rule_73_picture(width, height);
                break;
            default:
                printf("Invalid rule\n");
                return 1;
        }
    }


//call test function
    test_rule_18();
    test_rule_57();
    test_rule_60();
    test_rule_73();



    return 0;
}

