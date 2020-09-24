import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os

train_dt = pd.read_csv(
    os.path.join('dataset', 'titanic_train.csv')
)

plt.figure(figsize=(30, 10))
train_dt = train_dt[['sex', 'survived']]
survived_dt = train_dt.groupby('sex').sum()
survived_dt['total'] = train_dt.groupby('sex').count()
survived_dt.plot.bar(stacked=True)

plt.show()
