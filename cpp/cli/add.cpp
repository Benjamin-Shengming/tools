
#include "add.h"
#include <iostream>
#include <spdlog/fmt/ranges.h>
#include <spdlog/spdlog.h>

struct add_config {
  int a;
  int b;
};

void build_add_subcmd(CLI::App &app) {
  add_config config;
  auto sub_cmd = app.add_subcommand("add", "Add two numbers");
  sub_cmd->add_option("a", config.a, "First number")->required();
  sub_cmd->add_option("b", config.b, "Second number")->required();
  sub_cmd->allow_extras();
  sub_cmd->callback([config]() {
    spdlog::debug("Add command called with a={}, b={}", config.a, config.b);
    std::cout << "Add: " << config.a << " + " << config.b << " = "
              << (config.a + config.b) << std::endl;

    spdlog::debug("return from build ");
  });
}
