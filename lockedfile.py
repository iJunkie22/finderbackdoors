import os
import os.path
import stat


def binflagget(int1, rpad, flag_len=1):
    return (int1 >> rpad) % (1 << rpad + flag_len)


def flagnpadlen(int1, exp_bit_len=None, *flag_lens):
    work_bit_len = exp_bit_len
    if exp_bit_len is None:
        work_bit_len = int1.bit_length()

    flag_sum = sum(flag_lens)
    elbow_room = work_bit_len - flag_sum
    return flag_sum, elbow_room


def testflag(sample1, target1, flag_len=1):
    flag_l, pad_l = flagnpadlen(target1, None, 1)
    return binflagget(sample1, pad_l, flag_l)


def hasrpad(int1, exp_bit_len=None, *flag_lens):
    if exp_bit_len is None:
        exp_bit_len = int1.bit_length()

    elbow_room = exp_bit_len - sum(flag_lens)

    if elbow_room <= 0:
        return False

    return int1 == ((int1 >> elbow_room) << elbow_room)


def bin_check(sample1, target1):
    print target1
    return bool(sample1 % (target1 * 2) // target1)


def is_file_locked(fp1):
    return os.stat(fp1).st_flags & stat.UF_IMMUTABLE


if __name__ == '__main__':
    print('hey')
    print(hasrpad(0b0110, 4, 1, 1, 1))
    print(bin(~0b0110))
    print(binflagget(0b010010, 1))
    print(binflagget(0b010010, 1, 4))
