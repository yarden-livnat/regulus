import regulus.file as rf

from regulus.morse.morse import morse
from regulus.update.update import update

import regulus.update.find_reg as find_reg

PARAMS = {
    'k': {'name': 'knn', 'type': int},
    'G': {'name': 'graph', 'type': str},
    'g': {'name': 'gradient', 'type': str},
    'n': {'name': 'norm', 'type': str},
    'b': {'name': 'beta', 'type': float}
}


def get_params(spec):
    params = {}
    for p in spec["params"]:
        if p in PARAMS:
            item = PARAMS[p]
            params[item['name']] = item['type'](spec["params"][p])
    return params


def recompute_topo(spec, data_dir, output=None):
    regulus = find_reg.get(spec, wdir=data_dir)
    regulus["name"] = spec["name"]
    regulus["version"] = spec["new_version"]

    params = get_params(spec)
    morse(regulus, args=params)
    update(regulus)

    rf.save(regulus, output)
