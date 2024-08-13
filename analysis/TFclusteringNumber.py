import numpy as np
import matplotlib.pyplot as plt

ntf_l = [100, 200, 400, 600, 800, 1200]

system_C = [x * 0.009 for x in ntf_l]  # 0.011
local_C_proto03 = [2.32, 3.88, 6.51, 8.65, 10.59, 13.93]
local_C_mep03 = [2.54, 4.31, 7.46, 10.82, 13.78, 18.85]

local_C_proto15 = [3.27, 5.15, 8.01, 10.28, 12.27, 15.92]
local_C_mep15 = [3.37, 5.42, 8.66, 11.83, 14.86, 20.10]

ax = plt.subplot(1, 1, 1)
x = np.arange(len(ntf_l))
plt.plot(ntf_l, system_C, linestyle='--', linewidth=2, color='black', label=r'Average locality $n_{TF}$')
plt.plot(ntf_l, local_C_proto03, linestyle='-', linewidth=2, marker='^', markersize=7, color='b', alpha=0.85,
         label='Stable')
plt.plot(ntf_l, local_C_mep03, linestyle='-', linewidth=2, marker='^', markersize=7, color='r', alpha=0.85,
         label='Dynamic')
plt.xlabel(r"System $n_{TF}$", fontproperties='Arial', size=18)
plt.xticks([0, 400, 800, 1200], fontproperties='Arial', size=15)
plt.tick_params(axis='x', length=0)
plt.ylabel(r"E-P locality $n_{TF}$", fontproperties='Arial', size=18)
plt.ylim([0, 21])
plt.yticks([4*x for x in range(6)], fontproperties='Arial', size=15)
plt.legend(loc='upper left', prop={'family': 'Arial', 'size': 15}, frameon=False)
# plt.title("Contrast of local TF concentration around e-p complex",
#           fontproperties='Arial', size=16)
plt.tight_layout()
ax.tick_params(which='both', direction='in', length=5)
plt.show()


ax = plt.subplot(1, 1, 1)
plt.plot(ntf_l, [1 for x in range(6)], linestyle='--', linewidth=2, color='black', dashes=[8, 2])
plt.plot(ntf_l, [a / b for a, b in zip(local_C_proto03, system_C)],
linestyle='-', linewidth=2, marker='^', markersize=7, color='b', alpha=0.85,
         label='Stable')
plt.plot(ntf_l, [a / b for a, b in zip(local_C_mep03, system_C)],
linestyle='-', linewidth=2, marker='^', markersize=7, color='r', alpha=0.85,
         label='Dynamic')
plt.xlabel(r"$n_{TF}$", fontproperties='Arial', size=24)
plt.xticks([0, 400, 800, 1200], fontproperties='Arial', size=15)
plt.tick_params(axis='x', length=0)
plt.ylabel(r'TF-clustering rate', fontproperties='Arial', size=18)

plt.ylim([0, 4])
plt.yticks([0, 1, 2, 4], ['0%', '100%', '200%', '400%'],
           fontproperties='Arial', size=15)

# plt.ylim([0, 7])
# plt.yticks([2*x for x in range(4)], [str(2*x*100)+"%" for x in range(4)],
#            fontproperties='Arial', size=15)

plt.legend(loc='upper right', prop={'family': 'Arial', 'size': 17}, frameon=False)
plt.tight_layout()
ax.tick_params(which='both', direction='in', length=5)
plt.show()