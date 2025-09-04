#include "spdlog/spdlog.h"
#include "CLI11.hpp"
#include <iostream>
#include <string>
#include <vector>

#include "add.h"
#include "multiply.h"
#include "stacktrace.h"
#include "log.h"


int main(int argc, char** argv) {
    setup_log(1);
    spdlog::info("Starting CLI application info");
    spdlog::debug("Starting CLI application debug");
    stacktrace::install_signal_handlers();

    // TEST: Intentionally crash to verify stacktrace handler
    CLI::App app{"Example CLI11 tool mimicking Python Typer"};

    // ------------------------
    // Shared/global options
    // ------------------------
    bool verbose = false;
    std::string config_file = "default.conf";

    auto shared_group = app.add_option_group("Shared", "Shared/global options");
    shared_group->add_flag("-v,--verbose", verbose, "Enable verbose output");
    shared_group->add_option("-c,--config", config_file, "Path to config file");


    // Subcommand: add
    build_add_subcmd(app);

    spdlog::debug("After handle_add");
    // Subcommand: multiply
    auto multiply_cmd = app.add_subcommand("multiply", "Multiply two numbers");
    multiply_cmd->allow_extras();
    handle_multiply(multiply_cmd);

    // ------------------------
    // Parse arguments
    // ------------------------

    app.parse(argc, argv);                                                                                      \
    // Subcommand logic handled in add.cpp and multiply.cpp
    return 0;
}

