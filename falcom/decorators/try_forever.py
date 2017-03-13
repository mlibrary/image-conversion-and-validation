# Copyright (c) 2017 The Regents of the University of Michigan.
# All Rights Reserved. Licensed according to the terms of the Revised
# BSD License. See LICENSE.txt for details.

class TryForever:

    def __call__ (self): pass

    def __repr__ (self):
        return "<{}>".format(self.__class__.__name__)

def try_forever (func):
    return func
