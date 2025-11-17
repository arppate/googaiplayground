import { processVideo } from './api.js';
import { state } from './state.js';

const statusEl = document.getElementById('status');
const framesGrid = document.getElementById('framesGrid');
const generateBtn = document.getElementById('generateBtn');
const autoSelectBtn = document.getElementById('autoSelectBtn');
const platformSelect = document.getElementById('platformSelect');

function redirectToUpload() {
  window.location.href = 'index.html';
}

async function init() {
  if (!state.gcsUri) {
    // try to recover from localStorage fallback
    const saved = localStorage.getItem('clip2_state');
    if (saved) {
      Object.assign(state, JSON.parse(saved));
    }
  }
  if (!state.gcsUri) {
    alert('No uploaded video found. Please upload first.');
    redirectToUpload();
    return;
  }

  statusEl.textContent = 'Extracting frames... (this can take a few seconds)';
  try {
    const res = await processVideo(state.gcsUri, ["instagram","linkedin","x"]);
    state.frames = res.frames || [];
    renderFrames(state.frames);
    statusEl.textContent = `Choose a frame (${state.frames.length} found)`;
    // persist
    localStorage.setItem('clip2_state', JSON.stringify(state));
  } catch (err) {
    console.error(err);
    statusEl.textContent = 'Error extracting frames. Try again.';
    generateBtn.disabled = true;
  }
}

function renderFrames(frames) {
  framesGrid.innerHTML = '';
  frames.forEach((f, idx) => {
    const div = document.createElement('div');
    div.className = 'border rounded overflow-hidden relative cursor-pointer hover:shadow-lg';
    div.innerHTML = `
      <img src="data:image/jpeg;base64,${f.image_base64}" class="w-full h-36 object-cover" />
      <div class="p-2">
        <div class="text-sm font-medium">Frame ${idx+1}</div>
        <div class="text-xs text-gray-500">Score: ${f.heuristic_score?.toFixed(2) ?? '-'}</div>
      </div>
      <input type="radio" name="frame_select" data-idx="${idx}" style="position:absolute; top:8px; left:8px;" />
    `;
    framesGrid.appendChild(div);
  });

  // add click handlers on radios
  document.querySelectorAll('input[name="frame_select"]').forEach(inp => {
    inp.addEventListener('change', (e) => {
      const idx = parseInt(e.target.dataset.idx, 10);
      state.selectedFrame = state.frames[idx];
      generateBtn.disabled = false;
      localStorage.setItem('clip2_state', JSON.stringify(state));
    });
  });
}

autoSelectBtn.addEventListener('click', () => {
  if (!state.frames || !state.frames.length) return;
  state.selectedFrame = state.frames[0];
  // mark radio visually
  const firstRadio = document.querySelector('input[name="frame_select"]');
  if (firstRadio) firstRadio.checked = true;
  generateBtn.disabled = false;
  localStorage.setItem('clip2_state', JSON.stringify(state));
});

generateBtn.addEventListener('click', () => {
  if (!state.selectedFrame) {
    alert('Select a frame first');
    return;
  }
  state.selectedPlatform = platformSelect.value;
  localStorage.setItem('clip2_state', JSON.stringify(state));
  window.location.href = 'result.html';
});

init();
