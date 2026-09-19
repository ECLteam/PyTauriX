import { pyInvoke } from "@pytaurix/api";
import { Channel } from "@tauri-apps/api/core";
// const { pyInvoke } = window.__TAURI__.pytaurix;
// const { Channel } = window.__TAURI__.core;

const channel = new Channel<string>((msg) => console.log(msg));

await pyInvoke("command", channel);
