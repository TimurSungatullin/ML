import random
from decimal import Decimal

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from functools import reduce


def to_float(x):
    if isinstance(x, float):
        return x
    return float(x.replace(',', '.'))


def get_prob(symptoms, new_symptom):
    # P(B/A) для всех симптомов
    prob = 1
    for i, symptom in enumerate(symptoms):
        if new_symptom[i] == 1:
            # Симптом есть
            prob *= to_float(symptom)
        else:
            # Симптома нет
            prob *= 1 - to_float(symptom)
    return prob


def get_result(P_disease, data_symptom, new_symptom):
    max_v = None
    result = None
    for index, (dis, prob) in enumerate(P_disease.items(), start=1):
        # P(B/A)
        symptom_prob = get_prob(
            data_symptom.iloc[::, index][1:],
            new_symptom
        )
        # prob - P(A)
        # P(B) - у всех одинаковый, потому что это
        # переумножение вероятностей симптомов всех
        if max_v is None or max_v < symptom_prob * prob:
            max_v = symptom_prob * prob
            result = dis

    return result


def main():
    data_symptom = pd.read_csv('symptom.csv', delimiter=';')
    data_disease = pd.read_csv('disease.csv', delimiter=';')

    count_row = len(data_disease)
    # Формирование P(A)
    P_disease = dict(
        zip(
            list(data_disease['Болезнь'][:count_row - 1]),
            list(data_disease['Случаев'][:count_row - 1] / data_disease['Случаев'][count_row - 1])
        )
    )

    # Тестовые симптомы для получения диагноза
    new_symptom = [random.randint(0, 1) for _ in range(len(data_symptom) - 1)]

    # P(A/B) = P(B/A) * P(A) / P(B)
    result = get_result(P_disease, data_symptom, new_symptom)
    print(result)


if __name__ == '__main__':
    main()

