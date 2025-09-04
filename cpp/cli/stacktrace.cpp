#include "stacktrace.h"
#include <execinfo.h>
#include <unistd.h>
#include <cstdio>
#include <cstdlib>

namespace {
    void print_stacktrace() {
        void *array[50];
        int size = backtrace(array, 50);
        fprintf(stderr, "\nCaught signal, printing stack trace (most recent call last):\n");
        backtrace_symbols_fd(array, size, STDERR_FILENO);
    }

    void signal_handler(int sig) {
        print_stacktrace();
        std::_Exit(128 + sig); // Exit with signal code
    }
}

namespace stacktrace {
    void install_signal_handlers() {
        std::signal(SIGSEGV, signal_handler);
        std::signal(SIGABRT, signal_handler);
        std::signal(SIGFPE,  signal_handler);
        std::signal(SIGILL,  signal_handler);
        std::signal(SIGBUS,  signal_handler);
    }
}
