#include <stdio.h>
#include <string.h>
#include <ctype.h>

// function to check if a character is a vowel
int is_vowel(char c) {
    return (c == 'a' || c == 'e' || c == 'i' || c == 'o' || c == 'u' || c == 'y');
}

// function to convert a sentence to pig latin
void pig_latin(char *input) {
    char output[100];    // the output string to store the converted sentence
    char word[50];       // a buffer to store each word being processed
    int word_len = 0;    // length of the current word
    int j = 0;           // current position in the output string

    //  if a character is a letter assign it to word.
    for (int i = 0; i <= strlen(input); i++) {
        if (isalpha(input[i])) {
            word[word_len++] = input[i];
        } else {    // if the character is not a letter
            if (word_len > 0) {
                word[word_len] = '\0';
                // check if the word starts with a vowel or "y" followed by a vowel add "yay"
                if (is_vowel(word[0]) || (word_len > 1 && word[0] == 'y' && is_vowel(word[1]))) {
                    strcpy(output + j, word);
                    j += word_len;
                    strcpy(output + j, "yay");
                    j += 3;
                } else {    // if the word starts with a consonant
                    int start_consonants = 0;
                    // find the position of the first vowel in the word
                    for (int k = 0; k < word_len; k++) {
                        if (is_vowel(word[k])) {
                            start_consonants = k;
                            break;
                        }
                    }
                    // move the consonants at the beginning of the word to the end
                    strcpy(output + j, word + start_consonants);
                    j += word_len - start_consonants;
                    strncpy(output + j, word, start_consonants);
                    j += start_consonants;
                    strcpy(output + j, "ay");// add "ay" to the end of the word
                    j += 2;
                }
                // reset the word length to 0 and add current non-letter to the output
                word_len = 0;
                *(output + j++) = input[i];
            } else {
                *(output + j++) = input[i];
            }
        }
    }

    *(output + j) = '\0';
    printf("%s", output);
}

// main function
int main() {
    char input[100];
    printf("Enter text to be encoded: ");
    scanf("%99[^\n]", input);    // read input sentence from user
    pig_latin(input);    // convert the input sentence to pig latin
    return 0;
}