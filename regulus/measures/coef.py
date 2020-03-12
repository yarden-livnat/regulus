from sklearn.metrics.pairwise import cosine_similarity


def coef_change(context, node):
    if node.id < 0 or node.parent.id < 0:
        return None

    n_coef = context['model'][node].coef_
    p_coef = context['model'][node.parent].coef_
    if len(n_coef) == len(p_coef) :
        return cosine_similarity([n_coef], [p_coef])[[0][0]][0]
    return None


def coef_similarity(context, node):
    n_coef = context['model'][node].coef_
    s_coef = context['shared_model'][node].coef_
    if len(n_coef) == len(s_coef):
        return cosine_similarity([n_coef], [s_coef])[[0][0]][0]
    return None
