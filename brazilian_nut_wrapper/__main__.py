from brazilian_nut_simulation import simulation # noqa | Pycharm can't look into the .so file so it fails to recognise the import and would throw an error at this point.

def main():
    particles = 50
    steps = 1_000_000
    temp = 1.5
    seed = 0

    res = simulation(
        particles=particles,
        steps=steps,
        temp=temp,
        seed=seed
    )

    print(f"Simulation finished with {particles} particles, {steps} steps, and temperature {temp}.")

if __name__ == "__main__":
    main()