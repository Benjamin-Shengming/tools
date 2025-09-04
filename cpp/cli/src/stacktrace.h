#pragma once
#include <csignal>

namespace stacktrace {
    // Install signal handlers for common crash signals
    void install_signal_handlers();
}
