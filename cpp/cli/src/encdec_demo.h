#pragma once
#include "CLI11.hpp"

class EncodeDemoCmdApp : public CLI::App {
public:
    EncodeDemoCmdApp();
    void run();
};

class DecodeDemoCmdApp : public CLI::App {
public:
    DecodeDemoCmdApp();
    void run();
};
