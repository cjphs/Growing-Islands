import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import patches as mpatches

files = ["02", "025", "03", "035"]
files = [".015", ".02", ".0225", ".025", ".0275", ".03", ".035", ".04", ".045"]
files = [
    ".005",
    ".01",
    ".015",
    ".02",
    ".025",
    ".03",
    ".045",
    ".05",
]


i = 1
for f in files:
    df = pd.read_csv(f"results/results_{f[1:]}_50.txt")
    df.columns = ["omega", "discrepancy", "time"]

    print(df)
    df.describe()

    print(f"mean omega: {df['omega'].mean()}, best omega: {df['omega'].max()}")
    print(
        f"mean discrepancy: {df['discrepancy'].mean()}, best discrepancy: {df['discrepancy'].min()}"
    )
    # print(f"{df['omega'].describe()}")
    # print(f"{df['discrepancy'].describe()}")

    plt.boxplot(
        df["omega"],
        positions=[i / 2],
        widths=0.5,
        medianprops={"color": "red"},
        showfliers=False,
        labels=[float(f)],
    )
    plt.boxplot(
        df["discrepancy"],
        positions=[i / 2],
        widths=0.5,
        medianprops={"color": "blue"},
        showfliers=False,
        labels=[""],
    )
    i += 1


red_patch = mpatches.Patch(color="red", label=r"$\omega$")
blu_patch = mpatches.Patch(color="blue", label=r"$\delta$")

plt.legend(handles=[red_patch, blu_patch])
plt.xlabel(r"$\phi$")

plt.title(
    r"$\omega$ and $\delta$ for different values of $\phi$ on 100 randomly-generated Voronoi tessellations"
)
plt.show()


import warnings

warnings.filterwarnings("ignore")

prev_x = None
prev_y = None

j = 0
for f in files:
    df = pd.read_csv(f"results/results_{f[1:]}_50.txt")
    df.columns = ["omega", "discrepancy", "time"]

    # convert all items of df["time"] to float
    for i in range(len(df["time"])):
        df["time"][i] = float(df["time"][i].split(":")[-1])

    print(df["time"].mean())

    x = df["discrepancy"].median()
    y = df["time"].median()

    if prev_x is not None:
        plt.plot([prev_x, x], [prev_y, y], color="black", linewidth=0.5)

    prev_x, prev_y = x, y

    plt.scatter(x, y, color="black")

    if j == 0:
        t = r"$\phi = $" + f"{float(f)}"
    else:
        t = rf"{float(f)}"

    print(j, t)

    plt.text(
        x,
        y + 0.08,
        t,
        fontsize=13,
        horizontalalignment="center",
    )

    plt.title(r"Trajectory of median values depending on $\phi$")
    plt.xlabel(r"median area discrepancy ($\delta$)")
    plt.ylabel("median time (s)")

    j += 1

plt.show()
