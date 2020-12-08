import pygame as pg
from sklearn import svm

WHITE = pg.Color('white')
RED = pg.Color('red')
GREEN = pg.Color('green')
BLUE = pg.Color('blue')
LEFT = 1
RIGHT = 3

sc = pg.display.set_mode((600, 400))
sc.fill(WHITE)
pg.display.update()

dots = {}
colors = []

clf = None
is_exit = True


def redraw_dots(dots):
    """
    Перерисуем точки, чтобы убрать существующие линии
    """
    sc.fill(WHITE)
    for dot, dot_color in dots.items():
        pg.draw.circle(
            sc, dot_color, dot, 5)


while is_exit:
    for i in pg.event.get():
        if i.type == pg.QUIT:
            is_exit = False
        elif i.type == pg.MOUSEBUTTONDOWN and i.button in (LEFT, RIGHT):
            # Проставление точек
            if i.button == LEFT:
                color = RED
            else:
                color = BLUE
            pg.draw.circle(
                sc, color, i.pos, 5)

            dots[i.pos] = color

            colors.append(
                i.button
            )
            pg.display.update()

        elif i.type == pg.KEYDOWN and i.key == pg.K_RETURN:
            # Разделение точек
            redraw_dots(dots)
            clf = svm.SVC(kernel='linear', C=1.0)
            clf.fit(
                tuple(dots.keys()),
                colors
            )
            w = clf.coef_[0]
            i = clf.intercept_
            n = -w[0] / w[1]
            m = i[0] / w[1]
            Y_1 = -m
            X_1 = m / n
            reverse_coefficient = tuple(map(lambda x: 1 / x, w))
            Y_2, X_2 = (
                reverse_coefficient[1] + Y_1,
                reverse_coefficient[0] + X_1
            )
            Y_3, X_3 = (
                -reverse_coefficient[1] + Y_1,
                -reverse_coefficient[0] + X_1
            )
            pg.draw.line(sc, GREEN, [0, Y_1], [X_1, 0], 1)
            pg.draw.aaline(sc, GREEN, [0, Y_2], [X_2, 0])
            pg.draw.aaline(sc, GREEN, [0, Y_3], [X_3, 0])

            pg.display.update()

    pg.time.delay(30)
