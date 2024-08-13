import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter
import os

# -log(P) vs. contact p
def landscape_dx_03(tf_list, route, nsamples, nbins, thr1, thr2, thr3, thr4,
                     draw=True, smooth=False, window_size=10):
    A_B = []
    saddle1_A = []
    saddle1_B = []
    B_C = []
    saddle2_B = []
    saddle2_C = []

    color_list = ["#9503fb", "#0f15ff", "#1d8fc4", "#00bfcd", "#12e589",
                  "#1dc435", "#90d719", "#f5f20e", "#ff9f00", "#f5350f"]
    for j in range(len(tf_list)):
        d = np.array([])
        ntf = tf_list[j]
        for i in range(nsamples):
            if os.path.exists(f'{route}/{ntf}/dis{i + 1}.npy'):
                d = np.append(d, np.load(f'{route}/{ntf}/dis{i + 1}.npy'))
        d = np.array(d)
        d = d[d < 7]

        # Yield cp using tanh
        cp = 1 / 2 * (1 + np.tanh(10 * (1 - d)))

        # Generate new reaction coordinate d*
        d_star = d - 5 * cp
        hist_values, bin_edges = np.histogram(d_star, bins=nbins, density=True)

        x = bin_edges[:-1]
        index0 = np.where(hist_values == 0)  
        negative_log_prob = -np.log(hist_values)
        y = negative_log_prob
        # if len(index0[0]) > 0:  # Determines if the array is empty.
        #     hist_values = hist_values[:index0[0][0]]
        #     negative_log_prob = -np.log(hist_values)
        #     y = negative_log_prob
        #     x = x[:index0[0][0]]
        # else:
        #     negative_log_prob = -np.log(hist_values)
        #     y = negative_log_prob

        # Apply Savitzky-Golay filter to smooth the line
        if smooth:
            # if j < 5:
            #     window_size = 12
            y = savgol_filter(y, window_size, 3)

        # Find minimum and maximum values within the specified ranges
        min_range_1 = np.where(x <= thr1)
        max_range_1 = np.where((thr1 <= x) & (x <= thr2))
        min_range_2 = np.where((thr2 <= x) & (x <= thr3))
        max_range_2 = np.where((thr3 <= x) & (x <= thr4))
        min_range_3 = np.where((thr4 <= x))

        min_values_1 = np.argmin(y[min_range_1])

        y_min_org = y[min_range_1][min_values_1]
        y -= y_min_org

        if draw:
            plt.plot(x, y, label=f'{ntf}', linewidth=3, color=color_list[j])

        if draw:
            plt.scatter(x[min_range_1][min_values_1], y[min_range_1][min_values_1],
                        color='red', s=40, zorder=3)

        # Sum and -log all the p whose x < x[min_range_1][min_values_1]
        hist_values = hist_values[:len(x)]
        real_A_value = - np.log(np.sum(hist_values[x < x[min_range_1][min_values_1]])) - y_min_org

        max_values_1 = np.argmax(y[max_range_1])
        if draw:
            plt.scatter(x[max_range_1][max_values_1], y[max_range_1][max_values_1],
                        color='blue', s=40, zorder=3)

        min_values_2 = np.argmin(y[min_range_2])
        if draw and j > 3:
            plt.scatter(x[min_range_2][min_values_2], y[min_range_2][min_values_2],
                        color='red', s=40, zorder=3)

        max_values_2 = np.argmax(y[max_range_2])
        if draw and j > 3:
            plt.scatter(x[max_range_2][max_values_2], y[max_range_2][max_values_2],
                        color='blue', s=40, zorder=3)

        min_values_3 = np.argmin(y[min_range_3])
        if draw:
            plt.scatter(x[min_range_3][min_values_3], y[min_range_3][min_values_3],
                        color='red', s=40, zorder=3)

        if j > 3:
            A_B.append(real_A_value - y[min_range_2][min_values_2])  # y[min_range_1][min_values_1]
            saddle1_A.append(y[max_range_1][max_values_1] - real_A_value)
            saddle1_B.append(y[max_range_1][max_values_1] - y[min_range_2][min_values_2])
            B_C.append(y[min_range_2][min_values_2] - y[min_range_3][min_values_3])
            saddle2_B.append(y[max_range_2][max_values_2] - y[min_range_2][min_values_2])
            saddle2_C.append(y[max_range_2][max_values_2] - y[min_range_3][min_values_3])


    if draw:
        ax = plt.subplot(1, 1, 1)
        plt.xticks(fontproperties='Arial', size=18)
        plt.yticks([-4, 0, 4, 8], fontproperties='Arial', size=18)
        plt.xlabel(r'$d^{*} = d - 5 \times cp$', fontproperties='Arial', size=24)
        plt.xlim([-5, 7])
        plt.ylabel(r'Free energy ($\epsilon$)', fontproperties='Arial', size=24)
        my_font = {'family': 'Arial', 'size': 18}
        plt.legend(frameon=False, prop=my_font, ncol=2)
        ax.tick_params(axis='both', direction='in', length=6)
        # plt.title(r'Landscape of $d^{*}$ with distinct TF numbers',
        #           fontproperties='Arial', size=16)
        # full-screen SVG
        plt.show()


    return A_B, saddle1_A, saddle1_B, B_C, saddle2_B, saddle2_C

