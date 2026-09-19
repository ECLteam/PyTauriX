import { pyInvoke } from "@pytaurix/api";
// or if tauri config `app.withGlobalTauri = true`:
//
// ```js
// const { pyInvoke } = window.__TAURI__.pytaurix;
// ```

const output = await pyInvoke<string>("command", { foo: "foo", bar: 42 });
