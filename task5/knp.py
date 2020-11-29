from collections import defaultdict

from task2.kmeans import COUNT, create_random_dots, show_clusters


def fill_dist_matrix(dots):
    count = len(dots)
    matrix = [[0 for _ in range(count)] for _ in range(count)]
    for i in range(count):
        matrix[i][i] = None
        for j in range(i + 1, count):
            matrix[j][i] = matrix[i][j] = dots[i].distance(dots[j])
    return matrix


def find_min(matrix, visited_dots=frozenset()):
    """
    Находим ближайшую не соединенную точку к
    цепочке точек, если ещё нет цепочки, то находим
    две ближайшие точки
    """
    count = len(matrix)
    min_v = None
    dots = ()
    # Если ещё нет посещенных точек, то ищем из всех
    unvisited_dots = {}
    all_dots = False
    if not visited_dots:
        visited_dots = tuple(range(count))
        all_dots = True
    else:
        unvisited_dots = set(range(count)) - visited_dots
    for i in visited_dots:
        if all_dots:
            unvisited_dots = range(i + 1, count)
        for j in unvisited_dots:
            if j in visited_dots and not all_dots:
                continue
            if min_v is None or matrix[i][j] < min_v:
                min_v = matrix[i][j]
                dots = i, j
    return dots, min_v


def fill_edge(dots, edge_matrix, w):
    edge_matrix[dots[0]][dots[1]] = edge_matrix[dots[1]][dots[0]] = w


def remove_edge(edge_matrix, k):
    """
    Удаляем k - 1 ребер, чтобы образовалось k кластеров
    """
    while k - 1:
        max_v = -1
        edge = ()
        for i in range(len(edge_matrix)):
            for j in range(i + 1, len(edge_matrix)):
                if edge_matrix[i][j] > max_v:
                    max_v = edge_matrix[i][j]
                    edge = i, j
        k -= 1
        edge_matrix[edge[0]][edge[1]] = edge_matrix[edge[1]][edge[0]] = 0


def get_clusters(edge_matrix, dots):
    """
    Получаем матрицу на основе матрицы смежности
    """
    clusters = defaultdict(list)
    cluster_num = 0
    for i in range(len(edge_matrix)):
        for j in range(i + 1, len(edge_matrix)):
            if edge_matrix[i][j]:
                dot_cluster1 = getattr(dots[i], 'cluster', None)
                dot_cluster2 = getattr(dots[j], 'cluster', None)
                # Если у обоих точек есть уже кластер, то надо объединить,
                # Если только у одного, то присоединить к существующему,
                # Иначе создать новый
                if dot_cluster1 is not None and dot_cluster2 is not None:
                    clusters[dot_cluster1].extend(
                        clusters[dot_cluster2]
                    )
                    for dot in clusters[dot_cluster2]:
                        dot.cluster = dot_cluster1
                    del clusters[dot_cluster2]
                elif dot_cluster1 is not None:
                    clusters[dot_cluster1].append(
                        dots[j]
                    )
                    dots[j].cluster = dot_cluster1
                elif dot_cluster2 is not None:
                    clusters[dot_cluster2].append(
                        dots[i]
                    )
                    dots[i].cluster = dot_cluster2
                else:
                    clusters[cluster_num].extend((
                        dots[i],
                        dots[j]
                    ))
                    dots[i].cluster = cluster_num
                    dots[j].cluster = cluster_num
                    cluster_num += 1
    return clusters


def main():
    k = 3
    count = COUNT
    dots = create_random_dots(count=count)
    visited_dots = set()
    edge_matrix = [[0 for _ in range(count)] for _ in range(count)]
    dist_matrix = fill_dist_matrix(dots)

    while len(visited_dots) != count:
        min_dots, min_v = find_min(dist_matrix, visited_dots)
        fill_edge(min_dots, edge_matrix, min_v)
        visited_dots = visited_dots.union(set(min_dots))

    remove_edge(edge_matrix, k)

    cluster = get_clusters(edge_matrix, dots)
    show_clusters(cluster)


if __name__ == '__main__':
    main()
