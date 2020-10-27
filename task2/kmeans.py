import math
from collections import defaultdict
from itertools import chain

import numpy as np
from matplotlib import colors
import matplotlib.pyplot as plt


NUM_CLUSTERS = 3
COUNT = 100
MAX_V = 100
MIN_V = 1


class Dot:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    @classmethod
    def create_random_dot(cls, min_v, max_v):
        dot = cls(
            np.random.randint(min_v, max_v),
            np.random.randint(min_v, max_v)
        )
        return dot

    def distance(self, other_dot):
        return (
           (self.x - other_dot.x) ** 2 + (self.y - other_dot.y) ** 2
        ) ** 0.5

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash(f'Dot x: {self.x}, y: {self.y}')

    def __str__(self):
        return f'x: {self.x}, y: {self.y}'


def create_random_dots(min_v, max_v, count):
    dots = [Dot.create_random_dot(min_v, max_v) for _ in range(count)]
    return dots


def create_start_center(dots, count_center):

    if count_center < 2:
        return [dots[0]]

    max_distance = -1
    center_dots = []
    dot_center1 = None
    dot_center2 = None

    for i in range(len(dots)):
        start_dot = dots[i]
        for j in range(i + 1, len(dots)):
            dist = start_dot.distance(dots[j])
            if dist > max_distance:
                max_distance = dist
                dot_center1 = start_dot
                dot_center2 = dots[j]

    center_dots.extend((
        dot_center1,
        dot_center2
    ))

    for i in range(count_center - len(center_dots)):
        max_min_distance = -1
        new_center_dot = None

        for dot in dots:
            if dot in center_dots:
                continue
            min_distance = None
            for center_dot in center_dots:
                dist = center_dot.distance(dot)
                if min_distance is None or dist < min_distance:
                    min_distance = dist

            if max_min_distance < min_distance:
                max_min_distance = min_distance
                new_center_dot = dot
        center_dots.append(new_center_dot)
    return center_dots


def get_xy(dots):
    x = []
    y = []
    for dot in dots:
        x.append(dot.x)
        y.append(dot.y)
    return x, y


def show_dots(dots, centers):
    fig, ax = plt.subplots()
    x, y = get_xy(dots)
    ax.scatter(x, y)
    x_center, y_center = get_xy(centers)
    ax.scatter(x_center, y_center, edgecolors='g')
    fig.savefig('dots.png')
    plt.show()


def show_clusters(clusters):
    fig, ax = plt.subplots()
    for index, (center, dots) in enumerate(clusters.items()):
        x, y = get_xy(dots)
        ax.scatter(x, y, edgecolors=list(colors.cnames.keys())[index])
    fig.savefig('clusters.png')
    plt.show()


def update_center(clusters):
    new_centers = []
    for center, dots in clusters.items():
        sum_x = 0
        sum_y = 0
        for dot in dots:
            sum_x += dot.x
            sum_y += dot.y
        center_x = sum_x / len(dots)
        center_y = sum_y / len(dots)
        new_centers.append(Dot(center_x, center_y))
    return new_centers


def sum_dist_to_center(clusters):
    dist = 0
    for center, dots in clusters.items():
        for dot in dots:
            dist += center.distance(dot)
    return dist


def get_clusters(dots, center_dots):
    clusters = defaultdict(list)
    for dot in dots:
        min_dist = None
        t_dot = None
        for center_dot in center_dots:
            dist = center_dot.distance(dot)
            if min_dist is None or dist < min_dist:
                min_dist = dist
                t_dot = center_dot
        if t_dot is not None:
            clusters[t_dot].append(dot)

    return clusters


def get_normalize_clusters(dots, centers):
    clusters = {}
    new_centers = []
    while centers != new_centers:
        new_centers = centers
        clusters = get_clusters(dots, new_centers)
        centers = update_center(clusters)
    return clusters


def get_best_clusters(dots):
    max_k = 10
    min_k = 2
    dist_k = [0] * max_k
    d_k = [-1.0] * max_k
    clusters = [{}] * max_k
    for k in range(min_k, max_k):
        centers = create_start_center(dots, k)
        clusters[k] = get_normalize_clusters(dots, centers)
        dist_k[k] = sum_dist_to_center(clusters[k])
        if dist_k[k - 2]:
            d_k[k - 1] = math.fabs(
                dist_k[k - 1] - dist_k[k]
            ) / math.fabs(
                dist_k[k - 2] - dist_k[k - 1]
            )
    min_dist = min(filter(
        lambda x: x > 0,
        d_k
    ))

    index = d_k.index(min_dist)
    print(f'Количество класстеров: {index}')

    return clusters[index]


def main():
    dots = create_random_dots(MIN_V, MAX_V, COUNT)
    clusters = get_best_clusters(dots)
    show_dots(
        list(chain.from_iterable(clusters.values())),
        clusters.keys()
    )
    show_clusters(clusters)


if __name__ == '__main__':
    main()