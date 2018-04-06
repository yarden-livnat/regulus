keymap = {
    'k': 'knn',
    'G': 'graph',
    'g': 'gradient',
    'n': 'norm',
    'b': 'beta'
}


def update_params(reg, spec):
    import re

    reg["name"] = spec["name"]
    reg["version"] = spec["new_version"]

    keys = list(re.split(r'-', spec['params']))  # .remove('')
    keys.remove('')
    newparam = {}

    for key in keys:
        if key[0] in keymap.keys():
            newparam[keymap[key[0]]] = change_type(key[1:].strip(), key[0])

    return newparam


def change_type(val, key):
    if key == 'k':
        return int(val)
    elif key == 'b':
        return float(val)
    else:
        return val


def update_topo(spec, data_dir):
    from regulus.file import get, save
    from regulus.morse.morse import morse
    from regulus.math.process import process

    regulus = get(spec=spec, dir=data_dir)
    param = update_params(regulus, spec)

    morse(regulus, args=param)

    process(regulus)

    save(regulus)

    print("New Structure is available")

    return 1


if __name__ == '__main__':
    pass
