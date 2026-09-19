//! tauri runtime configuration for pytaurix.

/// The current [tauri::Runtime] for pytaurix.
#[cfg(not(all(feature = "__test", not(feature = "__no_test"))))]
pub type Runtime = tauri::Wry;

#[cfg(all(feature = "__test", not(feature = "__no_test")))]
pub type Runtime = tauri::test::MockRuntime;
