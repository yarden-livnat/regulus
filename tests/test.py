import argparse
from regulus.data.data import Data
from regulus.topo.morse import morse_smale
from regulus.utils.io import save


p = argparse.ArgumentParser()
p.add_argument('filename', help='input file')
p.add_argument('-d', '--dims', type=int, help='dimensions')
p.add_argument('-m', '--measure', help='measure')
p.add_argument('-k', '--knn', default=8, type=int, help='knn')

ns = p.parse_args()

pts = Data.read_csv(ns.filename+'.csv', ndims=ns.dims)
pts.normalize()

topo = morse_smale(pts, knn=ns.knn, measure=ns.measure)
save(topo, ns.filename)