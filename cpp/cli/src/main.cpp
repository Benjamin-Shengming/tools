#include <string>
#include "spdlog/spdlog.h"
#include "CLI11.hpp"
#include <cstdio>
#include <iostream>
#include <string>
#include <vector>

#include "add.h"
#include "multiply.h"
#include "stacktrace.h"
#include "log.h"
#include "common.h"



int main(int argc, char** argv) {
    // install signal handlers for stack traces
    stacktrace::install_signal_handlers();

    // create main app and  regiser all subcommands
    MainApp app {"Example CLI11 tool mimicking Python Typer"};
    // Register all Subcommands
    app.add_subcommand(std::make_unique<AddCmdApp>());
    app.add_subcommand(std::make_unique<MultiplyCmdApp>());

    // ------------------------
    // Parse arguments
    // ------------------------
    app.parse(argc, argv);
    return 0;
}

