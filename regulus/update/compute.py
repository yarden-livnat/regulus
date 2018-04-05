import re
from regulus.file import get, save
from regulus.morse.morse import morse
from regulus.math.process import process


def decode2(param):
    keys = list(re.split(r'-', param))  # .remove('')
    keys.remove('')
    for i in range(len(keys)):
        keys[i] = '-' + keys[i]

    return keys


def update_params(reg, spec):
    reg.name = spec["name"]
    reg.version = spec["new_version"]

    keys = list(re.split(r'-', spec['params']))  # .remove('')
    keys.remove('')

    newparam = {}

    i = 0
    while (i + 1 < len(keys)):
        newparam[keys[i]] = keys[i + 1]
        i = i + 2

    return newparam


def compute(spec, data_dir):
    regulus = get(spec=spec, dir=data_dir)
    param = update_params(regulus, spec)

    morse(regulus, args=param)

    process(regulus)

    save(regulus)

    print("New Structure is available")

    return 1


if __name__ == '__main__':
    pass
