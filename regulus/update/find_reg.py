from pathlib import Path
import regulus.file as rf

def get(spec, wdir=None):

    name = spec['name']
    version = spec['version']

    if wdir is None:
        wdir = Path('.')

    filename = wdir / "{}.{}.json".format(name, version)
    if not filename.exists():
        filename = wdir / "{}.json".format(name)
        if not filename.exists():
            raise FileNotFoundError()
    return rf.load(filename)
