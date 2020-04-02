# ---------------------------------------------------------
# Create by: Tu Nguyen Thien Phuc
# Research group: Rowley group https://www.rowleygroup.net/
# Github: github.com/zeldery
# ---------------------------------------------------------
# Read and combine the collectible data from umbrella 
# sampling
# ---------------------------------------------------------

import os

f = open('good_windows.txt','r')
lines = f.readlines()
f.close()

for line in lines:
    i,j = line.split()
    name = 'windows_{}_{}'.format(i,j)
    k = 0
    fout = open('traj/{}.traj'.format(name),'w')
    old_dat = ''
    while os.path.exists('{}/ala_prod{}.colvars.traj'.format(name,k)):
        fin = open('{}/ala_prod{}.colvars.traj'.format(name,k),'r')
        dats = fin.readlines()
        fin.close()
        for dat in dats:
            tmp = dat.split()
            if len(tmp) < 4:
                continue
            if tmp[0] == '#':
                continue
            if dat == old_dat:
                continue
            fout.write('{} {} {}\n'.format(tmp[0],float(tmp[2]),float(tmp[3])))
            old_dat = dat
        k += 1
    print('{} has {}'.format(name,k))
    fout.close()
    