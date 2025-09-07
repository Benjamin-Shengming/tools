
#include "multiply.h"
#include <iostream>
#include <spdlog/spdlog.h>

MultiplyCmdApp::MultiplyCmdApp() : SubCmdApp("Multiply two numbers", "multiply") {
  add_common_options();
  add_options();
}

void MultiplyCmdApp::run() {
  spdlog::info("Multiply command was called");
  try {
    int result = x * y;
    std::cout << "Result: " << result << std::endl;
  } catch (const std::exception &e) {
    spdlog::error("Error running multiply command: {}", e.what());
  }
}

void MultiplyCmdApp::add_options() {
  this->add_option("x", this->x, "First number")->required();
  this->add_option("y", this->y, "Second number")->required();
  this->allow_extras();
  this->fallthrough();
  this->callback([this]() { this->run(); });
}
