#include <cassert>
#include <iostream>
#include <string>

#include "hephaestus/logging/logging.h"

using String    = std::string;
using StreamPtr = std::ostream*;
namespace Hephaestus {

Logger::Logger(const LogLevel _minLevel, const StreamPtr _out) : minLevel(_minLevel), out(_out) {
    // Assuming makes an ass out of u and ming... not me :).
    assert((out != nullptr) && "Provided nullptr to output stream in Logger!");
}

void Logger::setLevel(const LogLevel minLevel) {
    this->minLevel = minLevel;
}

LogLevel Logger::getLevel() const {
    return this->minLevel;
}

bool Logger::log(const LogLevel level, const String& msg) const {

    // Simple level gating.
    if (level < this->minLevel) {
        return false;
    }

    (*out) << msg << std::endl;

    // Return the state of the stream post-write.
    return out->good();
}

}    // namespace Hephaestus