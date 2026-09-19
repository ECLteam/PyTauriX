use crate::{
    ext_mod::{manager_method_impl, plugin::Plugin, ImplManager},
    tauri_runtime::Runtime,
};
use pyo3::{exceptions::PyRuntimeError, prelude::*};
use pyo3_utils::serde::PySerde;
use tauri_plugin_cli::{self as plugin, CliExt as _};

#[pyfunction]
pub fn init() -> Plugin {
    Plugin::new(Box::new(|| Box::new(plugin::init::<Runtime>())))
}

#[pyfunction]
pub fn get_matches<'py>(py: Python<'py>, manager: ImplManager) -> PyResult<Bound<'py, PyAny>> {
    let matches = manager_method_impl!(py, &manager, [ungil], |manager| manager.cli().matches())?
        .map_err(|error| PyRuntimeError::new_err(error.to_string()))?;
    PySerde::new(matches).to_object(py)
}

#[pyfunction]
pub fn get_matches_from<'py>(
    py: Python<'py>,
    manager: ImplManager,
    args: Vec<String>,
) -> PyResult<Bound<'py, PyAny>> {
    let matches = manager_method_impl!(py, &manager, [ungil], |manager| manager
        .cli()
        .matches_from(args))?
    .map_err(|error| PyRuntimeError::new_err(error.to_string()))?;
    PySerde::new(matches).to_object(py)
}

#[pymodule(submodule, gil_used = false)]
pub mod cli {
    #[pymodule_export]
    pub use super::{get_matches, get_matches_from, init};
}
