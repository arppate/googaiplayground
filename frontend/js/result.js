import { generateImage, modifyImage } from './api.js';
import { state } from './state.js';

const statusEl = document.getElementById('status');
const mainImage = document.getElementById('mainImage');
const taglineEl = document.getElementById('tagline');
const captionsEl = document.getElementById('captions');
const editPrompt = document.getElementById('editPrompt');
const applyEditBtn = document.getElementById('applyEditBtn');
const downloadBtn = document.getElementById('downloadBtn');

function redirectBack() {
  window.location.href = 'select-frame.html';
}

async function init() {
  // restore from localStorage if needed
  const saved = localStorage.getItem('clip2_state');
  if (saved && !state.selectedFrame) Object.assign(state, JSON.parse(saved));

  if (!state.selectedFrame || !state.selectedPlatform) {
    alert('Missing selection. Go back and choose frame & platform.');
    redirectBack();
    return;
  }

  statusEl.textContent = 'Generating a marketing image...';
  try {
    const frame_b64 = state.selectedFrame.image_base64;
    const platform = state.selectedPlatform;
    const res = await generateImage(frame_b64, platform);

    // set UI
    state.generatedImage = {
      image_base64: res.generated_image_base64,
      caption: res.caption,
      tagline: res.tagline,
      image_prompt: res.image_prompt
    };

    mainImage.src = `data:image/jpeg;base64,${state.generatedImage.image_base64}`;
    taglineEl.textContent = state.generatedImage.tagline;
    captionsEl.innerHTML = `<div class="text-sm">${state.generatedImage.caption}</div>`;

    editPrompt.value = state.generatedImage.image_prompt || '';

    statusEl.textContent = 'Done';
    localStorage.setItem('clip2_state', JSON.stringify(state));
  } catch (err) {
    console.error(err);
    statusEl.textContent = 'Error generating image. Try again.';
  }
}

applyEditBtn.addEventListener('click', async () => {
  const prompt = editPrompt.value.trim();
  if (!prompt) {
    alert('Enter a prompt for modification');
    return;
  }
  applyEditBtn.disabled = true;
  statusEl.textContent = 'Applying edit...';
  try {
    const res = await modifyImage(state.generatedImage.image_base64, prompt);
    state.generatedImage.image_base64 = res.modified_image_base64;
    mainImage.src = `data:image/jpeg;base64,${state.generatedImage.image_base64}`;
    statusEl.textContent = 'Edit applied';
    localStorage.setItem('clip2_state', JSON.stringify(state));
  } catch (err) {
    console.error(err);
    statusEl.textContent = 'Edit failed';
  }
  applyEditBtn.disabled = false;
});

downloadBtn.addEventListener('click', () => {
  const a = document.createElement('a');
  a.href = mainImage.src;
  a.download = 'clip2campaign_generated.jpg';
  document.body.appendChild(a);
  a.click();
  a.remove();
});

init();
