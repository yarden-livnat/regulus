keymap = {
    'k': {'name': 'knn', 'type': int},
    'G': {'name': 'graph', 'type': str},
    'g': {'name': 'gradient', 'type': str},
    'n': {'name': 'norm', 'type': str},
    'b': {'name': 'beta', 'type': float}
}


def update_params(reg, spec):
    # import re

    reg["name"] = spec["name"]
    reg["version"] = spec["new_version"]

    # keys = list(re.split(r'-', spec['params']))  # .remove('')
    # keys.remove('')
    # newparam = {}
    #
    # or key in keys:
    #    if key[0] in keymap.keys():
    #        newparam[keymap[key[0]]['name']] = keymap[key[0]]['type'](key[1:].strip())

    params = spec["params"].keys()
    newparam = {}
    for param in params:
        if param in keymap.keys():
            newparam[keymap[param]['name']] = keymap[param]['type'](spec["params"][param])

    return newparam


def recompute_topo(spec, data_dir,output = None):
    import regulus.file as rf
    import regulus.update.find_reg as fr
    from regulus.morse.morse import morse
    from regulus.update.update_model import update_model

    regulus = fr.get(spec, data_dir=data_dir)

    param = update_params(regulus, spec)

    morse(regulus, args=param)

    update_model(regulus)

    rf.save(regulus, output)

    print("New Structure is available")

    return 1


if __name__ == '__main__':
    pass
