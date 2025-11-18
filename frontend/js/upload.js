import { getSignedUploadUrl, registerVideo } from "./api.js";
import { state } from "./state.js";

const videoInput = document.getElementById("videoInput");
const uploadBtn = document.getElementById("uploadBtn");

// Safe fallback for status text
const statusEl = document.getElementById("status");
const statusText = statusEl ? statusEl : { textContent: "" };

uploadBtn.addEventListener("click", async () => {
  const file = videoInput.files[0];
  if (!file) {
    statusText.textContent = "Please select a video file.";
    return;
  }

  uploadBtn.disabled = true;
  statusText.textContent = "Getting upload URL...";

  try {
    // -------------------------------
    // 1. Get signed URL from backend
    // -------------------------------
    const { upload_url, gcs_path, video_id } = await getSignedUploadUrl();

    statusText.textContent = "Uploading video...";

    // -------------------------------
    // 2. Upload file to GCS PUT URL
    // -------------------------------
    await fetch(upload_url, {
      method: "PUT",
      headers: { "Content-Type": file.type },
      body: file,
    });

    statusText.textContent = "Registering video...";

    // -------------------------------
    // 3. Register video with backend
    // -------------------------------
    const response = await registerVideo(gcs_path, video_id);

    // response returns gcs_uri
    state.gcsUri = response.gcs_uri;
    state.videoId = video_id;

    localStorage.setItem("clip2_state", JSON.stringify(state));

    statusText.textContent = "Upload complete! Redirecting...";

    setTimeout(() => {
      window.location.href = "select-frame.html";
    }, 500);

  } catch (err) {
    console.error(err);
    statusText.textContent = "Upload failed. Please try again.";
  } finally {
    uploadBtn.disabled = false;
  }
});
