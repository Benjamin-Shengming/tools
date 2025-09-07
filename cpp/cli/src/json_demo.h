#pragma once
#include "CLI11.hpp"

class JsonDemoCmdApp : public CLI::App {
public:
    JsonDemoCmdApp();
    void run();
};
