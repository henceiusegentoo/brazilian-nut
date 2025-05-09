from typing import Optional

from brazilian_nut_simulation import simulation # noqa | Pycharm can't look into the .so file so it fails to recognise the import and would throw an error at this point.
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
from scipy import stats
from multiprocessing import Pool

def main():
    particles = 50
    steps = 1_000_000
    temp = 1.5

    sim_count = 16

    res_all = []

    # generate sim_count seeds
    seeds = [np.random.randint(0, 2**32 - 1) for _ in range(sim_count)]
    seed_pairs = [(seeds[i], seeds[i + 1]) for i in range(0, sim_count - 1, 2)]

    if sim_count % 2 != 0:
        seed_pairs.append((seeds[-1],))

    elif sim_count <= 0:
        raise ValueError("Invalid number of simulations. Must be a positive integer.")

    for seeds in seed_pairs:
        try:
            print(f"Running simulation with seeds {seeds}" if len(seeds) > 1 else f"Running simulation with seed {seeds[0]}")
            with Pool() as pool:
                res = pool.starmap(
                    simulation_wrapper,
                    [(particles, steps, temp, seed) for seed in seeds]
                )

            res = np.concatenate(res)
            res_all.append(res)

        except KeyboardInterrupt:
            print("Simulation interrupted by user. Continuing with partial results.")
            break

    res = np.concatenate(res_all)

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

    plt.clf()

    print("Done!")

def simulation_wrapper(particles, steps, temp, seed):
    return np.array(simulation(particles, steps, temp, seed))

if __name__ == "__main__":
    main()