path1 = "for stable"
path2 = "for dynamic"
ntf_list = [0, 25, 50, 75, 100, 200, 400, 600, 800, 1200]

A_B, saddle1_A, saddle1_B, B_C, saddle2_B, saddle2_C = \
    landscape_dx_03(ntf_list, path1, 60, 300, -4, 0, 1.36, 2, False, True)

mA_B, msaddle1_A, msaddle1_B, mB_C, msaddle2_B, msaddle2_C = \
    landscape_dx_03(ntf_list, path2, 60, 300, -4, 0, 1.36, 2, False, True)

ntf_list = [100, 200, 400, 600, 800, 1200]
bar_width = 0.25
x = np.arange(len(ntf_list))

ax = plt.subplot(1, 1, 1)
plt.bar(x - bar_width / 2, A_B, width=bar_width, label='Stable',
        facecolor="none", alpha=0.9, edgecolor="b", linewidth=1.5, zorder=2)
plt.bar(x + bar_width / 2, mA_B, width=bar_width, label='Dynamic',
        color='r', alpha=0.6, edgecolor=None, zorder=2)
# plt.bar(x - bar_width / 2, A_B, width=bar_width, label='Stable',
#         color='b', alpha=0.6, edgecolor=None, zorder=2)  # #00CED1
# plt.bar(x + bar_width / 2 + 0.01, mA_B, width=bar_width, label='Dynamic',
#         color='r', alpha=0.6, edgecolor=None, zorder=2)  # #EE6363
plt.xlabel(r"$n_{TF}$", fontproperties='Arial', size=18)
plt.ylabel(r'Free energy ($\epsilon$)', fontproperties='Arial', size=18)
plt.xticks(x, ntf_list, fontproperties='Arial', size=18)
plt.tick_params(axis='x', length=0)
plt.yticks([-6, -4, -2, 0], fontproperties='Arial', size=18)
plt.ylim([-6, 0])
# plt.title(r'Stability contrast, A - B', fontproperties='Arial', size=16)
my_font = {'family': 'Arial', 'size': 15}
plt.legend(prop=my_font, frameon=False)
ax.tick_params(axis='y', direction='in', length=5)
plt.grid(axis="x", ls='--', alpha=0.75, linewidth=0.75)
plt.tight_layout()
# !SVG!
plt.show()


ax = plt.subplot(1, 1, 1)
plt.bar(x - bar_width / 2, saddle1_A, width=bar_width, label='Stable',
        facecolor="none", alpha=0.9, edgecolor="b", linewidth=1.5, zorder=2)
plt.bar(x + bar_width / 2, msaddle1_A, width=bar_width, label='Dynamic',
        color='r', alpha=0.6, edgecolor=None, zorder=2)
