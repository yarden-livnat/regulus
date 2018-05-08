from regulus.math.similarity import calc_similarity

SIMILARITIES = ['parent', 'sibling']


def update_sim(regulus, sim=None, model=None, measure=None):
    calc_similarity(regulus, SIMILARITIES, sim_func=sim, model_func=model, measure=measure)
