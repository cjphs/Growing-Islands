import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import patches as mpatches

files = ["02", "025", "03", "035"]
files = [".015", ".02", ".0225", ".025", ".0275", ".03", ".035", ".04", ".045"]


i = 1
for f in files:
    df = pd.read_csv(f"results/results_{f[1:]}_150.txt")
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
        labels=[float(f)],
    )
    plt.boxplot(
        df["discrepancy"],
        positions=[i / 2],
        widths=0.5,
        medianprops={"color": "blue"},
        labels=[""],
    )
    i += 1


red_patch = mpatches.Patch(color="red", label="Omega")
blu_patch = mpatches.Patch(color="blue", label="Area discrepancy")

plt.legend(handles=[red_patch, blu_patch])
plt.xlabel("Phi")

plt.show()
