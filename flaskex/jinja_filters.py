from math import ceil


def dt1(dt):
    return dt.strftime('%Y-%m-%d %H:%M:%S')


def group(iterable, colunm_count):
    li = tuple(iterable)
    ret = list()
    for i in range(0, int(ceil(len(li) * 1. / colunm_count))):
        s = i * colunm_count
        e = s + colunm_count
        ret.append(li[s:e])
    return ret

filters = globals()
