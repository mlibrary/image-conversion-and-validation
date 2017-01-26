# Copyright (c) 2017 The Regents of the University of Michigan.
# All Rights Reserved. Licensed according to the terms of the Revised
# BSD License. See LICENSE.txt for details.

def is_luhn_checkable (number):
    return bool(number) and isinstance(number, (str, int))

def rotate_digit (digit):
    result = digit * 2
    return result if result < 10 else result - 9

def add_two_digits (two_digits):
    first_digit = two_digits // 10
    second_digit = two_digits % 10

    return first_digit + rotate_digit(second_digit)

def get_check_digit_from_checkable_int (number):
    total = 0

    while number > 0:
        total += add_two_digits(number % 100)
        number //= 100

    return (9 * total) % 10

def get_check_digit (number = None):
    if is_luhn_checkable(number):
        try:
            return get_check_digit_from_checkable_int(int(number))

        except ValueError:
            return None

    else:
        return None