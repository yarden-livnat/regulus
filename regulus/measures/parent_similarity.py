

def parent_similarity(msc, partition, x, y):
    p_idx = partition['parent']
    if p_idx is None:
        return 1
    parent = msc['partitions'][p_idx]
    return parent['models']['linear_reg'].score(x, y)