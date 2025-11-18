uploadBtn.addEventListener("click", async () => {
  const file = videoInput.files[0];
  if (!file) {
    statusText.textContent = "Please select a video file.";
    return;
  }

  statusText.textContent = "Getting upload URL...";
  uploadBtn.disabled = true;

  try {
    // Step 1: get signed upload URL
    const { upload_url, gcs_path, video_id } = await getSignedUploadUrl();

    statusText.textContent = "Uploading to GCS...";
    
    // Step 2: upload video to GCS
    await fetch(upload_url, {
      method: "PUT",
      headers: { "Content-Type": file.type },
      body: file
    });

    statusText.textContent = "Registering video...";

    // Step 3: correctly register with backend
    const meta = await registerVideo(gcs_path, video_id);

    // Save in state
    state.videoId = meta.video_id;
    state.gcsUri = meta.gcs_uri;

    statusText.textContent = "Upload complete!";
    localStorage.setItem("clip2_state", JSON.stringify(state));

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
