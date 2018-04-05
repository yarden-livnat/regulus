import shutil
from regulus.file import get, save
from regulus.morse.morse import morse
from regulus.math.process import process
from regulus.resample.resample import resample


# Used for validation
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


# Dict to list
def dict2list(data, dims):
    new_sample_input = [[ptdict[inputdim] for inputdim in dims] for ptdict in data]
    print("NEW_SAMPLE_INPUT", new_sample_input)
    return new_sample_input


# resample with spec
def sample(regulus, spec, sim_dir, sim_in, sim_out):
    dims = regulus['dims']
    new_inputs = dict2list(spec['pts'], dims)
    result = resample(new_inputs, regulus, sim_dir, sim_in, sim_out)  # run_simulation(new_inputs, regulus)

    shutil.rmtree(sim_dir)
    return result


def add_pts(regulus, pts):
    regulus['pts'] = regulus['pts'] + pts
    return regulus


# calculate MSC, linear_reg, pca
def post_process(regulus, data_dir):
    try:

        morse(regulus)

        process(regulus)

        # Might be changed later
        save(regulus)
        return 0

    except Exception as e:
        print(e)
        print("Error, Recompute MSC Not Finished")
        return 1


# resample function
def resample2(spec, data_dir, sim_dir, sim_in, sim_out):
    regulus = get(spec=spec, dir=data_dir)
    newsamples = sample(regulus, spec, sim_dir, sim_in, sim_out)
    regulus = add_pts(regulus, newsamples)
    return post_process(regulus, data_dir)


# validate function
def get_sample(spec, data_dir, sim_dir, sim_in, sim_out):
    regulus = get(spec=spec, dir=data_dir)
    newsamples = sample(regulus, spec, sim_dir, sim_in, sim_out)
    dims = regulus['dims']
    measures = regulus['measures']
    return pts2json(newsamples, dims, measures)


if __name__ == '__main__':
    pass
