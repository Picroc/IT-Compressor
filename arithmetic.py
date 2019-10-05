import numpy as np

distr = {
    'A': 0.4,
    'B': 0.1,
    'C': 0.3,
    '\0': 0.2
}

alpha = ['A', 'B', 'C', '\0']


def min_bits(a):
    return -int(np.ceil(np.log2(a))) + 1


def float_bin(number, places=3):
    whole, dec = str(number).split(".")

    whole = int(whole)
    dec = int(dec)

    res = bin(whole).lstrip("0b") + "."

    for x in range(places):
        if dec == 0:
            res += '0'
            continue
        whole, dec = str((decimal_converter(dec)) * 2).split(".")

        dec = int(dec)

        res += whole

    return res


def decimal_converter(num):
    while num > 1:
        num /= 10
    return num


def mantissa_bin(fl_bin):
    res = 0.0
    i = 0
    for c in fl_bin:
        if not (c == '.'):
            if int(c) == 1:
                res += 2 ** -i
        i += 1

    return res * 0.1


def calc_table(alpha, base=0.0, length=1.0):
    q_probs = []
    cumul = base
    for i in range(len(alpha)):
        q_probs.append((cumul, distr[alpha[i]] * length))
        cumul += distr[alpha[i]] * length

    return q_probs


def which_letter(cumul, value):
    i = 0
    for el in cumul:
        if value < el[0] + el[1]:
            return alpha[i]
        i += 1

    return alpha[i]


def encode(arr):
    cumul = calc_table(alpha)
    curr = ()

    for char in arr:
        base, length = cumul[alpha.index(char)]
        curr = (char, cumul[alpha.index(char)])
        cumul = calc_table(alpha, base, length)

    return curr


def decode(value):
    string = ''
    curr = ''
    cumul = calc_table(alpha)

    while curr != '\0':
        curr = which_letter(cumul, value)
        string += curr
        base, length = cumul[alpha.index(curr)]
        cumul = calc_table(alpha, base, length)

    return string


list1 = 'AAABCACBABAB\0'

encoded = encode(list1)

en_dec = encoded[1][0]
bits = min_bits(encoded[1][0])
bin_num = float_bin(en_dec, 8)

print(encoded[0], en_dec)
print('Min bits', bits)
print(mantissa_bin(bin_num))
print('Encoded:', bin_num)

decoded = decode(mantissa_bin(bin_num))

print('Decoded:', decoded)
