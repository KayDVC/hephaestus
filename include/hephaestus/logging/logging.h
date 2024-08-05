#ifndef HEPHAESTUS_LOGGING_H
#define HEPHAESTUS_LOGGING_H

#include <cstdint>
#include <string>

#include "hephaestus/common/string.h"
#include "hephaestus/common/types.h"

namespace Hephaestus {

///////////////////////////////////////////////////////////////////////////////
/// @brief A numeric representation of a log message's severity/importance
///	level.
///////////////////////////////////////////////////////////////////////////////
enum class LogLevel : uint8_t {
    DEBUG = 0,
    INFO,
    WARNING,
    ERROR,
    CRITICAL,
};

///////////////////////////////////////////////////////////////////////////////
/// @brief Potentially useful utilities used enums.
///////////////////////////////////////////////////////////////////////////////
constexpr const char* toString(const LogLevel& level) {
    switch (level) {
        case LogLevel::DEBUG   : return "DEBUG";
        case LogLevel::INFO    : return "INFO";
        case LogLevel::WARNING : return "WARNING";
        case LogLevel::ERROR   : return "ERROR";
        case LogLevel::CRITICAL: return "CRITICAL";
    }
}

///////////////////////////////////////////////////////////////////////////////
/// @brief Common operators used on log levels.
///////////////////////////////////////////////////////////////////////////////
CREATE_OSTREAM_OPERATOR_ENUM(LogLevel);
CREATE_BOOLEAN_OPERATORS_ENUM(LogLevel, uint8_t);

class Logger {

  public:

    ///////////////////////////////////////////////////////////////////////////////
    /// @brief Sets the lowest log level to pipe to output.
    ///
    /// @param _minLevel the lowest level to output. Any levels above level will
    ///	also be output. Defaults to DEBUG.
    /// @param _out the output stream to log messages to. Defaults to standard
    /// error.
    ///
    /// @note Using a raw pointer rather than a smart pointer is a conscience
    /// decision here. There's no particular reason why we'd want to delete an
    /// output stream when this logger object is destructed. The caller assumes
    /// full responsibility for dealing closing and/or releasing the stream.
    /// Oh and don't pass a nullptr :).
    ///////////////////////////////////////////////////////////////////////////////
    explicit Logger(const LogLevel _minLevel = LogLevel::DEBUG, std::ostream* _out = &std::cerr);
    ~Logger() = default;

    ///////////////////////////////////////////////////////////////////////////////
    /// @brief Sets the lowest log level to pipe to output.
    ///
    /// @param minLevel the lowest level to output. Any levels above level will
    ///	also be output.
    ///////////////////////////////////////////////////////////////////////////////
    void setLevel(const LogLevel minLevel);

    ///////////////////////////////////////////////////////////////////////////////
    /// @brief Sets the lowest log level to pipe to output.
    ///
    ///	@return the lowest level logs currently being output.
    ///////////////////////////////////////////////////////////////////////////////
    LogLevel getLevel() const;

    // TODO: Cleanup Ostream support. Log function should be using write & flush methods.

    ///////////////////////////////////////////////////////////////////////////////
    /// @brief Pipes a message to output based on log level.
    ///
    /// @param level the log message's level.
    /// @param msg 	a string containing the message to output.
    ///
    /// @return True if msg successfully written to output stream; false otherwise.
    ///////////////////////////////////////////////////////////////////////////////
    bool log(const LogLevel level, const std::string& msg) const;

  private:

    LogLevel      minLevel;
    std::ostream* out;
};

// A logger that can be used without any additional configurations.
const Logger defaultLog { LogLevel::DEBUG };

///////////////////////////////////////////////////////////////////////////////
/// @brief Records a log at the specified level after formatting string.
///
/// @param logger the logger object to use.
/// @param level the log message's level.
/// @param fmt the c-style format template for the log msg.
/// @param ... a list of parameters to use when formatting the log msg.
///
/// @return True if formatted message written to output stream; false otherwise.
///////////////////////////////////////////////////////////////////////////////
// clang-format off: Begin Macro Definition
#define HEPHAESTUS_LOG_MSG(logger, level, fmt, ...)                                                                 \
    logger.log(level,                                                                                               \
        *(Hephaestus::format(                                                                                       \
                "[ %-8s | %s:%d ] %s",                                                                              \
                Hephaestus::toString(level),                                                                        \
                __func__,                                                                                           \
                __LINE__,                                                                                           \
                Hephaestus::format(fmt, __VA_ARGS__)->c_str()                                                       \
            )                                                                                                       \
        )                                                                                                           \
    );
// clang-format on: End Macro Definition

// Intellisense doesn't pick up on the shared documentation for this block of related macros.
// There may be a better way to do this, but for now, copy pasta it is :).

///////////////////////////////////////////////////////////////////////////////
/// @brief Logs a message at the debug level using the default logger.
///
/// @param fmt the c-style format template for the log msg.
/// @param ... a list of parameters to use when formatting the log msg.
///////////////////////////////////////////////////////////////////////////////
#define HEPHAESTUS_LOG_DEBUG(fmt, ...)                                                                                 \
    (void)HEPHAESTUS_LOG_MSG(Hephaestus::defaultLog, LogLevel::DEBUG, fmt, __VA_ARGS__);
///////////////////////////////////////////////////////////////////////////////
/// @brief Logs a message at the info level using the default logger.
///
/// @param fmt the c-style format template for the log msg.
/// @param ... a list of parameters to use when formatting the log msg.
///////////////////////////////////////////////////////////////////////////////
#define HEPHAESTUS_LOG_INFO(fmt, ...)                                                                                  \
    (void)HEPHAESTUS_LOG_MSG(Hephaestus::defaultLog, LogLevel::INFO, fmt, __VA_ARGS__);
///////////////////////////////////////////////////////////////////////////////
/// @brief Logs a message at the warning level using the default logger.
///
/// @param fmt the c-style format template for the log msg.
/// @param ... a list of parameters to use when formatting the log msg.
///////////////////////////////////////////////////////////////////////////////
#define HEPHAESTUS_LOG_WARN(fmt, ...)                                                                                  \
    (void)HEPHAESTUS_LOG_MSG(Hephaestus::defaultLog, LogLevel::WARNING, fmt, __VA_ARGS__);
///////////////////////////////////////////////////////////////////////////////
/// @brief Logs a message at the error level using the default logger.
///
/// @param fmt the c-style format template for the log msg.
/// @param ... a list of parameters to use when formatting the log msg.
///////////////////////////////////////////////////////////////////////////////
#define HEPHAESTUS_LOG_ERROR(fmt, ...)                                                                                 \
    (void)HEPHAESTUS_LOG_MSG(Hephaestus::defaultLog, LogLevel::ERROR, fmt, __VA_ARGS__);
///////////////////////////////////////////////////////////////////////////////
/// @brief Logs a message at the critical level using the default logger.
///
/// @param fmt the c-style format template for the log msg.
/// @param ... a list of parameters to use when formatting the log msg.
///////////////////////////////////////////////////////////////////////////////
#define HEPHAESTUS_LOG_CRITICAL(fmt, ...)                                                                              \
    (void)HEPHAESTUS_LOG_MSG(Hephaestus::defaultLog, LogLevel::CRITICAL, fmt, __VA_ARGS__);

}    // namespace Hephaestus

#endif    // HEPHAESTUS_LOGGING_H