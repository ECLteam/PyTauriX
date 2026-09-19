let greetInputEl: HTMLInputElement | null = null;
let greetMsgEl: HTMLElement | null = null;

// --8<-- [start:invoke]

import { invoke } from "@tauri-apps/api/core";
import { pyInvoke } from "@pytaurix/api";
// or if tauri config `app.withGlobalTauri = true`:
//
// ```js
// const { invoke } = window.__TAURI__.core;
// const { pyInvoke } = window.__TAURI__.pytaurix;
// ```

interface Greeting {
  message: string;
}

async function greet() {
  if (greetMsgEl && greetInputEl) {
    // Learn more about Tauri commands at https://tauri.app/develop/calling-rust/
    const rsGreeting = await invoke<string>("greet", {
      name: greetInputEl.value,
    });
    const pyGreeting = await pyInvoke<Greeting>("greet", {
      name: greetInputEl.value,
    });
    greetMsgEl.textContent = rsGreeting + "\n" + pyGreeting.message;
  }
}

// --8<-- [end:invoke]
