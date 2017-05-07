import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pandas.tools.plotting import table

def custom(dataframe):
    #sz = dataframe.groupby('Price')

    #total = sz.sum()
    #total.sort()

    #my_plot = sz.size().plot.hist()
    #my_plot.clear()
    #print(type(my_plot))

    df = pd.DataFrame(np.random.rand(5, 3), columns=['a', 'b', 'c'])
    fig, ax = plt.subplots(1,1)
    table(ax, np.round(df.describe(), 2), loc="upper right", colWidths=[0.2, 0.2, 0.2])
    my_plot=df.plot(ax=ax, ylim=(0, 2), legend=None)

    return my_plot
