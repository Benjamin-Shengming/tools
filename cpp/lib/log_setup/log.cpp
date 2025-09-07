#include "log.h"

#include "spdlog/spdlog.h"
#include "spdlog/sinks/stdout_color_sinks.h"
#include "spdlog/sinks/syslog_sink.h"

void setup_log(int log_verbosity, const std::string& name)
{
    // syslog always has full details
    auto syslog_sink = std::make_shared<spdlog::sinks::syslog_sink_mt>(name, 0, LOG_USER, false);
    syslog_sink->set_level(spdlog::level::trace);

    // console log can be controller by user via command line
    auto lvl = static_cast<spdlog::level::level_enum>(log_verbosity);
    auto console_sink = std::make_shared<spdlog::sinks::stdout_color_sink_mt>();
    console_sink->set_level(lvl);
    spdlog::sinks_init_list sink_list = { syslog_sink, console_sink };
    spdlog::set_default_logger(std::make_shared<spdlog::logger>(name, sink_list));
    spdlog::set_level(spdlog::level::trace);
}