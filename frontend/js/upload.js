import { getSignedUploadUrl, registerVideo } from './api.js';
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

  statusText.textContent = "Getting upload URL...";
  uploadBtn.disabled = true;

  try {
    // Step 1: get signed upload URL from backend
    const { upload_url, gcs_path } = await getSignedUploadUrl();

    statusText.textContent = "Uploading to GCS...";
    // Step 2: upload directly to GCS using PUT
    await fetch(upload_url, {
      method: "PUT",
      headers: {
        "Content-Type": file.type
      },
      body: file
    });

    statusText.textContent = "Registering video...";
    // Step 3: register the upload with your backend
    const meta = await registerVideo({ gcs_path });

    // Save in state
    state.gcsUri = `gs://${meta.gcs_path.includes("/") ? meta.gcs_path.split("/")[0] : ""}/${meta.gcs_path}`;
    statusText.textContent = "Upload complete!";
    localStorage.setItem("clip2_state", JSON.stringify(state));

    // Redirect to frame selection
    setTimeout(() => {
      window.location.href = "select-frame.html";
    }, 500);

  } catch (err) {
    console.error(err);
    statusText.textContent = "Upload failed. Try again.";
  } finally {
    uploadBtn.disabled = false;
  }
});
