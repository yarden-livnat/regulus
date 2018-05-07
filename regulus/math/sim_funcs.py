import abc
import six


@six.add_metaclass(abc.ABCMeta)
class Sim(object):
    @abc.abstractmethod
    def calc_sim(self, v1, v2):
        pass


class Pearson_corr(object):
    def calc_sim(self, v1, v2):
        from scipy.stats.stats import pearsonr
        r, p = pearsonr(v1, v2)
        return r
        # print("Method in third-party class, " + str(data))


class Cos_sim(object):
    def calc_sim(self, v1, v2):
        # from scipy.stats.stats import pearsonr
        # r, p = pearsonr(v1, v2)
        # return r
        print(v1, v2)
        # print("Method in third-party class, " + str(data))


SIM_FUNCS = {
    "cosine": Cos_sim,
    "pearson": Pearson_corr
}


def get_sim(sim_func):

    # register sim_func
    if sim_func is None:
        Sim.register(Pearson_corr)
        new_sim = Pearson_corr()

    elif sim_func in SIM_FUNCS:
        corr_func = SIM_FUNCS(sim_func)
        Sim.register(corr_func)
        new_sim = corr_func()

    else:
        print("Could not recognize similarity functions")
        return

    return new_sim.calc_sim

# def pearson_sim(v1, v2):
#    from scipy.stats.stats import pearsonr
#    r, p = pearsonr(v1, v2)
#    return r
