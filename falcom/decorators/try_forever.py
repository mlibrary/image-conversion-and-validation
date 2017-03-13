# Copyright (c) 2017 The Regents of the University of Michigan.
# All Rights Reserved. Licensed according to the terms of the Revised
# BSD License. See LICENSE.txt for details.

class TryForever:

    def __init__ (self):
        self.seconds_between_attempts = 60

    def __call__ (self, func):
        return func

    def __repr__ (self):
        return "<{}>".format(self.__class__.__name__)

def try_forever (func):
    return func
