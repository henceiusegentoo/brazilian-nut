use pyo3::prelude::*;
use rand::rngs::StdRng;
use rand::{Rng, SeedableRng};

#[pyfunction]
fn simulation(particles: i32, steps: i32, temp: f64, seed: u64) -> Vec<f64> {
    let mut generator = StdRng::seed_from_u64(seed);

    let mut positions: Vec<Vec<f64>> = (0..particles)
        .map(|_| {
            let lower = 0.0;
            let upper = 1.0;

            (0..3)
                .map(|_| generator.random_range(lower..upper) as f64)
                .collect()
        })
        .collect();

    let g = 1.0;
    let m = 1.0;

    let mut energy: f64 = calculate_energy(&positions, g, m);

    let mut positions_all: Vec<Vec<Vec<f64>>> =
        vec![vec![vec![0.0; 3]; particles as usize]; steps as usize];

    for step in 0..steps {
        positions_all[step as usize] = positions.clone();

        let new_positions: Vec<Vec<f64>> = positions
            .clone()
            .into_iter()
            .map(|pos| {
                let lower = -0.02;
                let upper = 0.02;

                pos.into_iter()
                    .map(|pos| pos + generator.random_range(lower..=upper) as f64)
                    .collect()
            })
            .collect();

        let new_energy: f64;

        if new_positions
            .iter()
            .any(|pos| pos[2] < 0.0)
        {
            new_energy = f64::INFINITY;
        } else {
            new_energy = calculate_energy(&new_positions, g, m);
        }

        if f64::exp(-(new_energy - energy) / temp) > 1.0 - generator.random_range(0.0..1.0) {
            positions = new_positions;
            energy = new_energy;
        }
    }
    
    let flattened_positions: Vec<Vec<f64>> =
        positions_all
            .into_iter()
            .flat_map(|step| step.into_iter().collect::<Vec<Vec<f64>>>())
            .collect();
    
    let z_coordinates: Vec<f64> = flattened_positions
        .into_iter()
        .map(|pos| pos[2])
        .collect();
    
    z_coordinates
}

fn calculate_energy(positions: &Vec<Vec<f64>>, g: f64, m: f64) -> f64 {
    positions
        .into_iter()
        .map(|pos: &Vec<f64>| pos[2])
        .sum::<f64>()
        * g
        * m
}

#[pymodule]
fn brazilian_nut_simulation(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(simulation, m)?)?;
    Ok(())
}
