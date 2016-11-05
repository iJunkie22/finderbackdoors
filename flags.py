from __future__ import unicode_literals, print_function


ONE_HEX_BIT = 0b1111
ONE_PYT_BYTE = 0b11111111

foo = type(ONE_HEX_BIT)


class BFlags(int):
    pass


print(foo)


