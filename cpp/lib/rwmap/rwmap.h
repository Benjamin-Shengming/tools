#pragma once

#include "rwlock.h" 
#include <map>

/*
 * Thread-safe read-write map protected by read-write lock
 */
template<typename K, typename V>
class RWMap
{
  public:
    bool get(const K& k, V& v) // read
    {
        // apply read lock 
        AutoRWLocker auto_lck(rwlock, true);

        // read data from map
        auto it = m.find(k);
        if (it == m.end()) 
        {
            return false;
        }
        v = it->second;
        return true;
    }

    bool put(const K& k, V& v)  // insert or update
    {
        // read firstly to check whether need to change  
        // trying avoid write lock 
        {
            // apply read lock 
            AutoRWLocker auto_lck(rwlock, true);
            // read data from map
            auto it = m.find(k);
            if (it != m.end() && (it->second == v))
            {
                // no need to update
                return true;
            }
        } // read lock is released here
        
        // apply write lock
        AutoRWLocker auto_lck(rwlock, false);
        // change data in map
        m[k] = v;
        return true;
    }

    void remove(const K& k) // remove 
    {
        // trying avoid write lock 
        {
            // apply read lock 
            AutoRWLocker auto_lck(rwlock, true);
            // read data from map
            auto it = m.find(k);
            if (it == m.end()) // coud not find key
            {
                // no need to remove 
                return;
            }
        } // read lock is released here

        // apply write lock
        AutoRWLocker auto_lck(rwlock, false);
        m.erase(k);
    }

    size_t size() // number of elements
    {
        // apply read lock 
        AutoRWLocker auto_lck(rwlock, true);
        // read data from map
        return m.size();
    }

  private:
    RWLock rwlock; // lock which can be locked by read or write
    std::map<K, V> m; // data need to protect
};



/*
 * Thread-safe read-write map-entry protected by read-write lock
 * has try functions
 */
template<typename K, typename V>
class RWMapWithEntryProtection
{
  public:
    bool get(const K& k, V& v) // read
    {
        // apply read lock on whole table
        AutoRWLocker auto_lck(rwlock, true);

        // read data from map
        auto it = m.find(k);
        if (it == m.end())  // does not exist in table
        {
            return false;
        }
        
        // does exist in table
        // apply read lock on the row before read

        AutoRWLocker auto_row_lck(std::get<1>(it->second));

        // read value  
        v = std::get<0>(it->second);
        return true;
    }

    // Update row value(wait until lock accquired) 
    bool update(const K& k, const V& v)   
    {
        // apply read lock 
        AutoRWLocker auto_lck(rwlock, true);
        // get row in map
        auto it = m.find(k);
        if (it == m.end())
        {
            // nothing to update
            return false;
        }
        // row does exist
        // Get row WRITE lock before udpate the value 
        AutoRWLocker auto_row_lck(std::get<1>(it->second), false);
        // change data in map
        std::get<0>(it->second) = v;
        return true;
    }

    bool try_create(const K& k, const V& v)  // insert 
    {
        // try to apply write lock 
        AutoRWTryLocker auto_lck(rwlock);
        if (!auto_lck.try_write()) // can't accquire WR lock
        {
            return false; // return without wait
        }
        m.emplace(std::make_pair(k, std::make_tuple(v, RWLock())));
       return true;
    }

    template<typename F>
    bool try_update(const K& k, V& v, F &&lambda)
    {
        // try to apply read lock  on whole table
        AutoRWTryLocker auto_lck(rwlock);
        if (!auto_lck.try_read()) // can't accquire WR lock
        {
            return false; // return withouit wait
        }
        // find entry from map
        auto it = m.find(k);
        if (it == m.end())
        {
            // does not exist
            return false;
        }
        // Get row WR lock before udpate the value 
        AutoRWTryLocker auto_row_lck(std::get<1>(it->second));
        if (!auto_row_lck.try_write())
        {
            // can't change the row 
            return false;
        }
      
        // now update value
        try 
        {
          v = lambda();
          std::get<0>(it->second) = v;
        }
        catch(...)// catch any errors
        {
           return false;
        }
        return true;
    }

    size_t size() // number of elements
    {
        // apply read lock 
        AutoRWLocker auto_lck(rwlock, true);
        // read data from map
        return m.size();
    }

  private:
    RWLock rwlock; //  protect whole map especially when you try to insert new entry
    std::map<K, std::tuple<V, RWLock>> m; // data need to protect
};

