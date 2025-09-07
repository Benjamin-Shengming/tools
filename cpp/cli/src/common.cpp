#include "common.h"
#include "log.h"

// Implementation for SubCmdApp methods

void SubCmdApp::add_common_options()
{
	this->add_flag("-v,--verbose", this->verbose, {"Enable verbose output"});
	this->add_option("--config", this->config_file, "Config file for this subcommand");
	this->allow_extras();
}

void SubCmdApp::pre_callback()
{
	std::string parent_name;
	if (this->get_parent()) {
		parent_name = this->get_parent()->get_name();
	} else {
		parent_name = "(no parent)";
	}
	std::string subcmd_name = this->get_name();
	std::string full_name = parent_name + ":" + subcmd_name;
	setup_log(this->verbose ? 1 : 3, full_name);
}
