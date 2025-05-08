from brazilian_nut_simulation import simulation # noqa | Pycharm can't look into the .so file so it fails to recognise the import and would throw an error at this point.
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
from scipy import stats

def main():
    particles = 50
    steps = 1_000_000
    temp = 1.5
    seed = 0

    res = np.array(simulation(
        particles=particles,
        steps=steps,
        temp=temp,
        seed=seed
    ))

    loc, scale = stats.expon.fit(res)

    plt.hist(
        res,
        density=True,
        label=rf"mc routine ($T = {temp:.2f}$)",
        zorder=6,
        alpha=0.6,
        edgecolor="black",
        color="magenta"
    )

    z_continuous = np.linspace(res.min(), res.max(), 10_000)

    plt.plot(
        z_continuous,
        np.exp(-(z_continuous - loc) / scale) / scale,
        linestyle="--",
        color="black",
        label=rf"exponential fit ($T = {scale:.2f}$)",
        zorder=7
    )

    plt.xlabel("Distance")
    plt.ylabel("Density")
    plt.title(r"Brazilian nut simulation")
    plt.legend()
    plt.grid()
    plt.yscale("log")

    plt.savefig("brazilian_nut_simulation.png", dpi=300)


if __name__ == "__main__":
    main()