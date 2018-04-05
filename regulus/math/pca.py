from sklearn import decomposition


def pca(x, y, args=2):
    pcamodel = decomposition.PCA(n_components=args)
    pcamodel.fit(x)

    components = pcamodel.components_
    vars = pcamodel.explained_variance_

    model = {
        "components": components.tolist(),
        "variance": vars.tolist()
    }

    return model
