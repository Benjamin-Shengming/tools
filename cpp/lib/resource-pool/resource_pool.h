#pragma once

#include "log.h"
#include <condition_variable>
#include <exception>
#include <iostream>
#include <pthread.h>
#include <sched.h>
#include <sstream>
#include <memory>
#include <mutex>
#include <queue>
#include <set>
#include <thread>
#include <unistd.h>


using namespace std;
#include "profiler.h"

using namespace std;
template <typename T, typename TPool>
class Resource
{
  public:
    Resource(std::shared_ptr<T> r_, TPool *p) : r{r_}, pool{p}, err{0} {};
    ~Resource()
    {
        pool->unborrow(r, err);
    };

    Resource(const Resource &) = delete;            // copy is not allowed
    Resource &operator=(const Resource &) = delete; // assign is not allowed

    bool is_healthy() const
    {
        return err == 0;
    }
    void mark_unhealthy(int err_code = 1)
    {
        START_FUNC_PROFILE();
        err = err_code;
    }
    // Use it but never free it
    T *get() const
    {
        return r.get();
    }
    // Reset a bad resource in case of interrupted DB connections
    void refresh()
    {
        pool->refresh(r);
        err = 0;
    }

  private:
    std::shared_ptr<T> r;    // the pointer to the real resource
    TPool *            pool; // pointer to resource pool
    int                err;  // 0 means resource is good, others mean error
};

template <typename T, typename TFactory>
class ResourcePool
{
  public:
    ResourcePool(std::shared_ptr<TFactory> factory,
                 size_t                    pool_size      = 200)
        : m_factory{factory}, m_capacity{pool_size} {};

    ~ResourcePool() = default;

    std::shared_ptr<Resource<T, ResourcePool>> borrow()
    {
        START_FUNC_PROFILE();
        std::unique_lock<std::mutex> lk(m_mutex);
        if (is_full() && m_idle.empty())
        {
            // Wait (temporarily block) until a resource is made available.
            m_cv.wait(lk);
        }
        
        shared_ptr<T> r;
        if (!m_idle.empty())
        {
            // A resource is available, move it from idle queue to busy queue.
            r = m_idle.front();
            m_idle.pop();
            m_busy.insert(r);
        }
        else if (!is_full())
        {
            // No resources available, but a new one can be created.
            r = std::shared_ptr<T>(create_resource());
            m_busy.insert(r);
        }

        DPM_LOG_DEBUG("idle: {}, busy: {}", size_idle(), size_busy());
        return make_shared<Resource<T, ResourcePool>>(r, this);
    }

    void unborrow(shared_ptr<T> &r, int err = 0)
    {
        START_FUNC_PROFILE();
        std::unique_lock<std::mutex> lk(m_mutex);
        if (err != 0) // if some error happened on the returned resource
        {
          m_busy.erase(r);
        }
        else
        {
            // Resource is healthy, put it back in idle queue.
            m_idle.push(r);
            m_busy.erase(r);
            lk.unlock();
            m_cv.notify_one();
        }
        DPM_LOG_DEBUG("idle: {}, busy: {}", size_idle(), size_busy());
    }

    void refresh(shared_ptr<T> &r)
    {
        START_FUNC_PROFILE();
        std::unique_lock<std::mutex> lk(m_mutex);
        /* Clear the resource from the pool . This is
         * needed so that the shared_ptr<T> "r" will be unique (with no other
         * pointers sharing ownership) when m_factory->refresh(r) is called.
         */
        m_busy.erase(r);
        // Refresh the resource and re-add it to the "busy" queue.
        m_factory->refresh(r);
        m_busy.insert(r);
    }

  private:
    // helper functions and should not protected by lock to avoid recursive lock
    bool is_full()
    {
        return m_idle.size() + m_busy.size() >= m_capacity;
    }
    std::shared_ptr<T> create_resource()
    {
        START_FUNC_PROFILE();
        return m_factory->create();
    }
    int size_idle()
    {
        return m_idle.size();
    }
    int size_busy()
    {
        return m_busy.size();
    }
    // members
    std::shared_ptr<TFactory> m_factory; // factory is used to create a resource
    size_t m_capacity;                   // max number of elements in the pool
    std::queue<std::shared_ptr<T>> m_idle; // available resources
    std::set<std::shared_ptr<T>>   m_busy; // borrowed resources

    // multi-thread control
    std::mutex              m_mutex;
    std::condition_variable m_cv;
};
