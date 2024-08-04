#include <cstdarg>
#include <memory>

#include "hephaestus/common/string.h"

using string  = std::string;
using str_ptr = std::shared_ptr<string>;

namespace Hephaestus {

str_ptr format(const char* fmt, ...) {

    // Create argument list and allow traversal. Note: fmt and remaining args
    // are all considered part of the argument list, but, making them separate,
    // arguments to the function helps my understanding.
    va_list args;
    va_start(args, fmt);

    // When we pass the arg list to a function, it's a one-way street; we won't know what
    // state the iterable is in once the function is done. Instead create a copy that
    // has no impact on the original iterable.
    va_list argsCopy;
    va_copy(argsCopy, args);

    // Determine the size needed to actually construct the formatted string including null-terminator.
    int formattedSize = std::vsnprintf(nullptr, 0, fmt, argsCopy) + 1;
    va_end(argsCopy);

    // Create a new string with the desired format and values.
    str_ptr sPtr = std::make_shared<string>(string(formattedSize, 0));
    (void)std::vsnprintf((*sPtr).data(), formattedSize, fmt, args);
    va_end(args);

    return sPtr;
}

}    // namespace Hephaestus