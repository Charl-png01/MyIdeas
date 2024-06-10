#include "substitution.h"
#include "percent.h"
int main(void) {

    //substitution cipher test
    test_encrypt_letter1();
    test_encrypt_letter2();
    test_encrypt_string1();
    test_encrypt_string2();
    test_encrypt_string3();
    test_encrypt_string4();

    //percent test
    test_percent_encode1();
    test_percent_encode2();
    test_percent_encode3();
    test_percent_encode4();

    return 0;
}
