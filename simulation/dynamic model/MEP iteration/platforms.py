# extract contact matrices and save them in an integrated-vectors form
import numpy as np
from scipy.io import savemat

y=1

tab = [1000, 3000]

for fn in [y]:
    data_arrays = np.zeros((tab[1] - tab[0], 27584))
    with open(f'{fn}.pdb') as file:
        # For each configuration
        for i in range(tab[0], tab[1]):
            target_string = '{}'.format(i)
            data = []
            # Begin scanning
            for line in file:
                line_list = line.split()
                # If the first string in the line is 'MODEL' and the second string matches the target string
                if line_list[0] == 'MODEL' and line_list[1] == target_string:
                    # print('find model {}'.format(i))
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
                    data_array = data_array[100: - 100, :]
                    # Because the unit of pdb file, 10^-10, is 10 times as much as the one in top file
                    data_array /= 10
                    # Compute Euclid distance
                    n1 = data_array.reshape(333, 1, 3)
                    n2 = data_array.reshape(1, 333, 3)
                    n3 = np.sqrt(np.sum((n1 - n2) ** 2, axis=2))
                    # Construct the probability matrix
                    n4 = 0.5 * (1 + np.tanh(10 * (1 - n3)))
                    # Convert to vector whose elements are from upper triangular of above
                    lv = []
                    for a in range(333):
                        for b in range(a + 1, 333):
                            if a in [142, 143, 144, 145, 146, 147, 148] and b in [182, 183, 184, 185, 186, 187, 188]:
                                lv.append(n4[a, b])
                            elif b % 2 == 1:
                                lv.append(n4[a, b])
                    n5 = np.array(lv)
                    data_arrays[i - tab[0]] = n5
                    break
    if fn == 1:
        print(data_arrays, len(lv))
    assert np.any(data_arrays != 0)
    savemat(f"data_arrays{fn}.mat", {'da': data_arrays})


