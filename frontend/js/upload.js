import { uploadVideo } from './api.js';
import { state } from './state.js';

const videoInput = document.getElementById("videoInput");
const uploadBtn = document.getElementById("uploadBtn");
const statusText = document.getElementById("status");

uploadBtn.addEventListener("click", async () => {

  const file = videoInput.files[0];

  if (!file) {
    statusText.textContent = "Please select a video file.";
    return;
  }

  statusText.textContent = "Uploading...";
  uploadBtn.disabled = true;

  try {
    // 1. Upload file via backend
    const response = await uploadVideo(file);

    // 2. Save state
    state.videoId = response.video_id;
    state.gcsUri = response.gcs_uri;

    statusText.textContent = "Upload complete. Processing...";
    
    // 3. Redirect to select frame page
    setTimeout(() => {
      window.location.href = "select-frame.html";
    }, 800);

  } catch (error) {
    console.error(error);
    statusText.textContent = "Upload failed. Try again.";
  }

  uploadBtn.disabled = false;
});