plt.xticks(x, ntf_list, fontproperties='Arial', size=18)
plt.tick_params(axis='x', length=0)
plt.yticks([0, 2, 4, 6, 8], fontproperties='Arial', size=18)
# plt.title(r'Barrier height contrast, saddle1 - B', fontproperties='Arial', size=16)
plt.grid(axis="x", ls='--', alpha=0.75, linewidth=0.75)
plt.tight_layout()
plt.show()


ax = plt.subplot(1, 1, 1)
plt.bar(x - bar_width / 2, saddle1_B, width=bar_width, label='Stable',
        facecolor="none", alpha=0.9, edgecolor="b", linewidth=1.5, zorder=2)
plt.bar(x + bar_width / 2, msaddle1_B, width=bar_width, label='Dynamic',
        color='r', alpha=0.6, edgecolor=None, zorder=2)
plt.xticks(x, ntf_list, fontproperties='Arial', size=18)
plt.tick_params(axis='x', length=0)
plt.yticks([0, 2, 4], fontproperties='Arial', size=18)
# plt.title(r'Barrier height contrast, saddle1 - B', fontproperties='Arial', size=16)
plt.grid(axis="x", ls='--', alpha=0.75, linewidth=0.75)
plt.tight_layout()
plt.show()


ax = plt.subplot(1, 1, 1)
plt.bar(x - bar_width / 2, B_C, width=bar_width, label='Stable',
        facecolor="none", alpha=0.9, edgecolor="b", linewidth=1.5, zorder=2)
plt.bar(x + bar_width / 2, mB_C, width=bar_width, label='Dynamic',
        color='r', alpha=0.6, edgecolor=None, zorder=2)
plt.xticks(x, ntf_list, fontproperties='Arial', size=18)
plt.tick_params(axis='x', length=0)
plt.yticks([-3, -2, -1, 0, 1], fontproperties='Arial', size=18)
# plt.title(r'Stability contrast, B - C', fontproperties='Arial', size=16)
plt.grid(axis="x", ls='--', alpha=0.75, linewidth=0.75)
plt.tight_layout()
ax.tick_params(axis='both', direction='in')
plt.show()


ax = plt.subplot(1, 1, 1)
plt.bar(x - bar_width / 2, saddle2_B, width=bar_width, label='Stable',
        facecolor="none", alpha=0.9, edgecolor="b", linewidth=1.5, zorder=2)
plt.bar(x + bar_width / 2, msaddle2_B, width=bar_width, label='Dynamic',
        color='r', alpha=0.6, edgecolor=None, zorder=2)
plt.xticks(x, ntf_list, fontproperties='Arial', size=18)
plt.tick_params(axis='x', length=0)
plt.yticks([0, 2, 4], fontproperties='Arial', size=18)
# plt.title(r'Barrier height contrast, saddle2 - B', fontproperties='Arial', size=16)
plt.grid(axis="x", ls='--', alpha=0.75, linewidth=0.75)
plt.tight_layout()
ax.tick_params(axis='both', direction='in')
plt.show()


ax = plt.subplot(1, 1, 1)
plt.bar(x - bar_width / 2, saddle2_C, width=bar_width, label='Stable',
        facecolor="none", alpha=0.9, edgecolor="b", linewidth=1.5, zorder=2)
plt.bar(x + bar_width / 2, msaddle2_C, width=bar_width, label='Dynamic',
        color='r', alpha=0.6, edgecolor=None, zorder=2)
plt.xticks(x, ntf_list, fontproperties='Arial', size=15)
plt.tick_params(axis='x', length=0)
plt.yticks([0, 2], fontproperties='Arial', size=15)
# plt.title(r'Barrier height contrast, saddle2 - C', fontproperties='Arial', size=16)
plt.grid(axis="x", ls='--', alpha=0.75, linewidth=0.75)
plt.tight_layout()
ax.tick_params(axis='both', direction='in')
plt.show()

