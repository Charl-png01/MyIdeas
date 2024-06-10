#include <stdio.h>
#include <ctype.h>
#include <math.h>
#include <string.h>

int approximate_alphabet(char *str) {
    int alphabet_size = 0;
    int used_chars[4] = {0}; // index 0 for lowercase, index 1 for uppercase, index 2 for digits, index 3 for symbols

    for (int i = 0; str[i] != '\0'; i++) {
        if (islower(str[i])) {
            used_chars[0]++;
        }
        else if (isupper(str[i])) {
            used_chars[1]++;
        }
        else if (isdigit(str[i])) {
            used_chars[2]++;
        }
        else {
            used_chars[3]++;
        }
    }

    if (used_chars[0] >0 ) { //if alphabet is lower add +26
        alphabet_size += 26;
    }
    if (used_chars[1] > 0) { //  if alphabet is upper add +26
        alphabet_size += 26;
    }

    if (used_chars[2] > 0) {//if isdigit add +10(0 to 9)
        alphabet_size += 10;
    }

    if (used_chars[3] > 0) {//if its symbol add +32
        alphabet_size += 32;
    }

    return alphabet_size;
}
//information content function using radomness to mean entropy
double information_content(int alphabet_size, size_t length) {
    double randomness = length * log2(alphabet_size);
    return randomness;
}

int main() {
    char string[101];

    printf("Enter a string : ");//take user input
    scanf("%100[^\n]",string);//read user input

    int alphabet_size = approximate_alphabet(string);//calling approximate function
    printf("Approximate Alphabet: %d\n", alphabet_size);

    double randomness = information_content(alphabet_size, strlen(string));//calling information content function
    printf("Length : %lu\n", strlen(string));

    printf("Information Content: %.2f bits\n", randomness);



    return 0;
}


