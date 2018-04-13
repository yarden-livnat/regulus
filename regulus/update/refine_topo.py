from regulus.resample.resample import resample
from regulus.update.update_model import update_model
import regulus.update.find_reg as find_reg
from regulus.morse.morse import morse
import regulus.file as rf


# resample with spec
def sample(regulus, spec, data_dir):
    dims = regulus['dims']
    new_inputs = [[item[dim] for dim in dims] for item in spec['pts']]
    result = resample(new_inputs, regulus)
    return result


def add_pts(regulus, pts):
    regulus['pts'] = regulus['pts'] + pts
    return regulus


# calculate MSC, linear_reg, pca
def post_process(regulus, data_dir=None, outfile=None):
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
    regulus = find_reg.get(spec, wdir=data_dir)
    newsamples = sample(regulus, spec, data_dir)
    return [regulus, newsamples]


#
# External Usage
#

def refine(spec, data_dir=None, filename=None):
    [regulus, samples] = create_samples(spec, data_dir)
    add_pts(regulus, samples)
    return post_process(regulus, data_dir, filename)


def get_sample(spec, data_dir):
    [regulus, samples] = create_samples(spec, data_dir)
    cols = regulus['dims'] + regulus['measures']
    return [ dict(zip(cols, values)) for values in samples]
