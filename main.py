import matplotlib.pyplot as plt
import numpy as np
import networkx as nx


def find_first_link():
    minim = matrix[0][1]
    a = 0
    b = 1
    for i in range(n):
        for j in range(i + 1, n):
            if minim > matrix[i][j]:
                minim = matrix[i][j]
                a = i
                b = j
    link_matrix[a][b] = 1
    link_matrix[b][a] = 1
    link_dots[a] = link_dots[b] = 1


def link_all_dot():
    minim = None
    a = -1
    b = -1
    for i in range(n):
        if not link_dots[i]:
            continue
        for j in range(n):
            if link_dots[j] or i == j:
                continue
            if minim is None or minim > matrix[i][j]:
                minim = matrix[i][j]
                a = i
                b = j
    if minim:
        link_matrix[a][b] = link_matrix[b][a] = 1
        link_dots[a] = link_dots[b] = 1


n = 5
matrix = [[0 for i in range(n)] for i in range(n)]
link_matrix = [[0 for i in range(n)] for i in range(n)]
for i in range(n):
    for j in range(i, n):
        matrix[i][j] = np.random.randint(1, 100)
        matrix[j][i] = matrix[i][j]

print(matrix)

k = 3
link_dots = [0] * n
find_first_link()
while not all(link_dots):
    link_all_dot()
print(link_matrix)

# TODO Вывести
graph = nx.Graph()
node_name = 'V'
for i in range(n):
    graph.add_node(f'{node_name}{i}')
weights = []
for i in range(n):
    for j in range(i + 1, n):
        if link_matrix[i][j]:
            graph.add_edge(
                f'{node_name}{i}',
                f'{node_name}{j}',
                weight=matrix[i][j]
            )
            weights.append(matrix[i][j])

nx.draw_circular(
    graph,
    node_color='r',
    node_size=1000,
    with_labels=True,
)

plt.show()
