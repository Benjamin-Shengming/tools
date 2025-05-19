#!/usr/bin/env python3

from itertools import product
import sys


def is_palindrome(s):
    return s == s[::-1]


def find_sub_palindromes(palindrome):
    sub_palindromes = []
    n = len(palindrome)

    for i in range(n):
        for j in range(i + 2, n + 1):
            substring = palindrome[i:j]
            if is_palindrome(substring):
                sub_palindromes.append(substring)

    return sub_palindromes


def generate_all_palindromes(length):
    assert length > 0, "Length must be greater than 0"

    half_length = (length + 1) // 2
    half_palindromes = ["".join(p) for p in product("ab", repeat=half_length)]
    palindromes = []
    for half in half_palindromes:
        if length % 2 == 0:
            palindromes.append(half + half[::-1])
        else:
            palindromes.append(half + half[-2::-1])
    return palindromes


if __name__ == "__main__":
    p = "aaabbbbbbbaaa"
    sub_palindromes = find_sub_palindromes(p)
    print(f"{p} Sub-palindromes: {sub_palindromes}")
    print(f"{p} Sub-palindromes: {len(sub_palindromes)}")
    sys.exit(0)

    for i in range(10, 20):
        palindromes = generate_all_palindromes(i)
        for p in palindromes:
            assert is_palindrome(p), "not a palindrome"
            sub_palindromes = find_sub_palindromes(p)
            sub_count = len(sub_palindromes)
            print(f"{p} Sub-palindromes: {sub_count}")
            if sub_count == 30:
                print(f"Found 30 sub-palindromes for {p}")
                sys.exit(0)
