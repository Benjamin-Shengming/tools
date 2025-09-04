#include <CLI11.hpp>
#include <iostream>
#include <string>
#include <vector>

int main(int argc, char** argv) {
    CLI::App app{"Example CLI11 tool mimicking Python Typer"};

    // ------------------------
    // Shared/global options
    // ------------------------
    bool verbose = false;
    std::string config_file = "default.conf";

    app.add_flag("-v,--verbose", verbose, "Enable verbose output");
    app.add_option("-c,--config", config_file, "Path to config file");

    // ------------------------
    // Subcommand: add
    // ------------------------
    auto add_cmd = app.add_subcommand("add", "Add two numbers");
    add_cmd->allow_extras(); // allow unknown options

    int a, b;
    add_cmd->add_option("a", a, "First number")->required();
    add_cmd->add_option("b", b, "Second number")->required();

    // ------------------------
    // Subcommand: multiply
    // ------------------------
    auto multiply_cmd = app.add_subcommand("multiply", "Multiply two numbers");
    multiply_cmd->allow_extras();

    int x, y;
    multiply_cmd->add_option("x", x, "First number")->required();
    multiply_cmd->add_option("y", y, "Second number")->required();

    // ------------------------
    // Parse arguments
    // ------------------------
    CLI11_PARSE(app, argc, argv);

    // ------------------------
    // Handle subcommands
    // ------------------------
    if (*add_cmd) {
    std::cout << "Add: " << a << " + " << b << " = " << (a + b) << std::endl;
        auto extras = add_cmd->remaining();
        if (!extras.empty()) {
            std::cout << "Extra args for add:";
            for (const auto &e : extras) std::cout << " " << e;
            std::cout << std::endl;
        }
    } else if (*multiply_cmd) {
    std::cout << "Multiply: " << x << " * " << y << " = " << (x * y) << std::endl;
        auto extras = multiply_cmd->remaining();
        if (!extras.empty()) {
            std::cout << "Extra args for multiply:";
            for (const auto &e : extras) std::cout << " " << e;
            std::cout << std::endl;
        }
    }

    // ------------------------
    // Handle shared options
    // ------------------------
    if (verbose) {
    std::cout << "[Verbose] Using config: " << config_file << std::endl;
    }

    return 0;
}

