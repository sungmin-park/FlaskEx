import hashlib


def hashed(cls, source):
    h = cls()
    h.update(source)
    return h.hexdigest()


def md5(source):
    return hashed(hashlib.md5, source)


def md5sum(path):
    with open(path, 'rb') as f:
        return md5(f.read())


def sha256(source):
    return hashed(hashlib.sha256, source)
