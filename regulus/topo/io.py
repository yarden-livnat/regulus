from pathlib import Path
from regulus.data.data import Data
from .morse import morse_smale
from regulus.utils import io


def morse_from_csv(filename, ndims=None, measure=None, save=False, **kwargs):
    p = Path(filename)
    data = Data.read_csv(filename, ndims, measure)
    data.normalize()
    msc = morse_smale(data, **kwargs)
    msc.filename = p.with_suffix('.p')
    if save:
        if not isinstance(save, str):
            save = None
        io.save(msc, filename=save)
    return msc