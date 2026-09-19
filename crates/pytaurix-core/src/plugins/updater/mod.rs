use std::{
    error::Error,
    fmt::{Debug, Display, Formatter},
};

use pyo3::{
    exceptions::PyRuntimeError,
    prelude::*,
    types::{PyAny, PyDict},
};
use pyo3_utils::from_py_dict::{derive_from_py_dict, FromPyDict as _};
use pyo3_utils::serde::PySerde;
use tauri_plugin_updater::{self as plugin, UpdaterExt as _};

use crate::{
    ext_mod::{manager_method_impl, plugin::Plugin, ImplManager},
    utils::TauriError,
};

#[derive(Debug)]
struct PluginError(plugin::Error);

impl Display for PluginError {
    fn fmt(&self, f: &mut Formatter<'_>) -> std::fmt::Result {
        Display::fmt(&self.0, f)
    }
}

impl Error for PluginError {}

impl From<PluginError> for PyErr {
    fn from(value: PluginError) -> Self {
        match value.0 {
            plugin::Error::Tauri(e) => TauriError::from(e).into(),
            plugin::Error::Io(e) => e.into(),
            e @ (plugin::Error::EmptyEndpoints
                | plugin::Error::Semver(_)
                | plugin::Error::Serialization(_)
                | plugin::Error::ReleaseNotFound
                | plugin::Error::UnsupportedArch
                | plugin::Error::UnsupportedOs
                | plugin::Error::FailedToDetermineExtractPath
                | plugin::Error::UrlParse(_)
                | plugin::Error::Reqwest(_)
                | plugin::Error::TargetNotFound(_)
                | plugin::Error::Network(_)
                | plugin::Error::Minisign(_)
                | plugin::Error::Base64(_)
                | plugin::Error::SignatureUtf8(_)
                | plugin::Error::TempDirNotOnSameMountPoint
                | plugin::Error::BinaryNotFoundInArchive
                | plugin::Error::TempDirNotFound
                | plugin::Error::AuthenticationFailed
                | plugin::Error::DebInstallFailed
                | plugin::Error::InvalidUpdaterFormat
                | plugin::Error::Http(_)
                | plugin::Error::InvalidHeaderValue(_)
                | plugin::Error::InvalidHeaderName(_)
                | plugin::Error::FormatDate
                | plugin::Error::InsecureTransportProtocol) => {
                PyRuntimeError::new_err(e.to_string())
            }
            #[cfg(target_os = "windows")]
            e @ plugin::Error::Extract(_) => PyRuntimeError::new_err(e.to_string()),
            non_exhaustive => PyRuntimeError::new_err(format!(
                "Unimplemented plugin error, please report this to the pytaurix developers: {non_exhaustive}"
            )),
        }
    }
}

impl From<plugin::Error> for PluginError {
    fn from(value: plugin::Error) -> Self {
        Self(value)
    }
}

/// See also: [tauri_plugin_updater::Builder]
#[non_exhaustive]
pub struct BuilderArgs {}

derive_from_py_dict!(BuilderArgs {});

impl BuilderArgs {
    fn from_kwargs(kwargs: Option<&Bound<'_, PyDict>>) -> PyResult<Option<Self>> {
        kwargs.map(Self::from_py_dict).transpose()
    }

    fn apply_to_builder(self, builder: plugin::Builder) -> plugin::Builder {
        let Self {} = self;
        builder
    }
}

/// See also: [tauri_plugin_updater::Builder]
#[pyclass(frozen)]
#[non_exhaustive]
pub struct Builder;

#[pymethods]
impl Builder {
    #[staticmethod]
    #[pyo3(signature = (**kwargs))]
    fn build(kwargs: Option<&Bound<'_, PyDict>>) -> PyResult<Plugin> {
        let args = BuilderArgs::from_kwargs(kwargs)?;

        let mut builder = plugin::Builder::new();
        if let Some(args) = args {
            builder = args.apply_to_builder(builder);
        }

        let plugin = Plugin::new(Box::new(move || Box::new(builder.build())));
        Ok(plugin)
    }
}

fn update_metadata<'py>(py: Python<'py>, update: plugin::Update) -> PyResult<Bound<'py, PyDict>> {
    let metadata = PyDict::new(py);
    metadata.set_item("body", update.body)?;
    metadata.set_item("current_version", update.current_version)?;
    metadata.set_item("version", update.version)?;
    metadata.set_item("date", update.date.map(|date| date.to_string()))?;
    metadata.set_item("target", update.target)?;
    metadata.set_item("download_url", update.download_url.to_string())?;
    metadata.set_item("signature", update.signature)?;
    metadata.set_item("raw_json", PySerde::new(update.raw_json).to_object(py)?)?;
    Ok(metadata)
}

/// Check configured updater endpoints without downloading or installing an update.
///
/// Passing `endpoints` is useful for controlled tests and temporary release channels.
/// Production applications should configure endpoints in `tauri.conf.json` instead.
#[pyfunction(signature = (manager, *, endpoints=None))]
pub fn check<'py>(
    py: Python<'py>,
    manager: ImplManager,
    endpoints: Option<Vec<String>>,
) -> PyResult<Option<Bound<'py, PyAny>>> {
    let endpoints = endpoints
        .map(|endpoints| {
            endpoints
                .into_iter()
                .map(|endpoint| {
                    endpoint.parse::<tauri::Url>().map_err(|error| {
                        PyRuntimeError::new_err(format!("invalid updater endpoint: {error}"))
                    })
                })
                .collect::<PyResult<Vec<_>>>()
        })
        .transpose()?;

    let builder = manager_method_impl!(py, &manager, [ungil], |manager| manager.updater_builder())?;
    let update = py.detach(move || {
        let updater = match endpoints {
            Some(endpoints) => builder.endpoints(endpoints)?.build()?,
            None => builder.build()?,
        };
        tauri::async_runtime::block_on(updater.check())
    });
    let update = update.map_err(PluginError::from)?;

    update
        .map(|update| update_metadata(py, update).map(Bound::into_any))
        .transpose()
}

/// See also: [tauri_plugin_updater]
#[pymodule(submodule, gil_used = false)]
pub mod updater {
    #[pymodule_export]
    pub use super::Builder;

    #[pymodule_export]
    pub use super::check;

    pub use super::BuilderArgs;
}
