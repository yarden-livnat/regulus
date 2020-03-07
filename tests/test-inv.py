import regulus

compute = True

if compute:
    data = regulus.from_csv('gauss4', knn=8)
else:
    data = regulus.load('gauss4')


print('range:', data.tree.attr['data_range'])

n = data.tree.find_id(166)
inv = data.tree.attr['inverse_regression']
curve = inv[n]

print(curve)