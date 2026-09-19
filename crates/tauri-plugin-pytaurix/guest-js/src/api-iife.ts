import * as pytaurix from "./index";

if ("__TAURI__" in window) {
    Object.defineProperty(window.__TAURI__, "pytaurix", { value: pytaurix });
}
