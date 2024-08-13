# Initialize the coordinate using the conformation from last simulation
import numpy as np

ini_config = [3000]  # sorted(np.random.randint(low=5000, high=6000, size=1).tolist())
y=1
nTF=0
a = 100
data = []
with open(f's{y}.pdb') as file:
    # For each ini_config
    for x in ini_config:
        # Begin scanning
        for line in file:
            line_list = line.split()
            # If the first string in the line is 'MODEL' and the second string matches the target string
            if line_list[0] == 'MODEL' and line_list[1] == f'{x}':
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
                # !10!
                data_array /= 10
                # Translate
                data_array[:, 0] -= np.min(data_array[:, 0]) - 40
                data_array[:, 1] -= np.min(data_array[:, 1]) - 40
                data_array[:, 2] -= np.min(data_array[:, 2]) - 40
                break

        string = f'MD of coarse-grained beads\n{533 + nTF:>5}\n'

        for i in range(1, 534):
            if i < 101:
                string += "{:>5}{:>5}{:>5}{:>5}{:>8.3f}{:>8.3f}{:>8.3f}\n".format(
                    i, 'ASN', 'OB', i, data_array[i - 1][0], data_array[i - 1][1], data_array[i - 1][2])
            elif i == 246:
                string += "{:>5}{:>5}{:>5}{:>5}{:>8.3f}{:>8.3f}{:>8.3f}\n".format(
                    i, 'ASN', 'EN', i, data_array[i - 1][0], data_array[i - 1][1], data_array[i - 1][2])
                e1 = data_array[i - 1][0]
                e2 = data_array[i - 1][1]
                e3 = data_array[i - 1][2]
            elif i == 286:
                string += "{:>5}{:>5}{:>5}{:>5}{:>8.3f}{:>8.3f}{:>8.3f}\n".format(
                    i, 'ASN', 'PR', i, data_array[i - 1][0], data_array[i - 1][1], data_array[i - 1][2])
                p1 = data_array[i - 1][0]
                p2 = data_array[i - 1][1]
                p3 = data_array[i - 1][2]
            elif i > 433:
                string += "{:>5}{:>5}{:>5}{:>5}{:>8.3f}{:>8.3f}{:>8.3f}\n".format(
                    i, 'ASN', 'OB', i, data_array[i - 1][0], data_array[i - 1][1], data_array[i - 1][2])
            else:
                string += "{:>5}{:>5}{:>5}{:>5}{:>8.3f}{:>8.3f}{:>8.3f}\n".format(
                    i, 'ASN', 'NB', i, data_array[i - 1][0], data_array[i - 1][1], data_array[i - 1][2])

        for i in range(534, 534 + nTF):
            q = np.random.normal((e1 + p1)/2, 3)
            w = np.random.normal((e2 + p2)/2, 3)
            e = np.random.normal((e3 + p3)/2, 3)
            string += "{:>5}{:>5}{:>5}{:>5}{:>8.3f}{:>8.3f}{:>8.3f}\n".format(
                i, 'ASN', 'TF', i, q, w, e)

        string += f'{a:<10.5f}{a:<10.5f}{a:<10.5f}'

with open(f'{y}.gro', 'w') as f:
    f.write(string)





