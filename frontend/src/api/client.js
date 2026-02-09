/**
 * Base API client. All requests go to the backend.
 * Set VITE_API_URL in .env or .env.local (default: http://localhost:8000).
 */
const BASE = import.meta.env.VITE_API_URL || "http://localhost:8000";

async function request(path, options = {}) {
  const url = `${BASE}${path}`;
  const res = await fetch(url, {
    headers: {
      "Content-Type": "application/json",
      ...options.headers,
    },
    ...options,
  });
  if (!res.ok) {
    const text = await res.text();
    let detail = text;
    try {
      const j = JSON.parse(text);
      detail = j.detail || text;
    } catch (_) {}
    const err = new Error(detail);
    err.status = res.status;
    throw err;
  }
  if (res.status === 204) return;
  return res.json();
}

export const api = {
  get: (path) => request(path, { method: "GET" }),
  post: (path, body) =>
    request(path, { method: "POST", body: body ? JSON.stringify(body) : undefined }),
  put: (path, body) =>
    request(path, { method: "PUT", body: body ? JSON.stringify(body) : undefined }),
  delete: (path) => request(path, { method: "DELETE" }),
};
