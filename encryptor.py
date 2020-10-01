# encryptor.py

from filters import ip, pc1, pc2, p, e_bit, ip_minus_1, s_boxes


def do_permutation(str_, filter_):
    """
    The function applies permutation to a given binary string
    :param str_: (str) binary string to alter
    :param filter_: (list of int) permutation filter
    :return: (str) altered binary string
    """
    return "".join([str_[i - 1] for i in filter_])


def left_circular_shift(str_):
    return str_[1:] + str_[0]


def halve(str_):
    return str_[:len(str_) // 2], str_[len(str_) // 2:]


def xor(str_1, str_2):
    str_1 = [int(item) for item in str_1]
    str_2 = [int(item) for item in str_2]

    # implementing xor formula
    result = [(bit_1 and not bit_2) or (not bit_1 and bit_2) for bit_1, bit_2 in zip(str_1, str_2)]

    result = "".join([str(int(item)) for item in result])
    return result


def transform(str_, row_len):
    """
    The function splits one-line string into a list of strings
    :param str_: given one-line string
    :param row_len: width of the new matrix
    :return: (list of strings)
    """
    matrix = []
    temp = ""
    for index, item in enumerate(str_):
        temp += item
        if index != 0 and (index + 1) % row_len == 0:
            matrix.append(temp)
            temp = ""
    return matrix


def s_boxing(*args):
    """
    Transforms 6bit rows into 4bit rows
    :param args: (list of strings) rows
    :return: (str)
    """
    values = []
    for s_box_num, arg in enumerate(args):
        row = arg[0] + arg[-1]
        row = int(row, 2)

        column = arg[1:-1]
        column = int(column, 2)

        values.append(s_boxes[s_box_num][row][column])

    return "".join([f"{value:04b}" for value in values])


def do_round(l_in_, r_in_, k_):
    # e-bit selection for r_in
    r_out = do_permutation(r_in_, e_bit)

    # xor R with sub key
    r_out = xor(r_out, k_)

    # 6bit rows to 4bit
    r_out = s_boxing(*(transform(r_out, 6)))

    # permutation
    r_out = do_permutation(r_out, p)

    # xor left and right
    r_out = xor(l_in_, r_out)
    return r_in_, r_out


def generate_keys(c, d):
    sub_keys_ = []
    for round_number in range(16):
        c, d = left_circular_shift(c), left_circular_shift(d)
        if round_number not in [0, 1, 8, 15]:
            c, d = left_circular_shift(c), left_circular_shift(d)
        sub_keys_.append(do_permutation(c + d, pc2))
    return sub_keys_


def binary_to_hex(*args):
    """
    :param args: (str)
    :return: (str)
    """
    return "".join([f"{int(arg, 2):x}" for arg in args])


def hex_to_binary(*args):
    """
    :param args: (str)
    :return: (str)
    """
    return "".join([f"{int(arg, 16):04b}" for arg in args])


def encrypt(message, key):
    # STEP 1
    # convert message to binary
    message = hex_to_binary(*message)
    # convert key to binary
    key = hex_to_binary(*key)

    # STEP 2
    # apply initial permutation to the message
    message = do_permutation(message, ip)

    # STEP 3
    # apply permuted choice 1 (PC-1) to the key
    key = do_permutation(key, pc1)
    c, d = halve(key)

    # STEP 4
    # generate 16 sub keys
    sub_keys = generate_keys(c, d)

    # STEP 5
    # encode each block of the data
    l_in, r_in = halve(message)
    for round_num in range(16):
        l_in, r_in = do_round(l_in, r_in, sub_keys[round_num])

    # STEP 6
    # apply final permutation
    result = do_permutation(r_in + l_in, ip_minus_1)

    result = transform(result, 4)
    result = binary_to_hex(*result)
    return result
