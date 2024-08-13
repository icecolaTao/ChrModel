import numpy as np
import matplotlib.pyplot as plt

ntf_l = [0, 100, 200, 400, 800, 1200]
p_TC = [467.7, 255.0, 226.6, 202.1, 162.4, 156.6]
m_TC = [430.5, 208.6, 177.2, 156.1, 125.1, 120.8]

p15_TC = [1092.8, 583.5, 502.3, 435.0, 344.3, 328.4]
m15_TC = [933.4, 423.4, 362.1, 310.2, 248.5, 236.6]

pTC = p15_TC
mTC = m15_TC
pSE = p15_SE
mSE = m15_SE

bar_width = 0.25
x = np.arange(len(ntf_l))

fig, ax1 = plt.subplots()
# plt.grid(axis='y', ls="--", alpha=0.5)

# Create bar charts with error bars
ax1.tick_params(which='both', direction='in')
ax1.bar(x - bar_width / 2, pTC, width=bar_width, label='Stable',
        facecolor="none", alpha=0.9, edgecolor="b", linewidth=1.5, zorder=2,
        yerr=pSE, capsize=3.5, ecolor='black')
ax1.bar(x + bar_width / 2, mTC, width=bar_width, label='Dynamic',
        color='r', alpha=0.6, edgecolor=None, zorder=2,
        yerr=mSE, capsize=3.5, ecolor='black')

# Set labels and ticks for the left y-axis
ax1.set_xlabel('Numbers of TFs', fontproperties='Arial', size=22)
ax1.set_ylabel(r'MFPT ($\tau$)', fontproperties='Arial', size=22)
ax1.set_xticks(x)
ax1.set_xticklabels(ntf_l, fontproperties='Arial', size=19)
ax1.tick_params(axis='x', length=0)
ax1.tick_params(axis='y', direction='in', length=5)
if pTC == p_TC:
    ax1.set_ylim([0, 500])
    ax1.set_yticks([100*x for x in range(6)], [100*x for x in range(6)],
                   fontproperties='Arial', size=19)
else:
    ax1.set_ylim([0, 1200])
    ax1.set_yticks([300*x for x in range(5)], [300*x for x in range(5)],
                   fontproperties='Arial', size=19)
ax1.legend(loc='upper right', prop={'family': 'Arial', 'size': 19}, frameon=False)

# Create a second y-axis on the right
ax2 = ax1.twinx()
ax2.tick_params(axis='y', direction='in', length=5)

# Calculate the difference between 'MEP model' and 'Prototype' data
difference = [m - p for m, p in zip(mTC, pTC)]

# Calculate the percentage change
percentage_change = [(d / p) * 100 if p != 0 else 0 for d, p in zip(difference, pTC)]

# Create a line chart for the percentage change
ax2.plot(x, percentage_change, linestyle=(5, (10, 3)), marker='o', markersize=6, linewidth=2,
         color='#006400', alpha=0.8)
ax2.set_ylabel(r'Time reduction percentage', color='#006400', fontproperties='Arial', size=19)
if pTC == p_TC:
    ax2.set_ylim([-25, 0])
    ax2.set_yticks([-25+5*x for x in range(6)], [str(-25+5*x)+"%" for x in range(6)],
                   fontproperties='Arial', color='#006400', size=17)
else:
    ax2.set_ylim([-30, 6])
    ax2.set_yticks([-30, -18, -6, 6], ['-30%', '-20%', '-10%', '0%'],
                   fontproperties='Arial', color='#006400', size=17)

# Add a legend for the right y-axis
ax2.legend(loc='upper left', prop={'family': 'Arial', 'size': 17}, frameon=False)

# plt.title("First passage time of state C to A, eps=0.19",
#           fontproperties='Arial', size=16)
plt.tight_layout()
# SVG
# plt.savefig('D:/Model1/Ai-0512/S-FPT015.png', dpi=600, transparent=True)
plt.show()
