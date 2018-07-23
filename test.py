from regulus.topo.data import Data
from regulus.topo.morse import morse_smale
from regulus.utils.io import save

pts = Data.read_csv('data/gauss4.csv')
# pts.normalize()

topo = morse_smale(pts, knn=8)
save(topo, 'data/gauss4.p')
