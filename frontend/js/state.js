export const state = {
  videoId: null,
  gcsUri: null,
  frames: [],            // array of {frame_id, image_base64, ...}
  selectedFrame: null,   // {frame_id, image_base64}
  selectedPlatform: null,
  generatedImage: null,  // {image_base64, caption, tagline, image_prompt}
};
