from matplotlib import colors

from task2.kmeans import create_random_dots, COUNT, Dot, show_dots, get_xy
import numpy as np
import matplotlib.pyplot as plt
import math


def update_center(c, count, f_m, dots, v_centers):
    # Уточнение центров
    for i in range(c):
        sum_f_m = 0
        sum_dot_x = 0
        sum_dot_y = 0
        for k in range(count):
            pow_f_m = f_m[k, i] ** m
            sum_f_m += pow_f_m
            sum_dot_x += pow_f_m * dots[k].x
            sum_dot_y += pow_f_m * dots[k].y
        v_centers[i] = Dot(sum_dot_x / sum_f_m, sum_dot_y / sum_f_m)
    return v_centers


def calc_dist(c, count, dots, dist_m, v_centers):
    # Расчёт расстояний
    for i in range(count):
        for j in range(c):
            dist_m[i][j] = dots[i].distance(v_centers[j])
    return dist_m


def calc_f_m(c, count, f_m, dist_m, m):
    # Расчёт степеней принадлежности
    for i in range(count):
        for k in range(c):
            d = 0
            for j in range(c):
                d += (dist_m[i][k] / dist_m[i][j]) ** (2 / (m - 1))
            f_m[i][k] = 1 / d
    return f_m


def is_end(c, count, f_m, f_m_prev):
    # Условие остановки
    max_v = 0
    for i in range(count):
        for k in range(c):
            s = math.fabs(f_m[i][k] - f_m_prev[i][k])
            if max_v < s:
                max_v = s
    return max_v


def show(f_m, dots, centers):
    fig, ax = plt.subplots()
    cache_colors = list(colors.cnames.keys())
    all_colors = []
    for index, dot in enumerate(f_m):
        # Максимальная вероятность
        index_max_v = list(dot).index(max(dot))
        all_colors.append(cache_colors[index_max_v + 10])
    x, y = get_xy(dots)
    ax.scatter(
        x, y,
        edgecolors=all_colors
    )
    centers_x, centers_y = get_xy(centers)
    ax.scatter(
        centers_x,
        centers_y,
        edgecolors=cache_colors[len(centers) * 5 + 1],
        s=100
    )
    fig.savefig('clusters.png')
    plt.show()


def main():
    # экспоненциальный вес (Степень "размытости")
    m = 2
    # Число кластеров
    c = 2
    count = COUNT
    dots = create_random_dots(count=count)
    f_m = np.random.dirichlet([1] * c, size=len(dots))
    f_m_prev = None
    v_centers = [None] * c
    dist_m = [[0] * c for _ in range(len(dots))]
    e = 0.00001
    max_v = e + 1
    while max_v > e:

        v_centers = update_center(c, count, f_m, dots, v_centers)

        dist_m = calc_dist(c, count, dots, dist_m, v_centers)

        f_m_prev = f_m.copy()
        f_m = calc_f_m(c, count, f_m, dist_m, m)

        max_v = is_end(c, count, f_m, f_m_prev)

    show_dots(dots, v_centers)
    show(f_m, dots, v_centers)
    print(f_m)


if __name__ == '__main__':
    main()
