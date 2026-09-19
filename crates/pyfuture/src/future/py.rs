use std::task::Waker;

use pyo3::prelude::*;

#[pyclass(subclass)]
pub struct PyFuture {
    #[pyo3(get)]
    awaitable: Py<PyAny>,
    waker: Waker,
    result: Option<PyResult<Py<PyAny>>>,
}

impl PyFuture {
    pub(crate) const fn new(awaitable: Py<PyAny>, waker: Waker) -> Self {
        Self {
            awaitable,
            waker,
            result: None,
        }
    }

    fn wake(&self) {
        self.waker.wake_by_ref();
    }

    pub(crate) fn waker_clone_from(&mut self, waker: &Waker) {
        self.waker.clone_from(waker);
    }

    pub(crate) fn result_as_ref(&self) -> Option<&PyResult<Py<PyAny>>> {
        self.result.as_ref()
    }

    // // we don't need yet, just leave it here for future use
    //
    // pub(crate) fn result_as_mut(&mut self) -> Option<&mut PyResult<Py<PyAny>>> {
    //     self.result.as_mut()
    // }
}

#[pymethods]
impl PyFuture {
    fn set_result(&mut self, result: Py<PyAny>) {
        self.result = Some(Ok(result));
        self.wake();
    }

    fn set_exception(&mut self, exception: Bound<'_, PyAny>) {
        self.result = Some(Err(PyErr::from_value(exception)));
        self.wake();
    }
}
