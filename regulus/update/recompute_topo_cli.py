from regulus.update.recompute_topo import recompute_topo


def recompute_topo_cli():
    from pathlib import Path
    import argparse

    import json

    p = argparse.ArgumentParser()
    p.add_argument('specname', help='new parameter spec .json file]')
    p.add_argument('-o', '--out', help='output file')
    p.add_argument('-d', '--dir', help='regulus.json file dir')

    ns = p.parse_args()

    with open(ns.specname) as f:
        spec = json.load(f)

    data_dir = Path(ns.dir) if ns.dir is not None else spec.parent

    return recompute_topo(spec, data_dir, ns.out)


if __name__ == '__main__':
    # pass
    recompute_topo_cli()
