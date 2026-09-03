use pyo3::prelude::*;
use pyo3::wrap_pyfunction;

/// Epoch 18: High-Frequency Trading Core in Rust
/// Evaluates tick data exponentially faster than Python.
#[pyfunction]
fn evaluate_tick_hft(price: f64, moving_avg: f64, threshold: f64) -> PyResult<i32> {
    if price > moving_avg + threshold {
        Ok(1) // Long Signal
    } else if price < moving_avg - threshold {
        Ok(-1) // Short Signal
    } else {
        Ok(0) // Hold
    }
}

/// A Python module implemented in Rust.
#[pymodule]
fn macro_rust_core(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(evaluate_tick_hft, m)?)?;
    Ok(())
}
