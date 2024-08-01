#ifndef LOGGER_H
#define LOGGER_H

#include <cstdint>

namespace Hephaestus {

//  Using an enum class here removes common ambiguity errors. A few extra lines work in operator defintions
//  will save a good bit of headache later; I'll take that trade any day. 
enum class LogLevel : uint8_t {
    None = 0,
    Debug,
    Info,
    Warning,
    Error,
    Critical
};

///////////////////////////////////////////////////////////////////////////////
/// @brief Common operators used on log levels.
///////////////////////////////////////////////////////////////////////////////
constexpr bool operator<<(LogLevel lhs, LogLevel rhs){

};

class Logger {

public:


private: 
    uint8_t level;

};

}

#endif /* LOGGER_H */