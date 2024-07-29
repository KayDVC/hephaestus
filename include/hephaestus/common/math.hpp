#ifndef MATH_H
#define MATH_H

#include <cmath>

/************************************************************
 * @brief A set of wrapper functions or custom implementations
 * of useful mathematical functions.
 ************************************************************/

namespace Hephaestus {

    uint32_t abs(int value){
        return static_cast<uint32_t>(std::abs(value));
    }

}

#endif


