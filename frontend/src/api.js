const API_BASE = import.meta.env.VITE_API_URL || "http://localhost:8000";

export async function generateNda(payload) {
  const response = await fetch(`${API_BASE}/api/nda/generate/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });

  const data = await response.json().catch(() => ({}));

  if (!response.ok) {
    const error = new Error(data.error || "Unable to generate the NDA.");
    error.errors = data.errors || {};
    throw error;
  }

  return data;
}
