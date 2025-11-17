const BASE_URL = "https://YOUR_BACKEND_URL";

export async function getSignedUploadUrl() {
  const res = await fetch(`${BASE_URL}/generate-upload-url`);
  if (!res.ok) throw new Error("Failed to get upload URL");
  return await res.json();  // { upload_url, gcs_path }
}

export async function registerVideo({ gcs_path }) {
  const res = await fetch(`${BASE_URL}/upload-video`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ gcs_path })
  });
  if (!res.ok) throw new Error("Failed to register video");
  return await res.json();
}
