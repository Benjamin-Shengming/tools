#include "json_demo.h"
#include <nlohmann/json.hpp>
#include <iostream>

JsonDemoCmdApp::JsonDemoCmdApp() : CLI::App("Show nlohmann/json usage demo", "json-demo") {
    this->callback([this]() { this->run(); });
}

void JsonDemoCmdApp::run() {
    nlohmann::json j;
    j["name"] = "CLI11 JSON Demo";
    j["version"] = 1.0;
    j["features"] = {"parsing", "serialization", "pretty print"};
    std::cout << "Demo JSON output:\n" << j.dump(4) << std::endl;
}
