import hashlib


def md5(source):
    m = hashlib.md5()
    m.update(source)
    return m.hexdigest()


def md5sum(path):
    with open(path, 'rb') as f:
        return md5(f.read())
