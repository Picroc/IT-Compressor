def tobin_string(num):
    # dv, md = divmod(num, 128)
    # if dv < 128:
    #     return format(dv, '#09b')[2:] + format(md, '#09b')[2:]
    # else:
    #     return tobin_string(dv) + format(md, '#09b')[2:]
    result = []
    dv, md = divmod(num, 128)
    while dv >= 128:
        result.append(format(md, '#09b')[2:])
        dv, md = divmod(dv, 128)

    if not dv == 0:
        result.append(format(md, '#09b')[2:])
        result.append(format(dv, '#09b')[2:])
    else:
        result.append(format(md, '#09b')[2:])

    result.reverse()

    return result


def build_tree(string):
    D = []
    D_tree = []
    curr_string = bytes()

    for char in string:
        char = bytes([int(char)])
        if curr_string + char in D:
            curr_string += char
        else:
            if curr_string in D:
                idx = D.index(curr_string) + 1
            else:
                idx = 0
            D.append(curr_string + char)
            D_tree.append((idx, char))
            curr_string = bytes()

    if len(curr_string) > 0:
        idx = D.index(curr_string)
        D_tree.append(D_tree[idx])

    return D_tree


def encode(string):
    D_tree = build_tree(string)
    bin_string = []

    for node in D_tree:
        bin_node_arr = tobin_string(node[0])
        for element in bin_node_arr[:-1]:
            bin_string.append('0' + element)

        bin_string.append('1' + bin_node_arr[-1])
        bin_string.append(format(int.from_bytes(node[1], 'big'), '#010b')[2:])

    return bin_string, D_tree


def decode(string):
    result = []
    curr = ''
    sym = False
    for byte in string:
        buff = format(byte, '#010b')[2:]
        if sym:
            idx = result.pop()
            result.append((idx, str(byte)))
            sym = False
            continue
        if buff[0] == '1':
            curr += buff[1:]
            result.append(int(curr, 2))
            curr = ''
            sym = True
        else:
            curr += buff[1:]

    D = []
    # fin_string = []
    for node in result:
        if node[0] == 0:
            D.append(bytes([int(node[1])]))
        else:
            buff = D[node[0] - 1] + bytes([int(node[1])])
            D.append(buff)

    return D, result


f = open('maxresdefault.jpg', 'rb')
ba = bytearray(f.read())
# print([int(x[1], 8) for x in build_tree(ba)])
encoded, d_tree = encode(ba)
of = open('maxresdefaultEncoded.jpg', 'wb')
for byte in encoded:
    of.write(bytes([int(byte, 2)]))
of.close()

tf = open('maxresdefaultEncoded.jpg', 'rb')
ba2 = bytearray(tf.read())

ba2, dtree = decode(ba2)
df = open('maxresdefaultDecoded.jpg', 'wb')
df.write(b''.join(ba2))
df.close()