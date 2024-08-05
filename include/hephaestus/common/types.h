#ifndef HEPHAESTUS_TYPES_H
#define HEPHAESTUS_TYPES_H

#include <iostream>

namespace Hephaestus {

///////////////////////////////////////////////////////////////////////////////
/// @brief Defines output behavior for enum values.
///
/// @param name the name of the enum class.
/// @note This function relies on the definition of a toString function for a
/// given enum class type.
///////////////////////////////////////////////////////////////////////////////
// clang-format off: Begin Macro Definition
#define CREATE_OSTREAM_OPERATOR_ENUM(name)                                                                          \
constexpr std::ostream& operator<<(std::ostream& os, const name value) {                                            \
    os << toString(value);                                                                                          \
    return os;                                                                                                      \
}
// clang-format on: End Macro Definition

///////////////////////////////////////////////////////////////////////////////
/// @brief Defines comparison operators for enum classes with simple types.
///
/// @param name the name of the enum class.
/// @param u_type the underlying type of the enum class.
///////////////////////////////////////////////////////////////////////////////
// clang-format off: Begin Macro Definition
#define CREATE_BOOLEAN_OPERATORS_ENUM(name, u_type)                                                                \
constexpr bool operator==(const name lhs, const name rhs) {                                                        \
    return static_cast<u_type>(lhs) == static_cast<u_type>(rhs);                                                   \
}                                                                                                                  \
constexpr bool operator!=(const name lhs, const name rhs) {                                                        \
    return !(lhs == rhs);                                                                                          \
}                                                                                                                  \
constexpr bool operator<( const name lhs, name rhs) {                                                              \
    return static_cast<u_type>(lhs) < static_cast<u_type>(rhs);                                                    \
}                                                                                                                  \
constexpr bool operator>(const name lhs, const name rhs) {                                                         \
    return rhs < lhs;                                                                                              \
}                                                                                                                  \
constexpr bool operator<=(const name lhs, const name rhs) {                                                        \
    return !(lhs > rhs);                                                                                           \
}                                                                                                                  \
constexpr bool operator>=(const name lhs, const name rhs) {                                                        \
    return !(lhs < rhs);                                                                                           \
}
// clang-format on: End Macro Definition

}    // namespace Hephaestus

#endif    // HEPHAESTUS_TYPES_H