import os
import random
import shutil


# List to store the names of files that don't meet the size criteria
files_to_delete = []

# List to store the names of files that meet the size criteria
files_to_copy = []

# Iterate over the files in the directory
for i in range(1, 61):
    file_name = f"{i}.pdb"
    file_path = file_name
    if os.path.isfile(file_path):
        # Check the file size
        file_size = os.path.getsize(file_path) / (1024 * 1024)  # Convert to MB
        print(file_size)

        if 120.72 <= file_size <= 121:
            files_to_copy.append(file_name)
        else:
            files_to_delete.append(file_name)
            os.remove(file_path)
    else:
        files_to_delete.append(file_name)

print(files_to_copy, len(files_to_copy))

# if len(files_to_delete) > 0:
#     # Randomly select files to copy from the files that meet the size criteria
#     files_to_copy_selected = random.choices(files_to_copy, k=len(files_to_delete))
#     # random.sample(files_to_copy, len(files_to_delete)) /// random.choices(files_to_copy, k=len(files_to_delete))

#     # Copy and rename the selected files to match the names of the deleted files
#     for old_file_name, new_file_name in zip(files_to_delete, files_to_copy_selected):
#         old_file_path = os.path.join(directory, new_file_name)
#         new_file_path = os.path.join(directory, old_file_name)
#         shutil.copy2(old_file_path, new_file_path)
