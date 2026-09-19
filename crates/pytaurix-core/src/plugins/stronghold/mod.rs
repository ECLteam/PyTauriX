use crate::ext_mod::plugin::Plugin;
use pyo3::prelude::*;
use std::path::PathBuf;
use tauri_plugin_stronghold as plugin;

#[pyclass(frozen)]
pub struct Builder;

#[pymethods]
impl Builder {
    #[staticmethod]
    fn with_argon2(salt_path: PathBuf) -> Plugin {
        Plugin::new(Box::new(move || {
            Box::new(plugin::Builder::with_argon2(&salt_path).build())
        }))
    }
}

#[pymodule(submodule, gil_used = false)]
pub mod stronghold {
    #[pymodule_export]
    pub use super::Builder;
}

#[cfg(test)]
mod tests {
    use std::{
        fs,
        time::{SystemTime, UNIX_EPOCH},
    };

    use tauri_plugin_stronghold::stronghold::Stronghold;

    #[test]
    fn encrypted_vault_round_trip_does_not_expose_secret() {
        let nonce = SystemTime::now()
            .duration_since(UNIX_EPOCH)
            .unwrap()
            .as_nanos();
        let path = std::env::temp_dir().join(format!("pytaurix-stronghold-{nonce}.hold"));
        let password = vec![7; 32];
        let secret = b"test-secret-not-for-logs".to_vec();

        let stronghold = Stronghold::new(&path, password.clone()).unwrap();
        let client = stronghold.create_client(b"pytaurix-test").unwrap();
        client
            .store()
            .insert(b"token".to_vec(), secret.clone(), None)
            .unwrap();
        stronghold.save().unwrap();

        let reopened = Stronghold::new(&path, password).unwrap();
        let client = reopened.load_client(b"pytaurix-test").unwrap();
        assert_eq!(client.store().get(b"token").unwrap(), Some(secret));
        fs::remove_file(path).unwrap();
    }
}
