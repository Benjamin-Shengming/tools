// Prints verbose/config info for a subcommand, using options from the app
#pragma once
#include "CLI11.hpp"
#include <string>

class PrecallableApp : public CLI::App
{
public:
	using CLI::App::App;             // Inherit constructors
	virtual void pre_callback() = 0; // pure virtual function enforce implementation in derived classes
};

class MainApp : public PrecallableApp
{
public:
	using PrecallableApp::PrecallableApp; // Inherit constructors
	virtual void pre_callback() override
	{
	}
};

class SubCmdApp : public PrecallableApp
{
public:
	using PrecallableApp::PrecallableApp; // Inherit constructors
	virtual void add_common_options();
	virtual void pre_callback() override;

	// sub command main logic
	virtual void run() = 0; // pure virtual function enforce implementation in derived classes
protected:
	bool verbose{false};
	std::string config_file{""};
};
