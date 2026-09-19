use std::{fmt::Display, sync::Arc};

use pyo3::{exceptions::PyRuntimeError, prelude::*};
use pyo3_utils::serde::PySerde;
use tauri_plugin_store::{self as plugin, StoreExt as _};

use crate::{
    ext_mod::{manager_method_impl, plugin::Plugin, ImplManager},
    tauri_runtime::Runtime,
};

/// See also: [tauri_plugin_store::Builder].
#[pyfunction]
pub fn init() -> Plugin {
    Plugin::new(Box::new(|| Box::new(plugin::Builder::new().build())))
}

fn store_error(error: impl Display) -> PyErr {
    PyRuntimeError::new_err(error.to_string())
}

#[pyclass(frozen)]
pub struct Store(Arc<plugin::Store<Runtime>>);

#[pymethods]
impl Store {
    fn get<'py>(&self, py: Python<'py>, key: &str) -> PyResult<Option<Bound<'py, PyAny>>> {
        self.0
            .get(key)
            .map(|value| PySerde::new(value).to_object(py))
            .transpose()
    }

    fn set(&self, key: String, value: PySerde<plugin::JsonValue>) {
        self.0.set(key, value.into_inner());
    }

    fn has(&self, key: &str) -> bool {
        self.0.has(key)
    }
    fn delete(&self, key: &str) -> bool {
        self.0.delete(key)
    }
    fn clear(&self) {
        self.0.clear()
    }
    fn keys(&self) -> Vec<String> {
        self.0.keys()
    }

    fn entries<'py>(&self, py: Python<'py>) -> PyResult<Bound<'py, PyAny>> {
        PySerde::new(self.0.entries()).to_object(py)
    }

    fn save(&self) -> PyResult<()> {
        self.0.save().map_err(store_error)
    }
    fn reload(&self) -> PyResult<()> {
        self.0.reload().map_err(store_error)
    }
    fn reload_ignore_defaults(&self) -> PyResult<()> {
        self.0.reload_ignore_defaults().map_err(store_error)
    }
}

#[pyfunction]
pub fn load(py: Python<'_>, manager: ImplManager, path: &str) -> PyResult<Store> {
    manager_method_impl!(py, &manager, [ungil], |manager| {
        manager.store(path).map(Store).map_err(store_error)
    })?
}

#[pymodule(submodule, gil_used = false)]
pub mod store {
    #[pymodule_export]
    pub use super::init;
    #[pymodule_export]
    pub use super::{load, Store};
}
