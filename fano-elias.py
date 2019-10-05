import numpy as np

def calc_table(arr):
    q_probs = []
    cumul = 0
    for i in range(len(arr)):
        cumul += arr[i][1]
        q_probs.append(cumul)

    q_bar = []
    for i in range(len(arr)):
        q_bar.append(q_probs[i] - arr[i][1] / 2)

    lenghts = []
    for i in range(len(arr)):
        lenghts.append(int(np.ceil(np.log2(1 / arr[i][1]))) + 1)

    return q_probs, q_bar, lenghts

def encode(arr):
    _, q_bar, lenghts = calc_table(arr)

    codes = []
    for i in range(len(arr)):
        codes.append(float_bin(q_bar[i], lenghts[i]))

    return codes


def decode(arr, codes):
    q_prob, _, _ = calc_table(arr)
    decodes = []

    for code in codes:
        code_dec = mantissa_bin(code)
        i = 0
        while float(code_dec) >= q_prob[i]:
            i += 1
            if(i == len(q_prob)):
                break

        decodes.append((code, arr[i][0]))

    return decodes


def float_bin(number, places=3):
    dec = float(number)

    res = '.'

    for i in range(places):
        if(2**-(i+1) > dec):
            res += '0'
        else:
            res += '1'
            dec -= 2**-(i+1)

    return res

def mantissa_bin(fl_bin):
    res = 0
    i = 0
    for c in fl_bin:
        if not(c == '.'):
            if int(c) == 1:
                res += 2**-i
        i += 1

    return res


list1 = [('1', 0.25), ('2', 0.15), ('3', 0.1), ('4', 0.05), ('5', 0.45)]

cds = encode(list1)
print(cds)
cds.reverse()
print(decode(list1, cds))
