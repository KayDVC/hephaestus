#ifndef HEPHAESTUS_MATH_H
#define HEPHAESTUS_MATH_H

#include <cmath>

///////////////////////////////////////////////////////////////////////////////
/// @brief A set of wrapper functions or custom implementations of useful
/// mathematical functions.
///////////////////////////////////////////////////////////////////////////////

namespace Hephaestus {

uint32_t abs(int value) {
    return static_cast<uint32_t>(std::abs(value));
}

}    // namespace Hephaestus

#endif    // HEPHAESTUS_MATH_H
