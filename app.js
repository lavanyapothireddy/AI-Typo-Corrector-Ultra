/* ═══════════════════════════════════════════════════════════
   AI TYPO CORRECTOR ULTRA  ·  js/app.js
   Groq API · llama-3.3-70b-versatile
   No login · No setup · Works instantly
═══════════════════════════════════════════════════════════ */

'use strict';

/* ── ⚙️  CONFIG — Your Groq API Key is hardcoded here ── */
// ⚠️ DO NOT hardcode your key here — use Render Environment Variables
const GROQ_API_KEY = window.__GROQ_KEY__ || '';
const GROQ_MODEL   = 'llama-3.3-70b-versatile';
const GROQ_URL     = 'https://api.groq.com/openai/v1/chat/completions';

/* ── DOM ─────────────────────────────────────────────── */
const $  = id => document.getElementById(id);
const D  = {
  inputText:      $('inputText'),
  inputMeta:      $('inputMeta'),
  clearBtn:       $('clearBtn'),
  correctBtn:     $('correctBtn'),
  outputBox:      $('outputBox'),
  outputMeta:     $('outputMeta'),
  copyBtn:        $('copyBtn'),
  badge:          $('badge'),
  arrowRing:      $('arrowRing'),
  statusDot:      $('statusDot'),
  statusText:     $('statusText'),
  errorBar:       $('errorBar'),
  errorMsg:       $('errorMsg'),
  errClose:       $('errClose'),
  changesSection: $('changesSection'),
  changesCount:   $('changesCount'),
  changesSummary: $('changesSummary'),
  changesGrid:    $('changesGrid'),
  loaderOverlay:  $('loaderOverlay'),
  loaderMsg:      $('loaderMsg'),
};

/* ── STATE ───────────────────────────────────────────── */
let busy = false;

/* ── SYSTEM PROMPT ───────────────────────────────────── */
const SYSTEM_PROMPT = `You are a professional English proofreader and grammar correction engine.

Fix ALL errors in the user's text including:
- Spelling mistakes and typos
- Grammar errors (wrong tense, subject-verb disagreement, etc.)
- Punctuation errors (missing commas, full stops, apostrophes)
- Wrong word usage (their/there/they're, to/too/two, your/you're, etc.)
- Capitalization errors (sentence starts, proper nouns)
- Run-on sentences or missing words

RESPOND ONLY with a valid JSON object. No markdown, no code fences, no text outside JSON.

JSON format:
{
  "corrected": "The fully corrected version of the input text.",
  "changes": [
    { "wrong": "original wrong word or phrase", "right": "corrected version", "type": "typo|grammar|punctuation|style|other" }
  ],
  "summary": "One sentence summarizing what was fixed."
}

Rules:
- Fix EVERY single error without exception.
- Preserve original meaning and tone completely.
- If the text is already correct, set changes to [] and mention it in summary.
- The JSON must be strictly valid. No trailing commas. No comments.`;

/* ── LOADER MESSAGES ─────────────────────────────────── */
const LOADER_MSGS = [
  'Analyzing your text...',
  'Detecting typos and errors...',
  'Running grammar check...',
  'Checking punctuation...',
  'Polishing sentences...',
  'Almost done...',
];

/* ── INIT ────────────────────────────────────────────── */
document.addEventListener('DOMContentLoaded', () => {
  bindEvents();
  setStatus('ready', 'Ready — paste your text and click Correct Now');
});

/* ── EVENTS ──────────────────────────────────────────── */
function bindEvents() {
  D.inputText.addEventListener('input', updateInputMeta);
  D.clearBtn.addEventListener('click', clearAll);
  D.copyBtn.addEventListener('click', copyOutput);
  D.correctBtn.addEventListener('click', runCorrection);
  D.errClose.addEventListener('click', hideError);
  document.addEventListener('keydown', e => {
    if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') runCorrection();
  });
}

/* ── STATUS ──────────────────────────────────────────── */
function setStatus(type, msg) {
  D.statusDot.className = 'status-dot' + (type !== 'ready' ? ` ${type}` : '');
  if (msg) D.statusText.textContent = msg;
}

/* ── INPUT META ──────────────────────────────────────── */
function updateInputMeta() {
  const v = D.inputText.value;
  const w = v.trim() ? v.trim().split(/\s+/).length : 0;
  D.inputMeta.textContent = `${w} word${w !== 1 ? 's' : ''} · ${v.length} chars`;
}

/* ── CLEAR ───────────────────────────────────────────── */
function clearAll() {
  D.inputText.value = '';
  updateInputMeta();
  resetOutput();
  hideError();
  setStatus('ready', 'Ready — paste your text and click Correct Now');
}

function resetOutput() {
  D.outputBox.innerHTML = `
    <div class="empty-state">
      <div class="empty-icon">
        <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
          <path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z"/>
          <polyline points="14 2 14 8 20 8"/>
          <line x1="16" y1="13" x2="8" y2="13"/>
          <line x1="16" y1="17" x2="8" y2="17"/>
        </svg>
      </div>
      <p class="empty-title">Corrected text appears here</p>
      <p class="empty-hint">Enter text on the left → click <strong>Correct Now</strong></p>
    </div>`;
  D.outputMeta.textContent = '—';
  D.badge.style.display = 'none';
  D.changesSection.style.display = 'none';
}

/* ── COPY ────────────────────────────────────────────── */
function copyOutput() {
  const txt = D.outputBox.innerText.trim();
  if (!txt || txt.includes('Corrected text appears here')) return;
  navigator.clipboard.writeText(txt).then(() => {
    D.copyBtn.textContent = '✓ Copied!';
    setTimeout(() => { D.copyBtn.textContent = '⎘ Copy'; }, 2200);
  });
}

