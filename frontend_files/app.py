import streamlit as st
import os

st.set_page_config(layout="centered", page_title="MonReader", page_icon="📖")

BACKEND_URL = os.getenv("MONREADER_BACKEND_URL", "https://dcsamuel-monreader.hf.space/v1/predict")

st.markdown("""
<style>
[data-testid="stAppViewContainer"],
[data-testid="stMain"],
[data-testid="block-container"] {
    background: #f0f0f0 !important;
    padding: 0 !important;
}
[data-testid="stHeader"], #MainMenu, footer, header { display: none !important; }
</style>
""", unsafe_allow_html=True)

st.components.v1.html(f"""
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}

  body {{
    background: #f0f0f0;
    display: flex;
    justify-content: center;
    align-items: flex-start;
    padding: 32px 16px 48px;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
  }}

  /* ── Phone shell ───────────────────────────────── */
  .phone {{
    width: 340px;
    background: #0f0f1a;
    border-radius: 52px;
    border: 7px solid #2a2a3d;
    box-shadow:
      0 0 0 2px #111,
      0 40px 100px rgba(0,0,0,0.3),
      inset 0 0 0 1px #333;
    position: relative;
    display: flex;
    flex-direction: column;
  }}

  /* Notch */
  .phone::before {{
    content: '';
    position: absolute;
    top: 0; left: 50%;
    transform: translateX(-50%);
    width: 130px; height: 30px;
    background: #0f0f1a;
    border-radius: 0 0 22px 22px;
    border: 6px solid #2a2a3d;
    border-top: none;
    z-index: 10;
  }}

  /* Power button */
  .phone::after {{
    content: '';
    position: absolute;
    top: 110px; right: -10px;
    width: 4px; height: 56px;
    background: #2a2a3d;
    border-radius: 0 3px 3px 0;
    box-shadow: 0 76px 0 0 #2a2a3d;
  }}

  /* Volume buttons */
  .vol {{
    position: absolute;
    top: 110px; left: -10px;
    width: 4px; height: 40px;
    background: #2a2a3d;
    border-radius: 3px 0 0 3px;
    box-shadow: 0 52px 0 0 #2a2a3d;
  }}

  /* Status bar — fixed at top, never scrolls */
  .status-bar {{
    flex-shrink: 0;
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 44px 22px 10px;
    color: #ccc;
    font-size: 11px;
    font-weight: 600;
  }}

  /* Scrollable screen area */
  .screen {{
    flex: 1;
    overflow-y: auto;
    overflow-x: hidden;
    padding: 0 16px 16px;
    /* hide scrollbar visually but keep it functional */
    scrollbar-width: none;        /* Firefox */
    -ms-overflow-style: none;     /* IE */
  }}
  .screen::-webkit-scrollbar {{ display: none; }} /* Chrome/Safari */

  /* Scroll hint pill — shows when content overflows */
  .scroll-hint {{
    flex-shrink: 0;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 5px;
    padding: 6px 0 2px;
    color: #555;
    font-size: 10px;
  }}
  .scroll-hint .arrow {{
    width: 18px; height: 18px;
    border: 1.5px solid #444;
    border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 9px;
    animation: bounce 1.4s ease-in-out infinite;
  }}
  @keyframes bounce {{
    0%,100% {{ transform: translateY(0);   opacity:.5; }}
    50%      {{ transform: translateY(3px); opacity:1;  }}
  }}

  /* Home bar */
  .home-bar {{
    flex-shrink: 0;
    width: 90px; height: 4px;
    background: #333;
    border-radius: 3px;
    margin: 8px auto 20px;
  }}

  /* ── App header ────────────────────────────────── */
  .app-header {{
    background: linear-gradient(135deg, #6c63ff, #3b3566);
    border-radius: 20px;
    padding: 16px;
    text-align: center;
    margin-bottom: 16px;
  }}
  .app-header h1 {{ color:#fff; font-size:18px; font-weight:700; margin-bottom:2px; }}
  .app-header p  {{ color:rgba(255,255,255,0.7); font-size:11px; }}

  /* ── Upload area ───────────────────────────────── */
  .upload-area {{
    border: 2px dashed #6c63ff;
    border-radius: 16px;
    background: rgba(108,99,255,0.08);
    padding: 28px 12px;
    text-align: center;
    cursor: pointer;
    transition: background 0.2s;
    margin-bottom: 14px;
    position: relative;
  }}
  .upload-area:hover {{ background: rgba(108,99,255,0.15); }}
  .upload-area input {{
    position: absolute; inset: 0;
    opacity: 0; cursor: pointer; width: 100%; height: 100%;
  }}
  .upload-area .icon {{ font-size: 32px; margin-bottom: 8px; }}
  .upload-area p    {{ color: #888; font-size: 12px; }}
  .upload-area .hint {{ color: #555; font-size: 10px; margin-top: 4px; }}

  /* ── Preview image ─────────────────────────────── */
  #preview-wrap {{
    display: none;
    border-radius: 14px;
    overflow: hidden;
    margin-bottom: 14px;
    position: relative;
  }}
  #preview-wrap img {{
    width: 100%;
    display: block;
    border-radius: 14px;
  }}
  .preview-badge {{
    position: absolute; bottom: 8px; right: 8px;
    background: rgba(0,0,0,0.6);
    color: #fff; font-size: 10px;
    padding: 3px 8px; border-radius: 20px;
  }}

  /* ── Predict button ────────────────────────────── */
  .btn-predict {{
    width: 100%; padding: 13px;
    background: linear-gradient(135deg, #6c63ff, #4b44cc);
    border: none; border-radius: 14px;
    color: #fff; font-size: 15px; font-weight: 600;
    cursor: pointer; margin-bottom: 10px;
    letter-spacing: 0.3px; transition: opacity 0.2s;
  }}
  .btn-predict:hover  {{ opacity: 0.88; }}
  .btn-predict:active {{ opacity: 0.75; }}
  .btn-predict:disabled {{
    background: #2a2a3d; color: #555;
    cursor: not-allowed; opacity: 1;
  }}

  /* ── Reset button ──────────────────────────────── */
  .btn-reset {{
    width: 100%; padding: 11px;
    background: transparent;
    border: 1.5px solid #3a3a5c;
    border-radius: 14px; color: #777;
    font-size: 13px; cursor: pointer;
    transition: border-color 0.2s, color 0.2s;
    margin-bottom: 36px;
  }}
  .btn-reset:hover {{ border-color: #6c63ff; color: #aaa; }}

  /* ── Spinner ───────────────────────────────────── */
  .spinner-wrap {{
    display: none; text-align: center;
    padding: 12px 0; color: #888; font-size: 12px;
  }}
  .spinner {{
    width: 28px; height: 28px;
    border: 3px solid #2a2a3d; border-top-color: #6c63ff;
    border-radius: 50%;
    animation: spin 0.8s linear infinite;
    margin: 0 auto 8px;
  }}
  @keyframes spin {{ to {{ transform: rotate(360deg); }} }}

  /* ── Result card ───────────────────────────────── */
  .result-card {{
    border-radius: 16px; padding: 16px;
    text-align: center; margin-bottom: 12px; display: none;
  }}
  .result-card.flip    {{ background:rgba(255,107,107,0.12); border:1px solid rgba(255,107,107,0.35); }}
  .result-card.notflip {{ background:rgba(81,207,102,0.12);  border:1px solid rgba(81,207,102,0.35); }}
  .result-icon  {{ font-size:34px; margin-bottom:6px; }}
  .result-label {{ font-size:20px; font-weight:700; margin-bottom:4px; }}
  .result-card.flip    .result-label {{ color:#ff6b6b; }}
  .result-card.notflip .result-label {{ color:#51cf66; }}
  .result-conf  {{ font-size:11px; color:#777; }}

  /* ── Error box ─────────────────────────────────── */
  .error-box {{
    display: none;
    background: rgba(255,107,107,0.1);
    border: 1px solid rgba(255,107,107,0.3);
    border-radius: 12px;
    padding: 10px 14px; color: #ff6b6b;
    font-size: 12px; text-align: center; margin-bottom: 10px;
  }}
</style>
</head>
<body>
<div class="phone">
  <div class="vol"></div>

  <!-- Fixed status bar -->
  <div class="status-bar">
    <span>9:41</span>
    <span>▲▲▲ &nbsp; 🔋</span>
  </div>

  <!-- Scrollable content -->
  <div class="screen" id="screen">

    <div class="app-header">
      <h1>📖 MonReader</h1>
      <p>Page-flip detection</p>
    </div>

    <div class="upload-area" id="upload-area">
      <input type="file" id="file-input" accept="image/jpeg,image/png,image/webp">
      <div class="icon">📷</div>
      <p>Tap to choose an image</p>
      <p class="hint">JPG, PNG or WebP</p>
    </div>

    <div id="preview-wrap">
      <img id="preview-img" src="" alt="preview">
      <div class="preview-badge" id="file-name"></div>
    </div>

    <div class="spinner-wrap" id="spinner">
      <div class="spinner"></div>
      <div>Analysing image…</div>
    </div>

    <div class="error-box" id="error-box"></div>

    <div class="result-card" id="result-card">
      <div class="result-icon"  id="result-icon"></div>
      <div class="result-label" id="result-label"></div>
      <div class="result-conf"  id="result-conf"></div>
    </div>

    <button class="btn-predict" id="btn-predict" disabled>Predict Page-Flip</button>
    <button class="btn-reset"   id="btn-reset"   style="display:none">↩ Reset / New image</button>

  </div><!-- /screen -->

  <!-- Scroll hint — hidden once user has scrolled or no overflow -->
  <div class="scroll-hint" id="scroll-hint" style="display:none">
    <div class="arrow">▼</div>
    <span>scroll for more</span>
    <div class="arrow">▼</div>
  </div>

  <div class="home-bar"></div>
</div><!-- /phone -->

<script>
const BACKEND = "{BACKEND_URL}";

const fileInput   = document.getElementById('file-input');
const uploadArea  = document.getElementById('upload-area');
const previewWrap = document.getElementById('preview-wrap');
const previewImg  = document.getElementById('preview-img');
const fileNameEl  = document.getElementById('file-name');
const spinner     = document.getElementById('spinner');
const errorBox    = document.getElementById('error-box');
const resultCard  = document.getElementById('result-card');
const resultIcon  = document.getElementById('result-icon');
const resultLabel = document.getElementById('result-label');
const resultConf  = document.getElementById('result-conf');
const btnPredict  = document.getElementById('btn-predict');
const btnReset    = document.getElementById('btn-reset');
const screen      = document.getElementById('screen');
const scrollHint  = document.getElementById('scroll-hint');

let selectedFile = null;

// Show scroll hint when content overflows, hide once user scrolls
function checkOverflow() {{
  if (screen.scrollHeight > screen.clientHeight + 10) {{
    scrollHint.style.display = 'flex';
  }} else {{
    scrollHint.style.display = 'none';
  }}
}}

screen.addEventListener('scroll', () => {{
  if (screen.scrollTop > 10) scrollHint.style.display = 'none';
}});

fileInput.addEventListener('change', (e) => {{
  const file = e.target.files[0];
  if (!file) return;
  selectedFile = file;

  const reader = new FileReader();
  reader.onload = (ev) => {{
    previewImg.src = ev.target.result;
    previewWrap.style.display = 'block';
    uploadArea.style.display  = 'none';
    fileNameEl.textContent    = file.name;
    btnPredict.disabled = false;
    setTimeout(checkOverflow, 100);
  }};
  reader.readAsDataURL(file);

  hide(resultCard); hide(errorBox); hide(btnReset);
  resultCard.className = 'result-card';
}});

btnPredict.addEventListener('click', async () => {{
  if (!selectedFile) return;

  btnPredict.disabled = true;
  show(spinner); hide(errorBox); hide(resultCard);
  setTimeout(checkOverflow, 50);

  const formData = new FormData();
  formData.append('image', selectedFile, selectedFile.name);

  try {{
    const resp = await fetch(BACKEND, {{ method: 'POST', body: formData }});
    const data = await resp.json();
    hide(spinner);

    if (!resp.ok || data.error) {{
      showError(data.error || 'Server error ' + resp.status);
      btnPredict.disabled = false;
      setTimeout(checkOverflow, 50);
      return;
    }}

    const pred   = data.prediction;
    const score  = data.prediction_score;
    const isFlip = pred === 'flip';
    const conf = isFlip ? (1 - score) : score;

    resultCard.className   = 'result-card ' + (isFlip ? 'flip' : 'notflip');
    resultIcon.textContent  = isFlip ? '📄🔄' : '📄✅';
    resultLabel.textContent = isFlip ? 'Page Flip' : 'Not a Flip';
    resultConf.textContent  = 'Confidence: ' + (conf * 100).toFixed(1) + '%';

    show(resultCard); show(btnReset);
    btnPredict.style.display = 'none';

    // Scroll result into view and check overflow
    setTimeout(() => {{
      resultCard.scrollIntoView({{ behavior: 'smooth', block: 'nearest' }});
      checkOverflow();
    }}, 100);

  }} catch (err) {{
    hide(spinner);
    showError('Could not reach backend. Check your connection.');
    btnPredict.disabled = false;
    setTimeout(checkOverflow, 50);
  }}
}});

btnReset.addEventListener('click', () => {{
  selectedFile = null;
  fileInput.value = '';
  previewImg.src  = '';
  previewWrap.style.display = 'none';
  uploadArea.style.display  = 'block';
  btnPredict.style.display  = 'block';
  btnPredict.disabled = true;
  hide(resultCard); hide(errorBox); hide(btnReset); hide(spinner);
  resultCard.className = 'result-card';
  screen.scrollTop = 0;
  setTimeout(checkOverflow, 50);
}});

function show(el) {{ el.style.display = 'block'; }}
function hide(el) {{ el.style.display = 'none';  }}
function showError(msg) {{ errorBox.textContent = msg; show(errorBox); }}

// Initial check
setTimeout(checkOverflow, 200);
</script>
</body>
</html>
""", height=900, scrolling=False)
