# ---------------------------------------------------------
# Create by: Tu Nguyen Thien Phuc
# Research group: Rowley group https://www.rowleygroup.net/
# Github: github.com/zeldery
# ---------------------------------------------------------
# The script to generate the NAMD simulation to create the
# initial structure for umbrella sampling
# ---------------------------------------------------------

import os
import shutil

# List of necessary files
need_file = ['sub.sh','rest.tcl', 'ala_make.conf','ala_min.coor', 'ala_min.xsc', 'ala_sol.pdb',
            'ala_sol.psf']

# List of windows
list_distance = [12.5,13.5,14.5,15.5,16.5,17.5,18.5,19.5,20.5,21.5,22.5,23.5,24.5,25.5,26.5,27.5,28.5,29.5,30.5,31.5]
list_helix = [0.1,0.15,0.2,0.25,0.3,0.35,0.4,0.45,0.5,0.55,0.6,0.65,0.7,0.75,0.8,0.85,0.9]

n_distance = len(list_distance)
n_helix = len(list_helix)

for i in range(n_distance):
    for j in range(n_helix):
        dir = 'windows_' + str(i) + '_' + str(j)
        os.system('mkdir ' + dir)
        for file_name in need_file:
            os.system('cp source/' + file_name + ' ' + dir)
        os.system('cp -r source/toppar '+ dir)
        os.chdir(dir)
        f = open('sub.sh','a')
        f.write('#SBATCH --job-name=' + dir)
        f.close()
        f = open('rest.tcl','a')
        f.write('''harmonic {
  name end_to_end_rest
  colvars end_to_end
  forceConstant 10.0
  centers 1.519867e+01
  targetCenters ''' + str(list_distance[i]) + '''
  targetNumSteps 500000
}''')
        f.write('''
harmonic {
  name helicity_rest
  colvars helicity
  forceConstant 1000.0
  centers 7.86224e-01
  targetCenters ''' + str(list_helix[j]) + '''
  targetNumSteps 500000
}''')
        f.close()
        os.system('sbatch sub.sh')
        os.chdir('..')
        
        
        
