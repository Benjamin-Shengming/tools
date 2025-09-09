#pragma once
#include <stddef.h>
#include <cstring>
#include <sys/mman.h>

template <typename T>
struct non_swapple_allocator {
  using value_type = T;

  non_swapple_allocator() = default;
  template <class U>
  non_swapple_allocator(const non_swapple_allocator<U>&) {}

  T* allocate(std::size_t n) {
    auto ptr = mmap(NULL, n * sizeof(T), PROT_READ | PROT_WRITE, MAP_PRIVATE | MAP_ANONYMOUS | MAP_LOCKED, -1, 0);
    if (ptr == MAP_FAILED) 
    {
        throw std::bad_alloc();
    }
    return static_cast<T*>(ptr);
  }

  void deallocate(T* ptr, std::size_t n)  {
    memset(ptr, 0, n * sizeof(T));
    munmap(ptr, n * sizeof(T));
  }
};

template <typename T, typename U>
inline bool operator == (const non_swapple_allocator<T>&, const non_swapple_allocator<U>&) {
  return true;
}

template<typename T, typename U>
inline bool operator != (const non_swapple_allocator<T>& lhs, const non_swapple_allocator<U>& rhs) {
  return !(lhs == rhs);
}

