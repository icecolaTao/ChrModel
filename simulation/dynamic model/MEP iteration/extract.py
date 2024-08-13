import numpy as np
import os
import random
import shutil

x = 3000
y = 3001

files_not_exist = []
files_to_copy = []

for i in range(1, 61):
    file_name = f"{i}.pdb"
    if os.path.isfile(file_name):
        files_to_copy.append(f's{i}.pdb')
        with open(f'{i}.pdb', 'r') as input_file, open(f's{i}.pdb', 'w') as output_file:
            for line in input_file:
                line_list = line.split()
                # If the first string in the line is 'MODEL' and the second string matches the target string
                if line_list[0] == 'MODEL' and line_list[1] == f'{x}':
                    output_file.write(line)
                    for next_line in input_file:
                        next_line_list = next_line.split()
                        if next_line_list[0] == 'MODEL' and next_line_list[1] == f'{y}':
                            break
                        output_file.write(next_line)
                    break
    else:
        file_name2 = f"s{i}.pdb"
        files_not_exist.append(file_name2)

print(files_not_exist, len(files_not_exist))

if len(files_not_exist) > 0:
    files_to_copy_selected = random.choices(files_to_copy, k=len(files_not_exist))
    # random.sample(files_to_copy, len(files_to_delete)) /// random.choices(files_to_copy, k=len(files_to_delete))

    # Copy and rename the selected files to match the names of the deleted files
    for old_file_name, new_file_name in zip(files_not_exist, files_to_copy_selected):
        old_file_path = new_file_name
        new_file_path = old_file_name
        shutil.copy2(old_file_path, new_file_path)




