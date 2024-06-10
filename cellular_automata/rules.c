//
// Created by Charles Kokofi on 5/18/23.
//

#include "rules.h"
#include <stdbool.h>

bool rule_18(bool left, bool center, bool right) {
    return (left && !center && !right) || (!left && !center && right);
}

bool rule_57(bool left, bool center, bool right) {
    return (left && !center && right) || (left && !center && !right) || (!left && center && right) ||
           (!left && !center && !right);
}

bool rule_60(bool left, bool center, bool right) {
    return (left && !center && right) || (left && !center && !right) || (!left && center && right) ||
           (!left && center && !right);
}

bool rule_73(bool left, bool center, bool right) {
    return (left && center && !right) || (!left && center && right) || (!left && !center && !right) ;
}