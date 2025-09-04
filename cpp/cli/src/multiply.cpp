#include "multiply.h"
#include <iostream>

void handle_multiply(CLI::App* multiply_cmd) {
    int x, y;
    multiply_cmd->add_option("x", x, "First number")->required();
    multiply_cmd->add_option("y", y, "Second number")->required();
    multiply_cmd->callback([multiply_cmd, x, y]() {
        std::cout << "Multiply: " << x << " * " << y << " = " << (x * y) << std::endl;
        auto extras = multiply_cmd->remaining();
        if (!extras.empty()) {
            std::cout << "Extra args for multiply:";
            for (const auto &e : extras) std::cout << " " << e;
            std::cout << std::endl;
        }
    });
}
