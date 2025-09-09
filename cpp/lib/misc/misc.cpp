
#include <string>
#include <vector>

#include "log.h"
#include "misc.h"
#include <arpa/inet.h>
#include <chrono>
#include <cstdint>
#include <ctime>
#include <cxxabi.h>
#include <errno.h>
#include <execinfo.h>
#include <ifaddrs.h>
#include <iomanip>
#include <iostream>
#include <linux/if_link.h>
#include <netdb.h>
#include <signal.h>
#include <sstream>
#include <stdio.h>
#include <stdlib.h>
#include <sys/socket.h>
#include <unistd.h>
using namespace std;

string hexlify(const string &input)
{
    const static string HexCodes = "0123456789ABCDEF";
    string              HexString;
    for (size_t i = 0; i < input.length(); ++i)
    {
        unsigned char BinValue = input[i];
        // High half
        HexString += HexCodes[(BinValue >> 4) & 0x0F];
        HexString += HexCodes[BinValue & 0x0F];
    }
    return HexString;
}

vector<char> hexlify(const vector<char> &input)
{
    string in  = string(input.begin(), input.end());
    auto   ret = hexlify(in);
    return vector<char>(ret.begin(), ret.end());
}

string unhexlify(const string &input)
{
    const static string HexCodes = "0123456789ABCDEF";
    string              BinString;
    for (size_t i = 0; i < input.length() - 1; i += 2)
    {
        BinString +=
            (input[i] >= 'A' ? input[i] - 'A' + 10 : input[i] - '0') * 16 +
            (input[i + 1] >= 'A' ? input[i + 1] - 'A' + 10
                                 : input[i + 1] - '0');
    }
    return BinString;
}

string iso8601_time_to_str(const time_t t)
{
    time_t timeSinceEpoch = t / 1000;
    tm     st             = {};
    gmtime_r(&timeSinceEpoch, &st);
    string ret("2020-04-09T00:57:00");
    strftime((char *)ret.data(), ret.size(), "%FT%T", &st);
    return ret;
}

time_t iso8601_str_to_time(const string tm_str)
{

    //"2020-04-09T00:57:00+00:00"
    int  y, M, d, h, m, s, offset_h, offset_m;
    char c;
    if (tm_str == "")
        return time_t(9223372036854775807);
    sscanf(tm_str.c_str(),
           "%d-%d-%dT%d:%d:%d%c%d:%d",
           &y,
           &M,
           &d,
           &h,
           &m,
           &s,
           &c,
           &offset_h,
           &offset_m);
    DPM_LOG_DEBUG("time value:  {} {} {} {} {} {}", y, M, d, h, m, s);
    DPM_LOG_DEBUG("sign of time: {}", c);
    tm t      = {};
    t.tm_year = y - 1900;
    t.tm_mon  = M - 1;
    t.tm_mday = d;
    t.tm_hour = h;
    t.tm_min  = m;
    t.tm_sec  = s;

    time_t timeSinceEpoch = mktime(&t);
    DPM_LOG_DEBUG("Epoch time is : {}", timeSinceEpoch);
    return timeSinceEpoch * 1000;
}

string ltrim(string str, const string chars)
{
    str.erase(0, str.find_first_not_of(chars));
    return str;
}

string rtrim(string str, const string chars)
{
    str.erase(str.find_last_not_of(chars) + 1);
    return str;
}

string trim(string str, const string chars)
{
    return ::ltrim(::rtrim(str, chars), chars);
}

string trim_space(string str)
{
    return ::trim(str, " ");
}

vector<string> tokenize(const string &str, const char delim)
{
    vector<string> out;
    size_t         start = 0;
    size_t         end   = 0;
    while ((start = str.find_first_not_of(delim, end)) != string::npos)
    {
        end = str.find(delim, start);
        out.push_back(str.substr(start, end - start));
    }
    return out;
}

string vec_str_to_str(const vector<string> &v, const string &sep)
{
    string s;
    for (const auto &piece : v)
    {
        if (!s.empty())
            s += sep + piece;
        else
            s = piece;
    }
    return s;
}

string escape(const string &s, char escape_char, const string &escape_replace)
{
    size_t n = s.length();
    string escaped;
    escaped.reserve(n * 2); // pessimistic preallocation

    for (size_t i = 0; i < n; ++i)
    {
        if (s[i] == escape_char)
            escaped += escape_replace;
        else
            escaped += s[i];
    }
    return escaped;
}

