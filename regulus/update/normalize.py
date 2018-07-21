import numpy as np

from sklearn.preprocessing import StandardScaler


def normalize(regulus):
    scaler = StandardScaler(copy=False)
    pts = np.array(regulus['pts'])
    x = pts[:, 0:len(regulus['dims'])]
    scaler.fit_transform(x)
    regulus['pts'] = pts.tolist()
    regulus['normalize'] = {
        'mean': scaler.mean_.tolist(),
        'scale': scaler.scale_.tolist()
    }
