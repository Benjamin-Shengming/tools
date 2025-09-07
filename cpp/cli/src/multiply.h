
#pragma once
#include "CLI11.hpp"
#include <memory>
#include "common.h"

class MultiplyCmdApp : public SubCmdApp {
public:
	MultiplyCmdApp();
	virtual void run() override;
	void add_options();
protected:
	int x;
	int y;
};
