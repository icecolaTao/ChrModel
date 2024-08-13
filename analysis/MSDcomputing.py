import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import seaborn as sns
import os

eps = "155"
region = "SEG"  # TAD
count1 = 0
count2 = 0
proto_list = []
mep_list = []

for i in range(60):
    if os.path.exists(f'hpc/{eps}/msd/proto/msd_array{region}{i + 1}.npy'):
        msd_array1 = np.load(f'hpc/{eps}/msd/proto/msd_array{region}{i + 1}.npy')
        proto_list.append(msd_array1)
        count1 += 1
    if os.path.exists(f'hpc/{eps}/msd/mep/msd_array{region}{i + 1}.npy'):
        msd_array2 = np.load(f'hpc/{eps}/msd/mep/msd_array{region}{i + 1}.npy')
        mep_list.append(msd_array2)
        count2 += 1

proto_total = np.array(proto_list)
mep_total = np.array(mep_list)
x = np.arange(1, mep_total.shape[1] + 1, 1)
print(count1, count2)

ax = plt.subplot(1, 1, 1)
plt.errorbar(x, np.mean(proto_total, axis=0), yerr=np.std(proto_total, axis=0) / np.sqrt(count1),
             color='b', ecolor='b', linewidth=1.25, elinewidth=0.8, label="Stable",
             alpha=0.2, zorder=1)
plt.errorbar(x, np.mean(mep_total, axis=0), yerr=np.std(mep_total, axis=0) / np.sqrt(count2),
             color='r', ecolor='r', linewidth=1.25, elinewidth=0.8, label="Dynamic",
             alpha=0.2, zorder=3)
plt.plot(x, np.mean(mep_total, axis=0), color='r', linewidth=1.25, zorder=3)
plt.plot(x, np.mean(proto_total, axis=0), color='b', linewidth=1.25, zorder=2)
plt.xlim([0, 1000])
if eps == "155":
    plt.ylim([0, 270])
    plt.yticks([80*x for x in range(4)], [str(int(80/0.16*x)) for x in range(4)],
               fontproperties='Arial', size=15)
if eps == "03":
    plt.ylim([0, 160])
    plt.yticks([40*x for x in range(5)], [str(int(40/0.16*x)) for x in range(5)],
               fontproperties='Arial', size=15)
plt.xlabel(r"Time ($\tau$)", fontproperties='Arial', size=18)
plt.ylabel(r"MSD (${\sigma}^{2}$)", fontproperties='Arial', size=18, labelpad=-3)
plt.xticks([0, 500, 1000], fontproperties='Arial', size=15)
my_font = {'family': 'Arial', 'size': 15}
plt.legend(prop=my_font, frameon=False, loc="lower right")
ax.tick_params(axis='both', direction='in', length=5)
plt.show()


mask = (1 <= x) & (x <= 1000)
index_log = np.where(mask)[0]
proto_total = np.log10(proto_total[:, index_log])
mep_total = np.log10(mep_total[:, index_log])
x = np.log10(x[index_log])

ax = plt.subplot(1, 1, 1)
plt.errorbar(x, np.mean(mep_total, axis=0), yerr=np.std(mep_total, axis=0) / np.sqrt(count2),
             color='r', ecolor='r', linewidth=1.25, elinewidth=0.75, label="Dynamic",
             alpha=0.2, zorder=3)
plt.errorbar(x, np.mean(proto_total, axis=0), yerr=np.std(proto_total, axis=0) / np.sqrt(count1),
             color='b', ecolor='b', linewidth=1.25, elinewidth=0.75, label="Stable",
             alpha=0.2, zorder=1)

plt.plot(x, np.mean(mep_total, axis=0), color='r', linewidth=1.25, zorder=3)
plt.plot(x, np.mean(proto_total, axis=0), color='b', linewidth=1.25, zorder=2)

def my_function(z, m, n):
    return m * z + n

popt, pcov = curve_fit(my_function, x, np.mean(mep_total, axis=0))
ax.plot(x, my_function(x, *popt) + 0.1, color="k", linewidth=2)
print("alpha:", popt[0])

# linear_y2 = 0.5 * linear_x + 1
# plt.plot(linear_x, linear_y2, color="k", linewidth=2)
plt.text(0.35, 1.5, f"slope of {popt[0]:.2f}",
         fontsize=18, fontproperties='Arial', color='k')
plt.xlabel("log(Time)", fontproperties='Arial', size=18)
plt.ylabel("log(MSD)", fontproperties='Arial', size=18)
plt.xlim([0, 3])
plt.xticks([0, 1, 2, 3], fontproperties='Arial', size=15)

if eps == "155":
    plt.ylim([0.2, 2.4])
    plt.yticks([0.2, 1.2, 2.2], ["1", "2", "3"], fontproperties='Arial', size=15)
if eps == "03":
    plt.ylim([0.2, 2.4])
    plt.yticks([0.2, 1.2, 2.2], ["1", "2", "3"], fontproperties='Arial', size=15)

plt.gca().set_aspect(1)
ax.tick_params(axis='both', direction='in', length=5)
my_font = {'family': 'Arial', 'size': 15}
plt.legend(prop=my_font, frameon=False)
plt.show()
