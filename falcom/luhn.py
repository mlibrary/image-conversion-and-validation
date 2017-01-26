# Copyright (c) 2017 The Regents of the University of Michigan.
# All Rights Reserved. Licensed according to the terms of the Revised
# BSD License. See LICENSE.txt for details.

def convert_into_luhn_checkable_int (number):
    if number:
        return int(number)

    else:
        return None

def rotate_digit (digit):
    if digit > 4:
        return (digit * 2) - 9

    else:
        return digit * 2

def get_check_digit (number = None):
    number = convert_into_luhn_checkable_int(number)

    if number is None:
        return None

    return (9 * ((number // 10) + rotate_digit(number % 10))) % 10
