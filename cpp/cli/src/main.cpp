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

class CliApp : public CLI::App {
public:
    using CLI::App::App; // inherit constructors

    void add_shared_options() {
        auto shared_group = this->add_option_group("Shared", "Shared/global options");
        shared_group->add_flag("-v,--verbose", verbose_, "Enable verbose output");
        shared_group->add_option("-c,--config", config_file_, "Path to config file");
    }
protected:
    void pre_callback() override {
        printf("verbose: %s\n", verbose_ ? "true" : "false");
        if (verbose_) {
            setup_log(1);
        }
        else {
            setup_log(3);
        }
    }

    bool verbose_ = false;
    std::string config_file_ = "default.conf";
};


int main(int argc, char** argv) {
    stacktrace::install_signal_handlers();

    // TEST: Intentionally crash to verify stacktrace handler
    CliApp app{"Example CLI11 tool mimicking Python Typer"};
    // ------------------------
    // Shared/global options
    // ------------------------
    app.add_shared_options();


    // Subcommand: add
    build_add_subcmd(app);
    // Subcommand: multiply
    auto multiply_opts = build_multiply_subcmd(app);
    // ------------------------
    // Parse arguments
    // ------------------------
    app.parse(argc, argv);
    for (const auto& subcmd : app.get_subcommands()) {
        if (subcmd->parsed()) {
            if (subcmd->get_name() == "multiply") {
                run_multiply(app, multiply_opts);
            }
        }
    }   
    return 0;
}

