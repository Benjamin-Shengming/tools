
#include "add.h"
#include <iostream>
#include <spdlog/spdlog.h>

AddCmdApp::AddCmdApp() : SubCmdApp("Add two numbers", "add") {
  add_common_options();
  add_options();
}

void AddCmdApp::run() {
  spdlog::info("Add command was called");
  try {
    int result = a + b;
    std::cout << "Result: " << result << std::endl;
  } catch (const std::exception &e) {
    spdlog::error("Error running add command: {}", e.what());
  }
}

void AddCmdApp::add_options() {
  this->add_option("a", this->a, "First number")->required();
  this->add_option("b", this->b, "Second number")->required();
  this->allow_extras();
  this->fallthrough();
  this->callback([this]() { this->run(); });  
}