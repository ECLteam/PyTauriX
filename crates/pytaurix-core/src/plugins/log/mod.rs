use std::str::FromStr;

use pyo3::{exceptions::PyValueError, prelude::*, types::PyDict};
use pyo3_utils::from_py_dict::{derive_from_py_dict, FromPyDict as _, NotRequired};
use tauri_plugin_log::{self as plugin, log::LevelFilter, Target, TargetKind};

use crate::ext_mod::plugin::Plugin;

#[non_exhaustive]
pub struct BuilderArgs {
    level: NotRequired<String>,
    targets: NotRequired<Vec<String>>,
    file_name: NotRequired<String>,
    clear_targets: bool,
}

derive_from_py_dict!(BuilderArgs {
    #[pyo3(default)]
    level,
    #[pyo3(default)]
    targets,
    #[pyo3(default)]
    file_name,
    #[pyo3(default)]
    clear_targets,
});

impl BuilderArgs {
    fn from_kwargs(kwargs: Option<&Bound<'_, PyDict>>) -> PyResult<Option<Self>> {
        kwargs.map(Self::from_py_dict).transpose()
    }
}

#[pyclass(frozen)]
#[non_exhaustive]
pub struct Builder;

#[pymethods]
impl Builder {
    #[staticmethod]
    #[pyo3(signature = (**kwargs))]
    fn build(kwargs: Option<&Bound<'_, PyDict>>) -> PyResult<Plugin> {
        let args = BuilderArgs::from_kwargs(kwargs)?;
        let (level, targets, file_name, clear_targets) = match args {
            Some(args) => (
                args.level.0,
                args.targets.0,
                args.file_name.0,
                args.clear_targets,
            ),
            None => (None, None, None, false),
        };
        let level = level
            .map(|level| {
                LevelFilter::from_str(&level).map_err(|_| {
                    PyValueError::new_err(
                        "level must be one of: off, error, warn, info, debug, trace",
                    )
                })
            })
            .transpose()?;
        if let Some(targets) = &targets {
            if targets.iter().any(|target| {
                !matches!(target.as_str(), "stdout" | "stderr" | "log_dir" | "webview")
            }) {
                return Err(PyValueError::new_err(
                    "targets may contain only: stdout, stderr, log_dir, webview",
                ));
            }
        }

        Ok(Plugin::new(Box::new(move || {
            let mut builder = plugin::Builder::new();
            if let Some(level) = level {
                builder = builder.level(level);
            }
            if clear_targets || targets.is_some() {
                builder = builder.clear_targets();
            }
            if let Some(targets) = targets {
                for target in targets {
                    builder = builder.target(match target.as_str() {
                        "stdout" => Target::new(TargetKind::Stdout),
                        "stderr" => Target::new(TargetKind::Stderr),
                        "log_dir" => Target::new(TargetKind::LogDir {
                            file_name: file_name.clone(),
                        }),
                        "webview" => Target::new(TargetKind::Webview),
                        _ => unreachable!("validated above"),
                    });
                }
            }
            Box::new(builder.build())
        })))
    }
}

#[pymodule(submodule, gil_used = false)]
pub mod log {
    #[pymodule_export]
    pub use super::Builder;
    pub use super::BuilderArgs;
}
