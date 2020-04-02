# ---------------------------------------------------------
# Create by: Tu Nguyen Thien Phuc
# Research group: Rowley group https://www.rowleygroup.net/
# Github: github.com/zeldery
# ---------------------------------------------------------
# The script to extract the energy from single-point 
# calculation and tabulate it.
# ---------------------------------------------------------


import os


# The script to extract the energy from ORCA single energy point
list_folder = ['windows_0_6', 'windows_3_13', 'windows_18_3']
for file in list_folder:
    total = []
    disp = []
    os.chdir(file)
    for num in range(50): # Change to fit the naming system
        f = open(str(num*5) + '.log','r') # Change here too
        lines = f.readlines()
        f.close()
        for line in lines:
            line = line.split()
            if len(line) == 0:
                continue
            if line[0] == 'FINAL':
                total.append(float(line[4]))
            elif line[0] == 'Dispersion':
                disp.append(float(line[2]))
        print(file + ' ' + str(num))
    os.chdir('..')    
    f = open(file + '.dat' , 'w') # Change extension, if wanted
    f.write('Total,Dispersion\n')
    for i in range(len(total)):
        f.write(str(total[i]) + ',' + str(disp[i]) + '\n')
    f.close()
    
# Extract the energy of QM part from NAMD simulation output
list_file = ['windows_0_6','windows_3_13','windows_18_3']
for file in list_file:
    time = []
    potential = []
    f = open(file + '.log','r')
    lines = f.readlines()
    f.close()
    j = -2 # Skip the energy from minimization part
           # Change it if necessary
    for line in lines:
        temp = line.split()
        if len(temp) == 0:
            continue
        if temp[0] == 'QMENERGY:':
            j += 1
            if j == 1000:
                j = 0
                time.append(temp[1])
                potential.append(float(temp[3]))
    f = open(file + '.txt','w') # Change the extension, if want
    f.write('Time,Energy\n')
    for i in range(len(time)):
        f.write(time[i] + ',' + str(potential[i]) + '\n')
    f.close()
    
