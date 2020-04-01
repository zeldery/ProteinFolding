# ---------------------------------------------------------
# Create by: Tu Nguyen Thien Phuc
# Research group: Rowley group https://www.rowleygroup.net/
# Github: github.com/zeldery
# ---------------------------------------------------------
# The script includes the function to run the production 
# of the NAMD
# ---------------------------------------------------------

import os

# List of windows
list_distance = [12.5,13.5,14.5,15.5,16.5,17.5,18.5,19.5,20.5,21.5,22.5,23.5,24.5,25.5,26.5,27.5,28.5,29.5,30.5,31.5]
list_helix = [0.1,0.15,0.2,0.25,0.3,0.35,0.4,0.45,0.5,0.55,0.6,0.65,0.7,0.75,0.8,0.85,0.9]


def make_conf_file(time):
    '''Create the NAMD configuration file'''
    f = open('ala_prod' + str(time) + '.conf','w')
    f.write('''structure          ala_sol.psf
coordinates        ala_sol.pdb
''')
    if time == 0:
        name = 'ala_make6'
    else:
        name = 'ala_prod' + str(time-1)
    f.write('binCoordinates     ' + name + '.coor\n')
    f.write('extendedSystem     ' + name + '.xsc\n')
    f.write('set temperature    310\n')
    f.write('set outputname     ala_prod' + str(time) + '\n')
    f.write('''set qmprogrampath  /home/zeldery/projects/rrg-crowley-ac/zeldery/prod3/ani/client.py
set qmscratchpath  $::env(RUNDIR)
''')
    f.write('firsttimestep      ' + str(time*250000) + '\n')
    f.write('numsteps           ' + str((time+1)*250000) + '\n')
    f.write('''paraTypeCharmm      on
parameters          toppar/mol.prm
parameters          toppar/par_all36m_prot.prm
parameters          toppar/par_all36_cgenff.prm
parameters          toppar/toppar_water_ions.prm
parameters          toppar/par_all36_lipid.prm
parameters          toppar/par_all36_carb.prm
parameters          toppar/par_all36_na.prm
temperature         $temperature


# Force-Field Parameters
exclude             scaled1-4
1-4scaling          1.0
cutoff              12.0
switching           on
switchdist          10.0
pairlistdist        14.0

timestep            2.0
rigidBonds          all
nonbondedFreq       1
fullElectFrequency  2
stepspercycle       10


# Constant Temperature Control
langevin            on    ;# do langevin dynamics
langevinDamping     1     ;# damping coefficient (gamma) of 1/ps
langevinTemp        $temperature
langevinHydrogen    off    ;# don't couple langevin bath to hydrogens

cellBasisVector1    60.0    0.0   0.0
cellBasisVector2     0.0   60.0   0.0
cellBasisVector3     0.0    0.0  60.0
cellOrigin           0.0    0.0   0.0

wrapAll             on

useGroupPressure      yes ;# needed for rigidBonds
useFlexibleCell       no
useConstantArea       no

langevinPiston        on
langevinPistonTarget  1.01325 ;#  in bar -> 1 atm
langevinPistonPeriod  100.0
langevinPistonDecay   50.0
langevinPistonTemp    $temperature


# QM Part
qmforces              on
qmParamPDB            qmmm.pdb
qmSoftware            custom

# Path
qmexecpath            $qmprogrampath
qmBaseDir             $qmscratchpath
QMColumn              occ
qmChargeMode          none
qmElecEmbed           off

# Collective Variables
colvars               on
''')
    f.write('colvarsConfig         rest.tcl\n')

    f.write('''# Output
outputName          $outputname

restartfreq         1000     ;# 500steps = every 1ps
dcdfreq             1000
xstFreq             1000
outputEnergies      500
outputPressure      500

minimize            0
reinitvels          $temperature

run 250000
''')
    f.close()
    
def make_sub_file(time):
    '''Create a submit file to SLURM system'''
    f = open('sub' + str(time) + '.sh','w')
    f.write('''#!/bin/bash
#
#SBATCH --mem 16GB
''')
    f.write('#SBATCH --output=tim_prod' + str(time) + '.log\n')
    f.write('''#SBATCH --time=24:00:00
#SBATCH --nodes=1
#SBATCH --gres=gpu:2
#SBATCH --job-name=timhortons
#SBATCH --ntasks-per-node=8
#SBATCH --account=rrg-crowley-ac

module load namd-multicore
source /home/zeldery/working/bin/activate
export RUNDIR=/dev/shm/$SLURM_JOB_ID
mkdir $RUNDIR

python /home/zeldery/projects/rrg-crowley-ac/zeldery/prod3/ani/server.py > server.log &
sleep 30s
''')
    f.write('namd2 +p8 ala_prod' + str(time) + '.conf > ala_prod' + str(time) + '.log\n')
    f.close()


