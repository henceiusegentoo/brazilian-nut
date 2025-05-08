use pyo3::prelude::*;
use rand::rngs::StdRng;
use rand::{Rng, SeedableRng};

/// Return a vector
#[pyfunction]
fn simulation(particles: i32, steps: i32, temp: f32) -> Vec<Vec<f32>> {
    let seed: u64 = 0;
    let mut generator = StdRng::seed_from_u64(seed);
    
    // create a new vector called positions. Populate it with vectors of three dimensions that have a random number between
    // 0 and 1 for each of their indexes
    
    let mut positions: Vec<Vec<f32>> = (0..particles)
        .map(|_|{
            let lower = 0;
            let upper = 1;

            (0..3)
                .map(|_| generator.random_range(lower..=upper) as f32)
                .collect()
        })
        .collect();
    

    positions
}

/// A Python module implemented in Rust.
#[pymodule]
fn brazilian_nut_simulation(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(simulation, m)?)?;
    Ok(())
}
