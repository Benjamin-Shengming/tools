#pragma once

#include <string>
#include <iostream>
#include <sstream>
#include <iomanip>
#include <thread>
#include <vector>
#include <map>
#include <algorithm>
#include <sstream>

#include "log.h"

#ifdef ENABLE_PROFILE
    #define START_PROFILE(x) (Profiler::get().start((x)))
    #define STOP_PROFILE(x) (Profiler::get().stop((x)))
    #define REPORT_ALL_PROFILE() (Profiler::get().report())
    #define START_FUNC_PROFILE()   ScopeProfiler profile##__func__(__func__)
    #define CURRENT_TICK()  (Profiler::get().tick_micro())
#else
    #define START_PROFILE(x)
    #define STOP_PROFILE(x)
    #define REPORT_ALL_PROFILE()
    #define START_FUNC_PROFILE()
    #define CURRENT_TICK()
#endif


class Profiler {
public:
    inline static Profiler& get() {
        static std::map<std::thread::id, Profiler> instances;

        auto id = std::this_thread::get_id();
        if (instances.find(id) == instances.end()) {
            instances.emplace(id, Profiler());
        }

        return instances.at(id);
    }

    inline void start(std::string s) {
        started[s] = tick_micro();
    }


    inline void stop(std::string s) {
        calls[s] += 1;
        total[s] += tick_micro() - started[s];
        average[s] = total[s] / calls[s];
    }


    inline void report(const std::string& s, ostringstream& out) {
        unsigned int max = 30;
        for (auto const &i : total) {
            if (i.first.length() > max) {
                max = i.first.length() + 2;
            }
        }
        out.width(max);
        out << std::left << s;

        out << "calls: ";
        out.width(3);
        out << std::right << calls[s] << "  ";

        out << "total: ";
        out.width(7);

        out << std::right << std::to_string(total[s] / 1000) + "ms" << "  / ";

        out << "average: ";
        out.width(12);
        out << std::right << std::to_string(average[s]) + "µs";

        out << std::endl;
    }

    inline std::string report() {
        std::vector<std::pair<std::string, uint32_t>> times;
        for (auto const &i : total) {
            times.push_back(i);
        }
        std::sort(times.begin(), times.end(),
            [](std::pair<std::string, uint32_t> p, std::pair<std::string, uint32_t> p2)
                    { return p.second > p2.second; });

        ostringstream out;

        out << std::endl;

        auto id = std::this_thread::get_id();
        out << id << std::endl;
        for (auto const &i : times) {
            report(i.first, out);
        }
        out << std::endl;
        return out.str();
    }

    inline static uint32_t tick_micro() {
        struct timespec timespec_time;

        clock_gettime(CLOCK_MONOTONIC, &timespec_time);

        uint32_t tick = timespec_time.tv_nsec / 1000;
        tick += timespec_time.tv_sec * 1000000;
        return tick;
    }
private:
    Profiler() {};
    std::map<std::string, uint32_t> started;
    std::map<std::string, uint32_t> calls;
    std::map<std::string, uint32_t> total;
    std::map<std::string, uint32_t> average;
};


class ScopeProfiler
{
public:
    ScopeProfiler(const std::string& name) {
        DPM_LOG_DEBUG("start scope {}, {}", name, Profiler::tick_micro());
        this->name = name;
        START_PROFILE(name);
    }
    ~ScopeProfiler() {
        STOP_PROFILE(name);
        DPM_LOG_DEBUG("stop scope {}, {}", name, Profiler::tick_micro());
    }
private:
    std::string name;

};
