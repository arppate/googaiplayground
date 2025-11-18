const BACKEND_URL = "https://clip2campaign-backend-770831665204.europe-west1.run.app";

// -----------------------------
// 1) Generate signed upload URL
// -----------------------------

export async function generateUploadURL() {
  const res = await fetch(`${BACKEND_URL}/generate-upload-url`);
  if (!res.ok) throw new Error("Failed to generate upload URL");
  return res.json();
}

// -----------------------------
// 2) Upload video to GCS
// -----------------------------

export async function uploadVideoToGCS(uploadUrl, file) {
  const res = await fetch(uploadUrl, {
    method: "PUT",
    headers: {
      "Content-Type": "video/mp4",
    },
    body: file,
  });

  if (!res.ok) {
    console.error("Upload failed:", await res.text());
    throw new Error("Video upload to GCS failed");
  }

  return true;
}

// -----------------------------
// 3) Register uploaded video
// -----------------------------

export async function registerVideo(gcsPath, videoId) {
  const res = await fetch(`${BACKEND_URL}/upload-video`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ gcs_path: gcsPath, video_id: videoId }),
  });

  if (!res.ok) throw new Error("Failed to register video");
  return res.json();
}

// -----------------------------
// 4) Process video (frames + scoring)
// -----------------------------

export async function processVideo(gcsUri, platforms) {
  const res = await fetch(`${BACKEND_URL}/process-video`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ gcs_uri: gcsUri, platforms }),
  });

  if (!res.ok) throw new Error("Video processing failed");
  return res.json(); // { frames: [...] }
}

// -----------------------------
// 5) Generate marketing images
// -----------------------------

export async function generateImage(frameBase64, platform) {
  const res = await fetch(`${BACKEND_URL}/generate-image`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ frame_base64: frameBase64, platform }),
  });

  if (!res.ok) throw new Error("Image generation failed");
  return res.json();
}

// -----------------------------
// 6) Modify generated images
// -----------------------------

export async function modifyImage(imageBase64, prompt) {
  const res = await fetch(`${BACKEND_URL}/modify-image`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ image_base64: imageBase64, prompt }),
  });

  if (!res.ok) throw new Error("Image modification failed");
  return res.json();
}
