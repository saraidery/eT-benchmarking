import re
import numpy as np
import os

def extract_timing_disco(timing_file, search_string):
#
#   Collect a single timing from timing_file
#   For 1.4 and earlier
#
    wall = []
    cpu = []
    with open(timing_file) as f:
        for line in f:
            if search_string in line:
                #read wall time
                nextLine = next(f)
                if "wall time" in nextLine:
                    time_string = nextLine.split(':')[1]
                    time = float(time_string)
                    wall.append(time)

                    #read cpu time
                    nextLine = next(f)
                    time_string = nextLine.split(':')[1]
                    time = float(time_string)
                    cpu.append(time)
    return wall, cpu


def get_calculation_summary(timing_file, search_strings):
#
#   Get full summary of single calculation (timing_file)
#   Will try to extract timings for all the strings in
#   search_strings
#
#   Currently always calls the Disco extractor
#
    search_matches_wall = []
    search_matches_cpu = []

    for string in search_strings:
        wall, cpu = extract_timing_disco(timing_file, string)
        if (wall and cpu):
           search_matches_wall.append(wall[0])
           search_matches_cpu.append(cpu[0])
        else:
           search_matches_wall.append(-1.00)
           search_matches_cpu.append(-1.00)

    return search_matches_wall, search_matches_cpu


def get_data_for_molecule(molecule, basis, folder, search_strings, methods, timing_file):
#
#   Collects the data for all methods
#   for a given molecule and basis set
#
    data_cpu = np.zeros(len(search_strings))
    data_wall = np.zeros(len(search_strings))

    for i , method in enumerate(methods):
        full_path = os.path.join(os.path.join(folder, method), timing_file)
        wall, cpu = get_calculation_summary(full_path, search_strings)

        if (wall and cpu):
            if (i==0):
                data_wall = np.array(wall)
                data_cpu = np.array(cpu)
            else:
                data_wall = np.vstack((data_wall,np.array(wall)))
                data_cpu = np.vstack((data_cpu,np.array(cpu)))
    return np.transpose(data_wall), np.transpose(data_cpu)

def print_latex_table(search_strings, methods, data_wall, data_cpu, caption, summary_file):
#
#   Prints a latex table (requres the booktabs package)
#
    f = open(summary_file, "a")

    s = "c"
    n = 2*len(methods)
    format_ = "".join([char*n for char in s])
    f.write(r"\begin{table}" + "\n")
    f.write(r"\caption{" + caption + "}" + "\n")
    f.write(r"\begin{tabular}{l" + format_ + "}" + "\n")
    f.write(r"\toprule" + "\n")
    f.write("Task")
    for method in methods:
        f.write(" & \multicolumn{2}{c}{" + method + "}")
    f.write(r'\\' + "\n")
    first=2
    last=3
    for method in methods:
        f.write(r"\cmidrule(lr){" + str(first) + "-" + str(last) + "}")
        first = last + 1
        last = first + 1
    f.write("\n")
    for method in methods:
        f.write(" & cpu & wall")
    f.write(r'\\' + "\n")
    f.write(r"\midrule" + "\n")
    for i, string in enumerate(search_strings):
        f.write(string)
        for j, method in enumerate(methods):
            wall_string = format_time(data_wall[i,j])
            cpu_string= format_time(data_cpu[i,j])
            f.write(" & " + cpu_string + " & " + wall_string)
        f.write(r'\\' + "\n")
    f.write(r"\bottomrule" + "\n")
    f.write(r"\end{tabular}" + "\n")
    f.write(r"\end{table}" + "\n")

def print_latex_header(file, title):
    f = open(file, "w") # should be .tex
    f.write(r"\documentclass{article}" + "\n")
    f.write(r"\usepackage[landscape]{geometry}" + "\n")
    f.write(r"\usepackage[utf8]{inputenc}" + "\n")
    f.write(r"\usepackage{booktabs}" + "\n")
    f.write(r"\usepackage{multicol}" + "\n")
    f.write(r"\title{" + title + "}" + "\n")
    f.write(r"\date{\today}" + "\n")
    f.write(r"\begin{document}" + "\n")
    f.write(r"\maketitle" + "\n")
    f.close()

def print_latex_footer(file):
    f = open(file, "a") # should be .tex
    f.write(r"\end{document}" + "\n")
    f.close()

def format_time(time):
    if (time > 7200):
        string = "{:.2f}".format(time/3600) + " h"
    elif (time > 120):
        string = "{:.2f}".format(time/60) + " min"
    elif (time == -1.00):
        string = "--"
    else:
        string = "{:.2f}".format(time) + " s"

    return string

def get_summary(folder, summary_file, title, timings_file_name):

    print_latex_header(summary_file, title)
    molecules = os.listdir(folder)

    search_strings = ['SCF solver',
                      'Cholesky decomposition of ERIs',
                      'CC GS solver time',
                      'multipliers',
                      'excited state (right)',
                      'excited state (left)',
                      'Time to calculate EOM properties',
    ]

    for molecule in molecules:
        molecule_folder = os.path.join(folder, molecule)
        bases = os.listdir(molecule_folder)
        for basis in sorted(bases):
            basis_folder = os.path.join(molecule_folder, basis)
            methods = sorted(os.listdir(basis_folder))

            data_wall_t, data_cpu_t = get_data_for_molecule(molecule, basis, basis_folder, search_strings, methods, timings_file_name)
            print_latex_table(search_strings, methods, data_wall_t, data_cpu_t, molecule + " " + basis, summary_file)

    print_latex_footer(summary_file)

get_summary("disco", "disco.tex", "Disco timing benchmark on (small) bigmem nodes on Saga", "eT.timing.out")
