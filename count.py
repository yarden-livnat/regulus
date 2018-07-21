import sys
from regulus import file as rf


def count(filename):
    r = rf.load(filename)
    # for name, c in r['morse']['complexes'].items():
    for m in r['mscs']:
        name = m['name']
        total = 0
        n = 0
        for partition in m['partitions']:
            span = partition['span']
            total += span[1] - span[0]+2
            n += 1
        print(name, ': pts:', len(m['pts_idx']), 'n:', n, 'count:', total, 'scale:', total/len(m['pts_idx']))


if __name__ == '__main__':
    if len(sys.argv) == 2:
        count(sys.argv[1])
    else:
        print('usageL count filename')