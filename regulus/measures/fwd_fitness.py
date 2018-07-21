

def fwd_fitness(msc, partition, x, y):
    return partition['models']['linear_reg'].score(x, y)