void assert_runtime(bool condition, const string &msg)
{
    if (condition)
        return;
    DPM_LOG_CRITICAL("Run time error {}", msg);
    throw runtime_error(msg);
}

static void printStackTrace(FILE *out = stderr, unsigned int max_frames = 63)
{
    DPM_LOG_CRITICAL("stack trace:");

    // storage array for stack trace address data
    void *addrlist[max_frames + 1];

    // retrieve current stack addresses
    uint32_t addrlen = backtrace(addrlist, sizeof(addrlist) / sizeof(void *));

    if (addrlen == 0)
    {
        DPM_LOG_CRITICAL("  \n");
        return;
    }

    // create readable strings to each frame.
    char **symbollist = backtrace_symbols(addrlist, addrlen);

    // print the stack trace.
    for (uint32_t i = 4; i < addrlen; i++)
        DPM_LOG_CRITICAL("{}\n", symbollist[i]);

    free(symbollist);
}

void abortHandler(int signum, siginfo_t *, void *)
{
    // associate each signal with a signal name string.
    const char *name = NULL;
    switch (signum)
    {
    case SIGABRT:
        name = "SIGABRT";
        break;
    case SIGSEGV:
        name = "SIGSEGV";
        break;
    case SIGBUS:
        name = "SIGBUS";
        break;
    case SIGILL:
        name = "SIGILL";
        break;
    case SIGFPE:
        name = "SIGFPE";
        break;
    case SIGTERM:
        name = "SIGTERM";
        break;
    case SIGKILL:
        name = "SIGKILL";
        break;
    case SIGHUP:
        name = "SIGHUP";
        break;
    }

    // Notify the user which signal was caught.
    if (name)
        DPM_LOG_CRITICAL("Caught signal {} ({})", signum, name);
    else
        DPM_LOG_CRITICAL("Caught signal {}", signum);

    // Dump a stack trace.
    printStackTrace();

    // If you caught one of the above signals, quit child worker thread
    exit(signum);
}

StackTracer::StackTracer()
{
    struct sigaction sa;
    sa.sa_flags     = SA_SIGINFO;
    sa.sa_sigaction = abortHandler;
    sigemptyset(&sa.sa_mask);

    sigaction(SIGABRT, &sa, NULL);
    sigaction(SIGSEGV, &sa, NULL);
    sigaction(SIGBUS, &sa, NULL);
    sigaction(SIGILL, &sa, NULL);
    sigaction(SIGFPE, &sa, NULL);
    sigaction(SIGPIPE, &sa, NULL);
    sigaction(SIGTERM, &sa, NULL);
    sigaction(SIGKILL, &sa, NULL);
    sigaction(SIGHUP, &sa, NULL);
}

int64_t current_milli_sec()
{
    return time(NULL) * 1000;
}

bool is_future(int64_t t)
{
    return t > current_milli_sec();
}

vector<string> get_local_ips()
{
    struct ifaddrs *ifaddr;
    vector<string>  ret;
    if (getifaddrs(&ifaddr) == -1)
    {
        return ret;
    }
    auto ifaddr_deleter = register_free(ifaddr, freeifaddrs);
    /* Walk through linked list, maintaining head pointer so we
       can free list later */

    for (struct ifaddrs *ifa = ifaddr; ifa != NULL; ifa = ifa->ifa_next)
    {
        if (ifa->ifa_addr == NULL)
            continue;
        int family = ifa->ifa_addr->sa_family;

        /* AF_INET/AF_INET6* interface address*/
        if (family == AF_INET || family == AF_INET6)
        {
            char          host[NI_MAXHOST];
            int           s = getnameinfo(ifa->ifa_addr,
                                family== AF_INET?sizeof(struct sockaddr_in):sizeof(struct sockaddr_in6),
                                host,
                                NI_MAXHOST,
                                NULL,
                                0,
                                NI_NUMERICHOST);
            if (s != 0)
            {
                DPM_LOG_CRITICAL("getnameinfo() failed: {}", gai_strerror(s));
                break;
            }
            ret.push_back(string(host));
        }
    }
    return ret;
}