def make_sub_file2(time):
    f = open('sub' + str(time) + '.sh','w')
    f.write('''#!/bin/bash
#
#SBATCH --mem 16GB
''')
    f.write('#SBATCH --output=tim_prod_again' + str(time) + '.log\n')
    f.write('''#SBATCH --time=24:00:00
#SBATCH --nodes=1
#SBATCH --gres=gpu:2
#SBATCH --job-name=timhortons_again
#SBATCH --ntasks-per-node=8
#SBATCH --account=rrg-crowley-ac

module load namd-multicore
source /home/zeldery/working/bin/activate
export RUNDIR=/dev/shm/$SLURM_JOB_ID
mkdir $RUNDIR

python /home/zeldery/projects/rrg-crowley-ac/zeldery/prod3/ani/server.py > server.log &
sleep 30s
''')
    f.write('namd2 +p8 ala_prod' + str(time) + '.conf > ala_prod' + str(time) + '.log\n')
    f.close()



def make_rest_file(i,j):
    '''Making the restrain file for NAMD simulation'''
    f = open('rest.tcl','w')
    f.write('''colvarsTrajFrequency 1000
colvar {
    name protein_com
    distance {
        group1 { atomnumbersrange 1-109 }
        group2 {  dummyAtom ( 0.000, 0.000, 0.000 )  }
    }
}

colvar {
    name end_to_end
    distance {
        group1 { atomnumbers { 7 } }
        group2 { atomnumbers { 105 } }
    }
}

colvar {
    name helicity
    alpha {
        psfSegID AP1
        residueRange 1-10
    }
}

harmonic {
  name com_rest
  colvars protein_com
  centers 0.0
  forceConstant 5
}

''')
    f.write('''harmonic {
  name end_to_end_rest
  colvars end_to_end
  forceConstant 5.0
  centers ''' + str(list_distance[i]) + '''
}''')
    f.write('''
harmonic {
  name helicity_rest
  colvars helicity
  forceConstant 500.0
  centers ''' + str(list_helix[j]) + '''
}''')
    f.close()
    
def get_info():
    '''Read the previous status from run_info.dat file'''
    f = open('run_info.dat','r')
    lines = f.readlines()
    f.close()
    n = int(lines[0][:-1])
    lst = []
    for i in range(n):
        lst.append(int(lines[i+1][:-1]))
    return lst
    
def write_info(lst):
    '''Write information to the file'''
    f = open('run_info.dat','w')
    f.write(str(len(lst)) + '\n')
    for i in range(len(lst)):
        f.write(str(lst[i]) + '\n')
    f.close()
    
def get_window():
    '''The windows that are used is stored in good_windows.txt'''
    f = open('good_windows.txt','r')
    lines = f.readlines()
    f.close()
    result = []
    for line in lines:
        temp = line.split()
        t = (int(temp[0]), int(temp[1]) )
        result.append(t)
    return result
    
def initialize():
    '''Create directory and copy necessary file'''
    write_info([0]*340)
    windows = get_window()
    for (i, j) in windows:
        name = 'windows_' + str(i) + '_' + str(j)
        os.system('mkdir ' + name)
        os.system('cp source/ala_sol.psf ' + name)
        os.system('cp source/ala_sol.pdb ' + name)
        os.system('cp source/qmmm.pdb ' + name)
        os.system('cp -r source/toppar ' + name)
        os.system('cp ../make/start_coor/' + name + '.coor ' + name)
        os.system('cp ../make/start_coor/' + name + '.xsc ' + name)
        os.chdir(name)
        os.system('mv ' + name + '.coor ala_make6.coor')
        os.system('mv ' + name + '.xsc ala_make6.xsc')
        os.chdir('..')

def run(i,j,times):
    '''Submit job'''
    name = 'windows_' + str(i) + '_' + str(j)
    os.chdir(name)
    make_conf_file(times)
    make_sub_file(times)
    if times == 0:
        make_rest_file(i,j)
    os.system('sbatch sub' + str(times) + '.sh')
    os.chdir('..')
    
def run2(i,j,times):
    name = 'windows_' + str(i) + '_' + str(j)
    os.chdir(name)
    make_conf_file(times)
    make_sub_file2(times)
    if times == 0:
        make_rest_file(i,j)
    os.system('sbatch sub' + str(times) + '.sh')
    os.chdir('..')

def check():
    '''Check the current status of the simulation
    Resubmit if the file has been run'''
    data = get_info()
    windows = get_window()
    for (i, j) in windows:
        name = 'windows_' + str(i) + '_' + str(j)
        if os.path.exists(name + '/ala_prod' + str(data[i*17+j]) +'.coor'):
            data[i*17 + j] += 1
            run(i,j, data[i*17 + j])
            print('NEW submission ' + name + ' for ' + str(data[i*17 + j]) )
        else:
            print(name + ' still running for ' + str(data[i*17 + j]) )
    write_info(data) 

def check_error():
    '''Check if the time given is not enough'''
    data = get_info()
    windows = get_window()
    for (i, j) in windows:
        name = 'windows_' + str(i) + '_' + str(j)
        f_name = name + '/tim_prod' + str(data[i*17 + j]) + '.log'
        if os.path.exists(f_name):
            if os.stat(f_name).st_size > 0:
                print(name + ' has fail for ' + str(data[i*17 + j]) + '. Resubmit with higher time')
                run2(i,j,data[i*17+j])
    
        
def first_run():
    '''Run this to submit the first step'''
    windows = get_window()
    for (i,j) in windows:
        run(i,j,0)
    










