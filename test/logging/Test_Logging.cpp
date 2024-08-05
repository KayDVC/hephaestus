#include "gtest/gtest.h"

#include "hephaestus/logging/logging.h"
#include "logging/logging.cpp"

using Logger   = Hephaestus::Logger;
using LogLevel = Hephaestus::LogLevel;

TEST(LoggerTest, Instantiation) {
    Logger logger;

    ASSERT_EQ(logger.getLevel(), LogLevel::DEBUG);

    Logger logger2 { LogLevel::INFO };

    ASSERT_EQ(logger2.getLevel(), LogLevel::INFO);
}