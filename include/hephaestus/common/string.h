#ifndef HEPHAESTUS_STRING_H
#define HEPHAESTUS_STRING_H

#include <memory>
#include <string>

///////////////////////////////////////////////////////////////////////////////
/// @brief A set of custom implementations for various string related
/// operations.
///////////////////////////////////////////////////////////////////////////////

namespace Hephaestus {

///////////////////////////////////////////////////////////////////////////////
/// @brief Creates a string using c-style string formatting.
///
/// @param fmt the c-style format template.
/// @param ... an n-length list of  parameters to use when filling the string
/// template.
///
/// @return a string with the
/// @note Use std::format if using C++20 or above.
///////////////////////////////////////////////////////////////////////////////
std::shared_ptr<std::string> format(const char* fmt, ...);

}    // namespace Hephaestus

#endif    // HEPHAESTUS_STRING_H
