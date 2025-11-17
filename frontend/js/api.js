const BASE_URL = "https://YOUR-CLOUD-RUN-URL"; // update

export async function uploadVideo(file) {
  const fd = new FormData();
  fd.append('file', file);
  const r = await fetch(`${BASE_URL}/upload-video`, { method: 'POST', body: fd });
  if (!r.ok) throw new Error('upload failed');
  return await r.json();
}

export async function processVideo(gcsUri, platforms = ["instagram","linkedin","x"]) {
  const r = await fetch(`${BASE_URL}/process-video`, {
    method: 'POST',
    headers: {'Content-Type':'application/json'},
    body: JSON.stringify({ gcs_uri: gcsUri, platforms })
  });
  if (!r.ok) throw new Error('process failed');
  return await r.json();
}

export async function generateImage(frameBase64, platform) {
  const r = await fetch(`${BASE_URL}/generate-image`, {
    method: 'POST',
    headers: {'Content-Type':'application/json'},
    body: JSON.stringify({ frame_base64: frameBase64, platform })
  });
  if (!r.ok) throw new Error('generate failed');
  return await r.json();
}

export async function modifyImage(imageBase64, prompt) {
  const r = await fetch(`${BASE_URL}/modify-image`, {
    method: 'POST',
    headers: {'Content-Type':'application/json'},
    body: JSON.stringify({ image_base64: imageBase64, prompt })
  });
  if (!r.ok) throw new Error('modify failed');
  return await r.json();
}
