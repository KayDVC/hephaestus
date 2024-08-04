#ifndef HEPHAESTUS_SIZES_H
#define HEPHAESTUS_SIZES_H

#include <cstdint>

///////////////////////////////////////////////////////////////////////////////
/// @brief Common sizes and units of measurement.
///////////////////////////////////////////////////////////////////////////////

namespace Hephaestus {

constexpr uint32_t _BIT_MULTIPLIER = 1024;
constexpr uint32_t KILOBYTE        = _BIT_MULTIPLIER;
constexpr uint32_t MEGABYTE        = KILOBYTE * _BIT_MULTIPLIER;

}    // namespace Hephaestus

#endif    // HEPHAESTUS_SIZES_H
