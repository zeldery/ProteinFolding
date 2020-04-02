# ---------------------------------------------------------
# Create by: Tu Nguyen Thien Phuc
# Research group: Rowley group https://www.rowleygroup.net/
# Github: github.com/zeldery
# ---------------------------------------------------------
# Scatter plot for DFT/ANI energy
# ---------------------------------------------------------

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

ENERGY_CONVERSION = 627.5094741
scale = False

lst_name = ['windows_0_6','windows_3_13','windows_18_3']
lst_color = ['r','g','b']
min_x = 0.0
min_y = 0.0
if scale:
    for i in range(3):
        ani = pd.read_csv(lst_name[i] + '.txt', index_col = 0)
        #dft = pd.read_csv(lst_name[i] + '.dat') #Good DFT
        dft = pd.read_csv(lst_name[i] + '.csv', index_col = 0) #Exact DFT
        if dft.iloc[:,0].min()*ENERGY_CONVERSION < min_x:
            min_x = dft.iloc[:,0].min()*ENERGY_CONVERSION
        if ani.iloc[:,0].min() < min_y:
            min_y = ani.iloc[:,0].min()
    min_x -= 10.0
    min_y -= 10.0
for i in range(3):
    ani = pd.read_csv(lst_name[i] + '.txt', index_col = 0)
    #dft = pd.read_csv(lst_name[i] + '.dat') #Good DFT
    dft = pd.read_csv(lst_name[i] + '.csv', index_col = 0)
    plt.scatter(dft.iloc[:,0]*ENERGY_CONVERSION - min_x,ani.iloc[:,0] - min_y,c = lst_color[i])
plt.title('Comparison between ANI potential and DFT reference')
plt.xlabel('DFT potential (kcal/mol)')
plt.ylabel('ANI potential (kcal/mol)')
plt.legend(['(12.5-0.4)','(15.5-0.75)','(30.5-0.25)'])
plt.show()
