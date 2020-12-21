import matplotlib.pyplot as plt
import numpy as np
from plotly import graph_objects
from sklearn.cluster import KMeans
from sklearn.linear_model import SGDClassifier
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC


class DotND:

    def __init__(self, *args):
        self.args_name = []
        self.args = args
        for index, arg in enumerate(args, start=1):
            arg_name = f'x_{index}'
            setattr(self, arg_name, arg)
            self.args_name.append(arg_name)

    @classmethod
    def create_random_dot(cls, min_v, max_v, nd):
        args = [np.random.randint(min_v, max_v) for _ in range(nd)]
        dot = cls(
            *args
        )
        return dot

    @classmethod
    def create_random_dots(cls, min_v=0, max_v=100, count=100, nd=3):
        """
        nd - размерность

        Например, nd = 3 - трёхмерная плоскость
        """
        dots = []
        for _ in range(count):
            dots.append(
                cls.create_random_dot(min_v, max_v, nd)
            )
        return dots

    def distance(self, other_dot):
        if self.args_name != other_dot.args_name:
            return None
        sum_quart = 0
        for arg_name in self.args_name:
            sum_quart += (
                    getattr(self, arg_name) - getattr(other_dot, arg_name)
            ) ** 2
        return sum_quart ** 0.5

    def __eq__(self, other):
        if isinstance(other, list):
            return self in other
        else:
            if self.args_name != other.args_name:
                return True
            for arg_name in self.args_name:
                if getattr(self, arg_name) != getattr(other, arg_name):
                    return True
            return False

    def __hash__(self):
        return hash((
            *self.args_name,
            *map(lambda arg_name: getattr(self, arg_name), self.args_name)
        ))

    def __str__(self):
        names = []
        for arg_name in self.args_name:
            names.append(
                f'{arg_name}={getattr(self, arg_name)}'
            )
        return ', '.join(names)


def get_coordinates(dots):
    coordinates = [dot.args for dot in dots]
    return np.array(list(zip(*coordinates)))


def gradient(x, y, z):
    a = 0
    b = 0
    c = 0

    # Скорость обучения
    L = 0.0001
    # количество итераци
    epochs = 1000

    n = float(len(x))

    # градиентный спуск
    for i in range(epochs):
        # Предсказанное значение
        Z_pred = a * x + b * y + c
        # Производная по a
        D_a = (-1 / n) * sum(x * (z - Z_pred))
        # Производная по b
        D_b = (-1 / n) * sum(y * (z - Z_pred))
        # Производная по c
        D_c = (-1 / n) * sum(z - Z_pred)

        a -= L * D_a
        b -= L * D_b
        c -= L * D_c

    return a, b, c


def main():
    dots = DotND.create_random_dots()

    x, y, z = get_coordinates(dots)

    a, b, c = gradient(x, y, z)

    tmp = np.linspace(0, 100, 100)
    xx, yx = np.meshgrid(tmp, tmp)

    fig = graph_objects.Figure(
        data=[graph_objects.Scatter3d(
            x=x, y=y, z=z, mode='markers',
        )]
    )
    fig.add_trace(graph_objects.Surface(
        x=xx,
        y=yx,
        z=a * xx + b * yx + c
    ))

    fig.show()


if __name__ == '__main__':
    main()
