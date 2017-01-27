# Copyright (c) 2017 The Regents of the University of Michigan.
# All Rights Reserved. Licensed according to the terms of the Revised
# BSD License. See LICENSE.txt for details.

from .luhn_number import LuhnNumber

def get_check_digit (number = None):
    n = LuhnNumber(number)
    return n.get_check_digit()

def verify_check_digit (number = None):
    n = LuhnNumber(number)
    return n.has_valid_check_digit()