/* ── ERROR ───────────────────────────────────────────── */
function showError(msg) {
  D.errorMsg.textContent = msg;
  D.errorBar.style.display = 'flex';
  setStatus('error', 'Error — see message below');
}
function hideError() {
  D.errorBar.style.display = 'none';
}

/* ── LOADER ──────────────────────────────────────────── */
let _loaderTimer;
function showLoader() {
  D.loaderOverlay.style.display = 'flex';
  D.arrowRing.classList.add('spinning');
  D.correctBtn.disabled = true;
  let i = 0;
  D.loaderMsg.textContent = LOADER_MSGS[0];
  _loaderTimer = setInterval(() => {
    i = (i + 1) % LOADER_MSGS.length;
    D.loaderMsg.textContent = LOADER_MSGS[i];
  }, 1500);
}
function hideLoader() {
  D.loaderOverlay.style.display = 'none';
  D.arrowRing.classList.remove('spinning');
  D.correctBtn.disabled = false;
  clearInterval(_loaderTimer);
}

/* ── MAIN ────────────────────────────────────────────── */
async function runCorrection() {
  if (busy) return;
  const input = D.inputText.value.trim();
  if (!input) {
    showError('Please type or paste some text first.');
    return;
  }

  hideError();
  showLoader();
  busy = true;
  setStatus('busy', 'Correcting your text...');

  try {
    const result = await callGroq(input);
    hideLoader();
    renderResult(result);
    setStatus('ready', `Done! ${result.changes?.length || 0} correction(s) applied.`);
  } catch (err) {
    hideLoader();
    handleError(err);
  } finally {
    busy = false;
  }
}

/* ── GROQ API CALL ───────────────────────────────────── */
async function callGroq(userText) {
  const res = await fetch(GROQ_URL, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${GROQ_API_KEY}`,
    },
    body: JSON.stringify({
      model: GROQ_MODEL,
      temperature: 0.1,
      max_tokens: 4096,
      messages: [
        { role: 'system', content: SYSTEM_PROMPT },
        { role: 'user',   content: userText },
      ],
    }),
  });

  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err?.error?.message || `Groq API error: ${res.status}`);
  }

  const data = await res.json();
  const raw  = data?.choices?.[0]?.message?.content || '';
  return parseResult(raw);
}

/* ── PARSE JSON RESPONSE ─────────────────────────────── */
function parseResult(raw) {
  // Strip accidental markdown fences
  const clean = raw.replace(/```json\s*/gi, '').replace(/```/g, '').trim();

  // Find JSON object
  const match = clean.match(/\{[\s\S]*\}/);
  if (!match) throw new Error('Unexpected response format from AI. Please try again.');

  try {
    return JSON.parse(match[0]);
  } catch {
    throw new Error('Could not read AI response. Please try again.');
  }
}

/* ── ERROR HANDLER ───────────────────────────────────── */
function handleError(err) {
  console.error('[Typo Corrector Ultra]', err);
  const m = err.message || '';
  if (m.includes('401') || m.includes('invalid_api_key')) {
    showError('API key is invalid or expired. Please update the key in js/app.js.');
  } else if (m.includes('429') || m.includes('rate_limit')) {
    showError('Rate limit reached. Please wait a moment and try again.');
  } else if (m.includes('Failed to fetch') || m.includes('NetworkError') || m.includes('fetch')) {
    showError('Network error. Please check your internet connection and try again.');
  } else {
    showError(`Error: ${m}`);
  }
}

/* ── RENDER RESULT ───────────────────────────────────── */
function renderResult({ corrected = '', changes = [], summary = '' }) {

  /* — Output text — */
  D.outputBox.textContent = corrected;

  /* — Output meta — */
  const w = corrected.trim() ? corrected.trim().split(/\s+/).length : 0;
  D.outputMeta.textContent = `${w} word${w !== 1 ? 's' : ''} · ${corrected.length} chars`;

  /* — Badge — */
  const n = Array.isArray(changes) ? changes.length : 0;
  D.badge.textContent     = n > 0 ? `${n} correction${n !== 1 ? 's' : ''}` : '✓ Perfect';
  D.badge.style.display   = 'inline-block';

  /* — Changes section — */
  D.changesSection.style.display = 'block';
  D.changesSummary.textContent   = summary || '';
  D.changesCount.textContent     = n > 0
    ? `${n} fix${n !== 1 ? 'es' : ''} applied`
    : 'No errors found';

  D.changesGrid.innerHTML = '';
  if (n > 0) {
    changes.forEach(ch => {
      const type = (ch.type || 'other').toLowerCase().trim();
      const item = document.createElement('div');
      item.className = 'change-item';
      item.innerHTML = `
        <span class="c-type ${type}">${type}</span>
        <span class="c-wrong" title="${esc(ch.wrong)}">${esc(ch.wrong)}</span>
        <span class="c-arrow">→</span>
        <span class="c-right" title="${esc(ch.right)}">${esc(ch.right)}</span>`;
      D.changesGrid.appendChild(item);
    });
  } else {
    D.changesGrid.innerHTML = `
      <div class="change-item" style="color:var(--emerald);font-size:0.83rem;gap:8px;">
        ✅ &nbsp;${esc(summary) || 'Your text was already correct — great job!'}
      </div>`;
  }
}

/* ── HTML ESCAPE ─────────────────────────────────────── */
function esc(str) {
  const d = document.createElement('div');
  d.appendChild(document.createTextNode(String(str || '')));
  return d.innerHTML;
}
