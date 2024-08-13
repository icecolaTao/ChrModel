import numpy as np
import matplotlib.pyplot as plt

ntf_l = [50, 100, 200, 400, 600, 800, 1200]

# 015
crowding_rate_proto_A = [20.26, 19.63, 16.51, 12.59, 10.63, 9.26, 7.57]
crowding_rate_proto_B = [52.21, 51.78, 50.29, 42.97, 37.86, 34.46, 29.86]
crowding_rate_mep_A = [12.50, 11.01, 8.10, 4.89, 2.81, 1.57, 0.56]
crowding_rate_mep_B = [51.87, 51.28, 49.89, 41.07, 36.27, 32.57, 27.86]

x = np.arange(len(ntf_l))
ax = plt.subplot(1, 1, 1)
plt.plot(x, crowding_rate_proto_B, marker='o', markersize=5, alpha=0.8,
         linestyle='--', color='blue', label='Poff, Stable')
plt.plot(x, crowding_rate_mep_B, marker='o', markersize=5, alpha=0.8,
         linestyle='--', color='red', label='Poff, Dynamic')
plt.plot(x, crowding_rate_proto_A, marker='v', markersize=5, alpha=0.8,
         linestyle='-', color='blue', label='Pon, Stable')
plt.plot(x, crowding_rate_mep_A, marker='v', markersize=5, alpha=0.8,
         linestyle='-', color='red', label='Pon, Dynamic')
plt.xlabel('Numbers of TFs', fontproperties='Arial', size=21)
plt.xticks(x, ntf_l, fontproperties='Arial', size=19)
plt.tick_params(axis='x', length=0)
plt.ylabel('Crowding rate', fontproperties='Arial', size=21)
plt.ylim([0, 60])
Yticks = [0, 20, 40, 60]
plt.yticks(Yticks, [str(x) + "%" for x in Yticks],
           fontproperties='Arial', size=19)
ax.tick_params(axis='y', direction='in', which="major", length=5, top=True, right=True)
plt.legend(loc='center left', prop={'family': 'Arial', 'size': 17}, ncol=2, frameon=False)
# plt.title("Crowding rate of state A and B in prototype/mep model, eps=0.15",
#           fontproperties='Arial', size=21)
ax.tick_params(axis='both', direction='in')
plt.tight_layout()
plt.show()


# 030
ntf_l = [100, 200, 400, 600, 800, 1200]

crowding_rate_proto_A = [17.36, 16.38, 12.95, 10.84, 9.46, 7.69]
crowding_rate_proto_B = [45.51, 44.66, 43.79, 39.21, 35.74, 31.03]
crowding_rate_mep_A = [9.89, 8.10, 4.87, 2.61, 1.42, 0.46]
crowding_rate_mep_B = [44.10, 43.02, 42.11, 37.29, 33.67, 28.49]

x = np.arange(len(ntf_l))
ax = plt.subplot(1, 1, 1)
plt.plot(x, crowding_rate_proto_B, marker='o', markersize=5, alpha=0.8,
         linestyle='--', color='blue', label='Poff, Stable')
plt.plot(x, crowding_rate_mep_B, marker='o', markersize=5, alpha=0.8,
         linestyle='--', color='red', label='Poff, Dynamic')
plt.plot(x, crowding_rate_proto_A, marker='v', markersize=5, alpha=0.8,
         linestyle='-', color='blue', label='Pon, Stable')
plt.plot(x, crowding_rate_mep_A, marker='v', markersize=5, alpha=0.8,
         linestyle='-', color='red', label='Pon, Dynamic')
plt.xlabel('Numbers of TFs', fontproperties='Arial', size=21)
plt.xticks(x, ntf_l, fontproperties='Arial', size=19)
plt.tick_params(axis='x', length=0)
plt.ylabel('Crowding rate', fontproperties='Arial', size=21)
plt.ylim([0, 50])
yticks = [0, 10, 20, 30, 40, 50]
plt.yticks(yticks, [str(x) + "%" for x in yticks],
           fontproperties='Arial', size=19)
ax.set_yticks([20, 40], minor=True)
ax.tick_params(axis='y', direction='in', which="minor", length=4, top=True, right=True)
ax.tick_params(axis='y', direction='in', which="major", length=5, top=True, right=True)
plt.legend(loc='upper right', prop={'family': 'Arial', 'size': 17}, ncol=2, frameon=False)
# plt.title("Crowding rate of state A and B in prototype/mep model, eps=0.15",
#           fontproperties='Arial', size=21)
ax.tick_params(axis='both', direction='in')
# ax.spines['right'].set_visible(False)
# ax.spines['top'].set_visible(False)
plt.tight_layout()
plt.show()
