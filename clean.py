from regulus import file as rf


def clean():
    print('clean')
    r = rf.load('/Users/yarden/data/regulus/model/gauss4.json')
    z = r['morse']['complexes']['z']
    for partition in z['partitions']:
        del partition['model']
    rf.save(r, '/Users/yarden/data/regulus/model/gauss4.json')


if __name__ == '__main__':
    clean()