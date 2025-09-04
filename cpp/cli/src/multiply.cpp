#include "multiply.h"
#include <iostream>

struct multiply_options {
    int x;
    int y;
};

void build_multiply_subcmd(CLI::App& app) {
    auto multiply_cmd = app.add_subcommand("multiply", "Multiply two numbers");
    multiply_cmd->allow_extras();
    // make a shared object to hold options
    auto multiply_opts = std::make_shared<multiply_options>();
    multiply_cmd->add_option("x", multiply_opts->x, "First number")->required();
    multiply_cmd->add_option("y", multiply_opts->y, "Second number")->required();
    multiply_cmd->callback([multiply_opts]() {
        std::cout << "Multiply: " << multiply_opts->x << " * " << multiply_opts->y << " = " << (multiply_opts->x * multiply_opts->y) << std::endl;
    });
}
