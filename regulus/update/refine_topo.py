#### Internal

#  Convert pts list to pt objects
def list2obj(pts, dims, measures):
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
def obj2list(data, dims):
    new_sample_input = [[item[dim] for dim in dims] for item in data]
    print("NEW_SAMPLE_INPUT", new_sample_input)
    return new_sample_input


# resample with spec
def sample(regulus, spec, data_dir):
    from regulus.resample.resample import resample

    dims = regulus['dims']
    new_inputs = obj2list(spec['pts'], dims)
    result = resample(new_inputs, regulus)  # run_simulation(new_inputs, regulus)

    return result


def add_pts(regulus, pts):
    regulus['pts'] = regulus['pts'] + pts
    return regulus


# calculate MSC, linear_reg, pca
def post_process(regulus, data_dir=None, outfile=None):
    from regulus.update.update_model import update_model
    from regulus.morse.morse import morse
    import regulus.file as rf

    try:
        morse(regulus)

        update_model(regulus)

        # Might be changed later due to data_dir
        rf.save(regulus, filename=outfile, data_dir=data_dir)
        return 0

    except Exception as e:
        print(e)
        print("Error, Recompute MSC Not Finished")
        return 1


def create_samples(spec, data_dir):
    import regulus.update.find_reg as fr

    regulus = fr.get(spec, wdir=data_dir)
    newsamples = sample(regulus, spec, data_dir)
    return [regulus, newsamples]


##### External Usage

def refine(spec, data_dir=None, filename=None):
    [regulus, newsamples] = create_samples(spec, data_dir)
    regulus = add_pts(regulus, newsamples)
    return post_process(regulus, data_dir, filename)


def get_sample(spec, data_dir):
    [regulus, newsamples] = create_samples(spec, data_dir)
    dims = regulus['dims']
    measures = regulus['measures']
    return list2obj(newsamples, dims, measures)
