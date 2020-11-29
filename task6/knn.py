from collections import defaultdict, Counter

from task2.kmeans import create_random_dots, COUNT, show_clusters


def create_clusters(n, count):
    clusters = defaultdict(list)
    train_dots = []
    for i in range(n):
        dots = create_random_dots(count=count, cluster=i)
        clusters[i].extend(dots)
        train_dots.extend(dots)
    return clusters, train_dots


def get_dist_to_all_dots(clusters, other_dot):
    # Получаем расстояние до всех точек кластера
    dots_dist = []
    for cluster, dots in clusters.items():
        for dot in dots:
            dist = dot.distance(other_dot)
            dots_dist.append((
                dot, dist
            ))
    return dots_dist


def distribution_dots(train_clusters, test_dots, k):
    """
    Распределение тестовых точек
    """
    clusters = train_clusters.copy()
    for test_dot in test_dots:
        dist = get_dist_to_all_dots(train_clusters, test_dot)
        neighbor = Counter()
        # Берём k ближайших соседей и считаем к каким кластерам
        # они принадлежат
        for dot, dist in sorted(
                dist, key=lambda dots: dots[1],
        )[:k]:
            neighbor[dot.cluster] += 1
        # Берём максимально часто встречающийся кластер
        cluster = sorted(neighbor.items(), key=lambda item: item[1])[-1]
        test_dot.cluster = cluster[0]
        clusters[cluster[0]].append(test_dot)
    return clusters


def main():
    k = 10
    # Число кластеров
    n = 3
    count = COUNT
    clusters, train_dots = create_clusters(n, count // n)
    show_clusters(clusters, filename='train_clusters.png')
    test_dots = create_random_dots(count=count)
    clusters = distribution_dots(clusters, test_dots, k)
    show_clusters(clusters)


if __name__ == '__main__':
    main()
