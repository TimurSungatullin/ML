import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

data_symptom = pd.read_csv('symptom.csv', delimiter=';')
data_disease = pd.read_csv('disease.csv', delimiter=';')

P_disease = dict(
    zip(
        list(data_disease['Болезнь']), list(data_disease['Случаев'] / data_disease['Случаев'][9])
    )
)
