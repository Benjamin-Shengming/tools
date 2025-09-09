#pragma once

#include <pthread.h>

/*
 * A thin wrapper over pthread read-write lock
 * can be replaced by std c++'s lock if we have c++14 or over
 */
class RWLock
{
  public:
    // avoid writer starving by default
    RWLock(int pref=PTHREAD_RWLOCK_PREFER_WRITER_NONRECURSIVE_NP) 
    { 
      pthread_rwlockattr_init(&attr);
      pthread_rwlockattr_setkind_np(&attr, pref);
      pthread_rwlock_init(&rwlock, &attr);
    }
    ~RWLock() 
    { 
      pthread_rwlockattr_destroy(&attr);
      pthread_rwlock_destroy(&rwlock);
    }

    pthread_rwlock_t* get() { return &rwlock; } 

  private:
    pthread_rwlockattr_t attr;
    pthread_rwlock_t rwlock;
};

class AutoRWLocker
{
  public:
    AutoRWLocker(RWLock& lock, bool read_only=true):lck(lock) 
    { 
      if (read_only)
      {
          // apply read lock
          pthread_rwlock_rdlock(lck.get()); 
      }
      else 
      {
          // apply write lock
          pthread_rwlock_wrlock(lck.get());
      }
    }

    ~AutoRWLocker() 
    { 
        // unlock nomater it is read or write
        pthread_rwlock_unlock(lck.get()); 
    }

  protected: 
    RWLock& lck;
};


class AutoRWTryLocker
{
  public:
    AutoRWTryLocker(RWLock& lock):lck(lock) {  }
   
    bool try_read() 
    {
          // try read lock
          err_code = pthread_rwlock_tryrdlock(lck.get());
          return (err_code == 0);
    }

    bool try_write()
    {
          // try write lock
          err_code = pthread_rwlock_trywrlock(lck.get());
          return (err_code == 0);
    }

    void unlock()
    {

        // unlock nomater it is read or write if it is locked
        // behavior is undefined if unlock an unlocked lock
        if (err_code == 0) // no errors, lock sucessfully, need release
        {
            pthread_rwlock_unlock(lck.get()); 
        }
    }

    int get_lock_error()
    {
       return err_code;
    }

    ~AutoRWTryLocker() 
    { 
        unlock();
    }

  protected: 
    int err_code = 0;
    RWLock& lck;
};
