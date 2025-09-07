#pragma once
#include "CLI11.hpp"
#include <memory>


#include "common.h"


class AddCmdApp : public SubCmdApp {
public:
	AddCmdApp();
	virtual void run() override;
	void add_options();
protected:
	int a;
	int b;
};

