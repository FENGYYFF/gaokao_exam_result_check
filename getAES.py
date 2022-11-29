from fontTools.misc.py23 import unichr


def fromCharCode(a, *b):
    return unichr(a % 65536) + ''.join([unichr(i % 65536) for i in b])


def getAES(value):
    str = ""
    count = 65
    tag = 90
    falg = 2
    for i in range(len(value)):
        str = str + fromCharCode(falg + i * 3 * 5) + fromCharCode(falg + i * 4 * 5) + fromCharCode(
            falg + i * 5 * 5) + fromCharCode(count - i) + value[i] + fromCharCode(tag + i) + fromCharCode(
            falg + i * 6 * 5) + fromCharCode(falg + i * 7 * 5) + fromCharCode(falg + i * 8 * 5)
        count = count + 1
        tag = tag + 1
    return str


if __name__ == '__main__':
    print(getAES("Xh13579."))
