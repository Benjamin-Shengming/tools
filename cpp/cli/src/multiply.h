#pragma once
#include "CLI11.hpp"
#include "add.h"

struct multiply_options;
std::shared_ptr<multiply_options> build_multiply_subcmd(CLI::App &app);


void run_multiply(CLI::App &app,
                  std::shared_ptr<multiply_options> multiply_opts);