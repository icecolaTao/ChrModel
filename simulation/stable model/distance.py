# plot contact probability - genomic distance
import numpy as np

fn=1  # for shell script to change
nTF=0 # for shell script to change
index = [1]
tab = [20000, 40000]
temp1 = []

with open(f'{fn}.pdb') as file:
    # Divided into groups
    for j in index:
        # For each configuration
        for i in range(tab[j-1], tab[j]):
            target_string = '{}'.format(i)
            data = []
            # Begin scanning
            for line in file:
                line_list = line.split()
                # If the first string in the line is 'MODEL' and the second string matches the target string
                if line_list[0] == 'MODEL' and line_list[1] == target_string:
                    print('find model {}'.format(i))
                    # Loop through each subsequent line until 'TER' is reached,and break the loop once find a model
                    for next_line in file:
                        next_line_list = next_line.split()
                        # If 'TER' is reached, break out of the loop
                        if next_line_list[0] == 'TER':
                            break
                        # Otherwise, extract columns 6, 7, and 8 and convert them to floats
                        row = [float(next_line_list[i]) for i in range(5, 8)]
                        # Append the row to the data list
                        data.append(row)
                    # Convert the data list to a numpy array
                    data_array = np.array(data)
                    # Delete the first and last 100 rows
                    data_array = data_array[100:-nTF-100, :]
                    # Because the unit of pdb file, 10^-10, is 10 times as much as the one in top file
                    data_array /= 10
                    # Compute Euclid distance
                    n1 = data_array.reshape(333, 1, 3)
                    n2 = data_array.reshape(1, 333, 3)
                    n3 = np.sqrt(np.sum((n1 - n2) ** 2, axis=2))
                    temp1.append(n3[145, 185])
                    break
        temp2 = np.array(temp1)
        np.save(f'dis{fn}.npy', temp2)

