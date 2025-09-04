
#include "add.h"
#include <iostream>
#include <spdlog/fmt/ranges.h>
#include <spdlog/spdlog.h>

void handle_add(CLI::App* add_cmd) {
    int a, b;
    add_cmd->add_option("a", a, "First number")->required();
    add_cmd->add_option("b", b, "Second number")->required();
    add_cmd->callback([add_cmd, a, b]() {
        spdlog::debug("Add command called with a={}, b={}", a, b);
        std::cout << "Add: " << a << " + " << b << " = " << (a + b) << std::endl;
        spdlog::debug("get extra args for add");
        auto extras = add_cmd->remaining();
        spdlog::debug("after get extra args for add {}", (void*)&extras);

        if (!extras.empty()) {
            spdlog::debug("Extra args for add: {}", fmt::join(extras, ", "));
            std::cout << "Extra args for add:";
            for (const auto &e : extras) std::cout << " " << e;
            std::cout << std::endl;
        }
        spdlog::debug("return from add command");
    });
}
