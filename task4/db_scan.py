from collections import defaultdict

from matplotlib import colors
import matplotlib.pyplot as plt

from task2.kmeans import create_random_dots, COUNT, show_clusters, get_xy

# Зоны
GREEN = 'green'
YELLOW = 'yellow'
RED = 'red'


def get_neighbours(dots, dot, need_dist):
    # Получаем всех соседей
    neighbours = set(d for d in dots if d.distance(dot) <= need_dist and d != dot)
    return neighbours


def show_clusters1(dots, clusters):
    fig, ax = plt.subplots()
    x, y = get_xy(dots)
    ax.scatter(x, y, edgecolors='r')
    for index, (_, dots) in enumerate(clusters.items()):
        x, y = get_xy(dots)
        ax.scatter(x, y, edgecolors=list(colors.cnames.keys())[index])
    fig.savefig('db_scan_clusters.png')
    plt.show()


def main():
    dots = create_random_dots(count=COUNT)
    need_neighbours = 2
    need_dist = 10
    visited_dots = {}
    clusters = defaultdict(list)
    num_cluster = 0

    for dot in dots:
        if dot not in visited_dots:

            neighbours = get_neighbours(dots, dot, need_dist)

            if len(neighbours) > need_neighbours:
                visited_dots[dot] = GREEN
                # Смотрим соседей
                num_cluster += 1
                clusters[num_cluster].append(dot)
                dot.cluster = num_cluster
                while neighbours:
                    # show_clusters1(dots, clusters)
                    d = neighbours.pop()
                    if d not in visited_dots:
                        n_neighbours = get_neighbours(dots, d, need_dist)
                        visited_dots[d] = YELLOW
                        clusters[num_cluster].append(d)
                        d.cluster = num_cluster
                        if len(n_neighbours) > need_neighbours:
                            neighbours = neighbours.union(n_neighbours)
                    if d not in clusters.values():
                        clusters[num_cluster].append(d)
                        d.cluster = num_cluster

            elif len(neighbours) == 0:
                visited_dots[dot] = RED
                clusters[RED].append(dot)
            else:
                visited_dots[dot] = YELLOW

    # Разбираемся с точками на границе,
    # которые ещё не принадлежат кластерам
    for dot, color in visited_dots.items():
        if getattr(dot, 'cluster', None) is None and color == YELLOW:
            min_v = None
            neighbour = None
            neighbours = get_neighbours(dots, dot, need_dist)
            for n in neighbours:
                if min_v is None or min_v > n.distance(dot):
                    min_v = n.distance(dot)
                    neighbour = n
            if neighbour and getattr(neighbour, 'cluster', None):
                clusters[neighbour.cluster].append(dot)

    show_clusters(clusters)


if __name__ == '__main__':
    main()
