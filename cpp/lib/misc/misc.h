#pragma once

#include "log.h"
#include "sha256.h"
#include <algorithm>
#include <ctime>
#include <stdexcept>
#include <string>
#include <sys/types.h>
#include <vector>
#include <chrono>

using namespace std;
using std::chrono::duration_cast;
using std::chrono::milliseconds;
using std::chrono::seconds;
using std::chrono::system_clock;

extern string         hexlify(const string &input);
extern vector<char>   hexlify(const vector<char> &input);
extern string         unhexlify(const string &input);
extern time_t         iso8601_str_to_time(const string &tm_str);
extern string         iso8601_time_to_str(const time_t t);
extern string         ltrim(string str, const string chars = "\t\n\v\f\r ");
extern string         rtrim(string str, const string chars = "\t\n\v\f\r ");
extern string         trim(string str, const string chars = "\t\n\v\f\r ");
extern string         trim_space(string str);
extern vector<string> tokenize(const string &str, const char delim = '\n');
extern string vec_str_to_str(const vector<string> &v, const string &sep = ":");

inline bool ends_with(const string &str, const string &suffix)
{
    return str.size() >= suffix.size() &&
           0 == str.compare(str.size() - suffix.size(), suffix.size(), suffix);
}

inline bool starts_with(const string &str, const string &prefix)
{
    return str.size() >= prefix.size() &&
           0 == str.compare(0, prefix.size(), prefix);
}

inline void erase_substr(string &mainStr, const string &toErase)
{
    // Search for the substring in string
    size_t pos = mainStr.find(toErase);
    if (pos != string::npos)
    {
        // If found then erase it from string
        mainStr.erase(pos, toErase.length());
    }
}

inline bool is_grp_in_grps(const string &grp, const vector<string> &grps)
{
    return find(grps.begin(), grps.end(), grp) != grps.end();
}

extern string escape(const string &s,
                     char          escape_char    = '\'',
                     const string &escape_replace = "\\\'");

extern void assert_runtime(bool condition, const string &msg = "unknown error");

#define ASSERT_PTR(p)                                                          \
    do                                                                         \
    {                                                                          \
        if (p == nullptr)                                                      \
        {                                                                      \
            DPM_LOG_CRITICAL("Expect valid ptr but nullptr detected!");        \
            assert_runtime(p != nullptr, "nullptr detected!");                 \
        }                                                                      \
    } while (0)

#define ASSERT_NULL_PTR(p)                                                     \
    do                                                                         \
    {                                                                          \
        if (p != nullptr)                                                      \
        {                                                                      \
            DPM_LOG_CRITICAL("Expect nullptr but NOT nullptr detected!");      \
            assert_runtime(p == nullptr, "NOT nullptr detected!");             \
        }                                                                      \
    } while (0)

#define ASSERT_TRUE(v)                                                         \
    do                                                                         \
    {                                                                          \
        if (!(v))                                                              \
        {                                                                      \
            DPM_LOG_CRITICAL("Expect true but false detected!");               \
            assert_runtime(v, "False detected!");                              \
        }                                                                      \
    } while (0)

#define ASSERT_FALSE(v)                                                        \
    do                                                                         \
    {                                                                          \
        if (v)                                                                 \
        {                                                                      \
            DPM_LOG_CRITICAL("Expect false but true detected!");               \
            assert_runtime(!v, "True detected!");                              \
        }                                                                      \
    } while (0)

#define ASSERT_0(v)                                                            \
    do                                                                         \
    {                                                                          \
        if (v != 0)                                                            \
        {                                                                      \
            DPM_LOG_CRITICAL("Expect 0 but {} detected!", v);                  \
            assert_runtime(v == 0, "Non Zero detected!");                      \
        }                                                                      \
    } while (0)

#define ASSERT_NOT_0(v)                                                        \
    do                                                                         \
    {                                                                          \
        if (v == 0)                                                            \
        {                                                                      \
            DPM_LOG_CRITICAL("Expect NOT 0 but 0 detected!");                  \
            assert_runtime(v != 0, "Zero detected!");                          \
        }                                                                      \
    } while (0)

template <typename T, typename F>
shared_ptr<T> register_free(T *p, F f)
{
    shared_ptr<T> share_holder(p, f);
    return share_holder;
}

class StackTracer
{
  public:
    StackTracer();
};

template <typename T>
T sha256(const T &in)
{
    SHA256 sha256;
    sha256.add(in.data(), in.size());
    vector<unsigned char> buffer(SHA256::HashBytes, '\0');
    sha256.getHash(buffer.data());
    return T(buffer.begin(), buffer.end());
}

extern bool is_future(int64_t t);

template <typename T>
T milli_sec_to_sec(T in)
{
    return in / 1000;
}

template <typename T>
T sec_to_milli_sec(T in)
{
    return in * 1000;
}

template <typename T>
constexpr const T &clamp(const T &v, const T &lo, const T &hi)
{
    return (v < lo) ? lo : (hi < v) ? hi : v;
}

extern vector<string> get_local_ips();


template<typename T>
bool same_elements(const std::vector<T>& l, const std::vector<T>& r)
{
    if (l.size() != r.size()) 
    {
        return false;
    }
    if (l.size() <= 0) 
    {
        return true;
    }
    return std::is_permutation(l.begin(), l.end(), r.begin());
}


inline int64_t millisec_since_epoch()
{
    return duration_cast<milliseconds>(system_clock::now().time_since_epoch()).count();
}

inline int64_t sec_since_epoch()
{
    return duration_cast<seconds>(system_clock::now().time_since_epoch()).count();
}


/*run some function F until it returns
* all expections from F will be catched under max_tries
*/
template<typename F>
auto retry(F f, const std::string func_name, uint sleep_interval=5, size_t max_tries=1000)
{
    while(max_tries > 1)
    {
        try 
        {
            return f();
        }
        catch (...)
        {
            max_tries--;
            DPM_LOG_CRITICAL("Function {} failed, will have another try after {} seconds.", func_name, sleep_interval );
            sleep(sleep_interval);
        }
    }
    return f(); // last call which could throw anything from f 
}

#define QUOTE_F(f) "\"" #f "\"" 

#define RETRY(f) retry(f, QUOTE_F(f))

