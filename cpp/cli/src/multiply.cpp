#include "multiply.h"
#include <iostream>
#include <memory>
#include <ostream>

struct multiply_options {
  int x;
  int y;
};


std::shared_ptr<multiply_options> build_multiply_subcmd(CLI::App &app) {
  auto multiply_cmd = app.add_subcommand("multiply", "Multiply two numbers");
  multiply_cmd->allow_extras();
  // make a shared object to hold options
  auto multiply_opts = std::make_shared<multiply_options>();
  multiply_cmd->add_option("x", multiply_opts->x, "First number")->required();
  multiply_cmd->add_option("y", multiply_opts->y, "Second number")->required();
  return multiply_opts;

}

void run_multiply(CLI::App &app,
                  std::shared_ptr<multiply_options> multiply_opts) {
  auto multiply_cmd = app.get_subcommand("multiply");
  std::cout << "Multiply: " << multiply_opts->x << " * " << multiply_opts->y
            << " = " << (multiply_opts->x * multiply_opts->y) << std::endl;
    // print extra args if any
    if (!multiply_cmd->remaining().empty()) {
      std::cout << "Extra args: " << std::endl;
      for (const auto &extra : multiply_cmd->remaining()) {
        std::cout << "\t" << extra << std::endl;
      }
      std::cout << std::endl;
    }
}
