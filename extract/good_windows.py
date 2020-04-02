# ---------------------------------------------------------
# Create by: Tu Nguyen Thien Phuc
# Research group: Rowley group https://www.rowleygroup.net/
# Github: github.com/zeldery
# ---------------------------------------------------------
# Detect the windows that has configuration lies inside the
# windows after dragging process
# ---------------------------------------------------------


import numpy as np
import pandas as pd

input_name = 'result4.csv'
output_name = 'good_windows.txt'
criterion = 1.0

dat = pd.read_csv(input_name,index_col = 0)
good = (np.abs(dat['real_dist'] - dat['rest_dist'])<=0.5*criterion) & (
          np.abs(dat['real_helix'] - dat['rest_helix']) <= 0.025*criterion)
f = open(output_name,'w')
for k in range(340):
    if good[k]:
        f.write(str(dat['dist_index'][k]) + ' ' + str(dat['helix_index'][k]) + '\n')

f.close()

