import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pandas.tools.plotting import table
from mpl_toolkits.mplot3d import Axes3D

def custom(dataframe):
	x = np.array([0,1,2,3])
	y = np.array([0.650, 0.660, 0.675, 0.685])
	my_xticks = ['a', 'b', 'c', 'd']
	plt.xticks(x, dataframe['LATIT'])
	plt.yticks(y, dataframe['LONGIT'])
	plt.plot(x, y)
	plt.grid(axis='y', linestyle='-')
	plt.grid(axis='y', linestyle='-')
	plt.show()
    ##sz = dataframe.groupby('Price')

    ##total = sz.sum()
    ##total.sort()

    ##my_plot = sz.size().plot.hist()
    ##my_plot.clear()
    ##print(type(my_plot))

	###df = pd.DataFrame(np.random.rand(5, 3), columns=['a', 'b', 'c'])
	###fig, ax = plt.subplots(1,1)
	###table(ax, np.round(df.describe(), 2), loc="upper right", colWidths=[0.2, 0.2, 0.2])
	###my_plot=df.plot(ax=ax, ylim=(0, 2), legend=None)
	
	return my_plot
