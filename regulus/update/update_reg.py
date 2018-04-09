#  Convert pts list to pt objects
def pts2json(pts, dims, measures):
    out = []
    for pt in pts:
        cur = {}
        i = 0
        for dim in dims:
            cur[dim] = pt[i]
            i = i + 1
        for measure in measures:
            cur[measure] = pt[i]
            i = i + 1
        out.append(cur)
    return out


# Convert pts objects to pts list
def dict2list(data, dims):
    new_sample_input = [[ptdict[inputdim] for inputdim in dims] for ptdict in data]
    print("NEW_SAMPLE_INPUT", new_sample_input)
    return new_sample_input


# resample with spec
def sample(regulus, spec, data_dir):
    import shutil
    from pathlib import Path
    from regulus.resample.resample import resample

    sim_dir = str(data_dir / 'temp')
    sim_out = 'new_sample_outputs.csv'
    sim_in = 'new_sample_inputs.csv'

    dims = regulus['dims']
    new_inputs = dict2list(spec['pts'], dims)
    result = resample(new_inputs, regulus, sim_dir, sim_in, sim_out)  # run_simulation(new_inputs, regulus)

    path = Path(sim_dir)
    if path.exists():
        shutil.rmtree(sim_dir)
    return result


def add_pts(regulus, pts):
    regulus['pts'] = regulus['pts'] + pts
    return regulus


# calculate MSC, linear_reg, pca
def post_process(regulus, data_dir=None, outfile=None):
    from regulus.math.process import process
    from regulus.morse.morse import morse
    from regulus.file import save

    try:
        morse(regulus)

        process(regulus)

        # Might be changed later due to data_dir
        save(regulus, filename=outfile, dir=data_dir)
        return 0

    except Exception as e:
        print(e)
        print("Error, Recompute MSC Not Finished")
        return 1


def sample_pts(spec, data_dir):
    from regulus.file import get

    regulus = get(spec=spec, dir=data_dir)
    newsamples = sample(regulus, spec, data_dir)
    return [regulus, newsamples]


def get_newreg(spec, data_dir=None, filename=None):
    [regulus, newsamples] = sample_pts(spec, data_dir)
    regulus = add_pts(regulus, newsamples)
    return post_process(regulus, data_dir, filename)


def get_sample(spec, data_dir):
    [regulus, newsamples] = sample_pts(spec, data_dir)
    dims = regulus['dims']
    measures = regulus['measures']
    return pts2json(newsamples, dims, measures)


def get_newreg_with_spec():
    from pathlib import Path
    import argparse

    import json

    p = argparse.ArgumentParser()
    p.add_argument('specname', help='new sample spec .json file]')
    p.add_argument('-o', '--out', help='output file')
    p.add_argument('-d', '--dir', help='regulus.json file dir')
    p.add_argument('--debug', action='store_true', help='compute with all models')

    ns = p.parse_args()

    with open(ns.specname) as f:
        spec = json.load(f)

    data_dir = Path(ns.dir) if ns.dir is not None else spec.parent

    return get_newreg(spec, data_dir, ns.out)


if __name__ == '__main__':
    # pass
    get_newreg_with_spec()
