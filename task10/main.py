import pygame as pg

import numpy as np
import cv2

from task10.model import get_model


def get_prediction(size, model):
    img = cv2.imread('picture.png', cv2.IMREAD_GRAYSCALE)
    (thresh, img) = cv2.threshold(img, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    thresh = 127
    img = cv2.threshold(img, thresh, 255, cv2.THRESH_BINARY)[1]
    img = norm_digit(img, size)
    img = cv2.resize(img, dsize=(28, 28))
    cv2.imwrite('picture_processing.png', img)
    img = np.array(img).reshape(1, 28, 28, 1)

    pred = model.predict(img)
    return np.argmax(pred, axis=1)[0]


def norm_digit(im, size):
    """
    Центрирование
    """
    min_x, min_y, max_x, max_y = size
    min_x = max(0, min_x - 20)
    min_y = max(0, min_y - 20)
    max_x = min(400, max_x + 20)
    max_y = min(400, max_y + 20)
    return im[min_y:max_y, min_x:max_x]


def main():
    max_x = 0
    max_y = 0
    min_x = 401
    min_y = 401

    pg.init()
    sc = pg.display.set_mode((400, 400))
    WHITE = pg.Color('white')
    BLACK = pg.Color('black')
    GREEN = pg.Color('green')
    sc.fill(BLACK)
    pg.display.update()
    f1 = pg.font.Font(None, 36)

    play = True

    model = get_model('mnist_copy2.h5')
    flag = False

    while play:
        pos = pg.mouse.get_pos()
        for i in pg.event.get():
            if i.type == pg.QUIT:
                pg.quit()
                play = False
            if i.type == pg.MOUSEBUTTONDOWN:
                flag = True
                if i.button == 3:
                    pg.image.save(sc, 'picture.png')
                    size = min_x, min_y, max_x, max_y
                    num = get_prediction(size, model)
                    text1 = f1.render(f'Цифра: {num}', True, GREEN)
                    sc.blit(text1, (10, 10))
                    pg.display.update()
                    pg.image.save(sc, f'result_{num}.png')
            if i.type == pg.MOUSEBUTTONUP:
                flag = False
            if i.type == pg.KEYDOWN and i.key == pg.K_SPACE:
                sc.fill(BLACK)
                pg.display.update()
                max_x = 0
                max_y = 0
                min_x = 401
                min_y = 401
        if flag:
            new_pos = pg.mouse.get_pos()
            pg.draw.line(sc, WHITE, pos, new_pos, 10)
            max_x = max(max_x, pos[0], new_pos[0])
            min_x = min(min_x, pos[0], new_pos[0])
            max_y = max(max_y, pos[1], new_pos[1])
            min_y = min(min_y, pos[1], new_pos[1])
            pg.display.update()


if __name__ == '__main__':
    main()
