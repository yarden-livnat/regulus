

def inv_fitness(t,n):
    p = n.parent
    if n.id == -1 or p.id == -1:
        return None
    if len(n.data.y) < 10 or len(p.data.y) < 10:
        return None
    nc = t['inverse_regression'][n][0]
    pc = t['inverse_regression'][p][0]
    d = (pc-nc).dropna()
    d2 = (d*d).sum()/len(d)
    return -d2.max()