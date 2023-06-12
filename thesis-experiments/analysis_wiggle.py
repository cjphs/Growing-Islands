import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import patches as mpatches

files = [".0000", ".0015", ".0025", ".005", ".01", ".015", ".02", ".025", ".03"]

i = 1
for f in files:
    df = pd.read_csv(f"results/wiggle_{f[1:]}.txt")
    df.columns = ["omega", "discrepancy", "time"]

    plt.boxplot(
        df["omega"],
        positions=[i / 2],
        widths=0.5,
        medianprops={"color": "red"},
        labels=[float(f)],
        showfliers=False,
    )
    plt.boxplot(
        df["discrepancy"],
        positions=[i / 2],
        widths=0.5,
        medianprops={"color": "blue"},
        labels=[""],
        showfliers=False,
    )
    i += 1


red_patch = mpatches.Patch(color="red", label=r"$\omega$")
blu_patch = mpatches.Patch(color="blue", label=r"$\delta$")

plt.title(r"$\omega$ and $\delta$ for different vertex distortion values")
plt.legend(handles=[red_patch, blu_patch])
plt.xlabel("Tessellation vertex distortion")

plt.show()
