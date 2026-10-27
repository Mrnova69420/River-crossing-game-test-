import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="River Crossing - HD Audio & Responsive Edition", page_icon="🚣", layout="wide")

game_html = """
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fredoka:wght@500;600;700&family=Plus+Jakarta+Sans:wght@600;700;800&display=swap" rel="stylesheet">

<style>
    * { box-sizing: border-box; font-family: 'Plus Jakarta Sans', sans-serif; user-select: none; touch-action: manipulation; -webkit-tap-highlight-color: transparent; }
    h1, h2, h3, .title-text, .bank-header, .btn, .action-btn, .modal-title, .avatar-card { font-family: 'Fredoka', cursive; }

    body {
        margin: 0; padding: clamp(8px, 1.8vw, 16px); background: #080c14;
        background-image: radial-gradient(circle at 50% 0%, #151d2a 0%, #080c14 75%);
        color: #f0f6fc; min-height: 100vh; position: relative; overflow-x: hidden;
    }

    /* --- TOP NAVIGATION BAR --- */
    .top-bar {
        display: flex; flex-wrap: wrap; justify-content: space-between; align-items: center;
        background: rgba(22, 30, 44, 0.88); backdrop-filter: blur(16px);
        padding: clamp(10px, 1.4vw, 14px) clamp(12px, 2vw, 20px);
        border-radius: 20px; margin-bottom: 12px; gap: 10px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 8px 32px rgba(0,0,0,0.5);
    }
    .title-text { font-size: clamp(18px, 2.4vw, 24px); font-weight: 700; color: #60a5fa; display: flex; align-items: center; gap: 8px; }
    .right-top-controls { display: flex; align-items: center; gap: clamp(6px, 1vw, 10px); flex-wrap: wrap; }

    .select-control {
        background: #1e293b; color: #f8fafc; border: 1px solid #334155;
        padding: clamp(6px, 1vw, 8px) clamp(8px, 1.2vw, 12px);
        border-radius: 12px; font-weight: 700; font-size: clamp(12px, 1.3vw, 14px);
        cursor: pointer; outline: none; transition: all 0.2s;
    }

    /* 3D TACTILE BUTTONS */
    .btn {
        background: #2563eb; color: white; border: none;
        padding: clamp(7px, 1vw, 9px) clamp(10px, 1.4vw, 15px);
        border-radius: 12px; font-weight: 700; font-size: clamp(12px, 1.3vw, 14px); cursor: pointer;
        box-shadow: 0 4px 0 #1d4ed8; transition: all 0.1s ease; outline: none;
    }
    .btn:active:not(:disabled) { transform: translateY(3px); box-shadow: 0 1px 0 #1d4ed8; }

    .btn-reset { background: #334155; box-shadow: 0 4px 0 #1e293b; color: #e2e8f0; }
    .btn-undo { background: #d97706; box-shadow: 0 4px 0 #b45309; color: white; }
    .btn-audio { background: #1e293b; box-shadow: 0 4px 0 #0f172a; color: #94a3b8; }
    .btn-audio.active { background: #0284c7; box-shadow: 0 4px 0 #0369a1; color: #fff; }
    .btn-solve { background: #7c3aed; box-shadow: 0 4px 0 #6d28d9; color: white; }
    .btn:disabled { opacity: 0.4; cursor: not-allowed; transform: none !important; box-shadow: none !important; }

    .stat-badge {
        background: rgba(15, 23, 42, 0.85); border: 1px solid rgba(255, 255, 255, 0.12);
        padding: 6px clamp(8px, 1.2vw, 12px); border-radius: 12px; font-weight: 700;
        font-size: clamp(12px, 1.3vw, 14px); display: flex; align-items: center; gap: 6px;
    }
    .timer-warning { color: #ef4444 !important; animation: pulse 1s infinite; }
    @keyframes pulse { 0%, 100% { opacity: 1; } 50% { opacity: 0.4; } }

    /* VOLUME CONTROLS PANEL */
    .volume-panel {
        display: none; position: absolute; top: 65px; right: 15px;
        background: #1e293b; border: 1px solid rgba(255,255,255,0.15);
        padding: 14px 18px; border-radius: 16px; box-shadow: 0 12px 30px rgba(0,0,0,0.7);
        z-index: 100; flex-direction: column; gap: 10px; width: min(220px, 85vw);
    }
    .volume-panel.active { display: flex; }
    .vol-row { display: flex; justify-content: space-between; align-items: center; font-size: 13px; font-weight: 700; }
    .vol-row input { width: 95px; cursor: pointer; }

    /* STATUS ALERTS (PROMINENT TEXT) */
    #status-box {
        padding: clamp(10px, 1.5vw, 14px) clamp(14px, 2vw, 20px);
        border-radius: 14px; font-weight: 700; font-size: clamp(14px, 1.8vw, 17px);
        margin-bottom: 12px; display: flex; align-items: center; gap: 10px;
        background: rgba(30, 58, 138, 0.35); border: 1px solid rgba(96, 165, 250, 0.4); color: #93c5fd;
        box-shadow: 0 4px 15px rgba(0,0,0,0.25); transition: all 0.3s;
    }
    .status-error { background: rgba(153, 27, 27, 0.35) !important; border-color: rgba(248, 113, 113, 0.5) !important; color: #fca5a5 !important; }
    .status-success { background: rgba(22, 101, 52, 0.35) !important; border-color: rgba(74, 222, 128, 0.5) !important; color: #86efac !important; }

    /* STAGE BOARD */
    .stage {
        display: flex; height: clamp(280px, 45vh, 360px); border-radius: 22px; overflow: hidden;
        box-shadow: 0 20px 50px rgba(0,0,0,0.6), inset 0 1px 1px rgba(255,255,255,0.1);
        position: relative; border: 2px solid #1e293b;
    }

    .bank {
        width: 28%;
        background: linear-gradient(180deg, #15803d 0%, #166534 60%, #14532d 100%);
        display: flex; flex-direction: column; align-items: center;
        padding: 14px 8px; position: relative; z-index: 2;
    }
    .bank-left { border-right: clamp(6px, 1vw, 10px) solid #78350f; }
    .bank-right { border-left: clamp(6px, 1vw, 10px) solid #78350f; }
    
    .bank-header {
        font-size: clamp(16px, 2vw, 19px); font-weight: 700; margin-bottom: 12px; color: #fef08a;
        text-shadow: 0 2px 4px rgba(0,0,0,0.4); text-align: center;
    }

    .river {
        width: 44%;
        background: linear-gradient(180deg, #0284c7 0%, #0369a1 50%, #075985 100%);
        position: relative; overflow: hidden;
    }
    .river-wave-1 {
        position: absolute; width: 200%; height: 100%; opacity: 0.18;
        background: repeating-linear-gradient(45deg, #fff 0px, #fff 14px, transparent 14px, transparent 36px);
        animation: flow 6s linear infinite;
    }
    .river-wave-2 {
        position: absolute; width: 200%; height: 100%; opacity: 0.12;
        background: repeating-linear-gradient(-45deg, #e0f2fe 0px, #e0f2fe 18px, transparent 18px, transparent 42px);
        animation: flow 9s linear infinite reverse;
    }
    @keyframes flow { 0% { transform: translateX(0); } 100% { transform: translateX(-50%); } }

    /* WOODEN BOAT */
    .boat {
        position: absolute; bottom: clamp(20px, 4vh, 35px);
        width: clamp(120px, 25vw, 175px); height: clamp(55px, 10vh, 75px);
        background: linear-gradient(180deg, #a16207 0%, #713f12 100%);
        border: 3px solid #451a03; border-radius: 4px 4px 48px 48px;
        box-shadow: 0 14px 28px rgba(0,0,0,0.5);
        display: flex; justify-content: space-evenly; align-items: center; padding: 0 6px;
        transition: left 1.4s cubic-bezier(0.45, 0, 0.55, 1); z-index: 10;
        animation: floatBob 3s ease-in-out infinite;
    }
    @keyframes floatBob {
        0%, 100% { transform: translateY(0) rotate(0deg); }
        50% { transform: translateY(-5px) rotate(-1.5deg); }
    }
    .boat-left { left: clamp(6px, 1.2vw, 16px); }
    .boat-right { left: calc(100% - clamp(126px, 26.2vw, 191px)); }

    /* CHARACTER AVATAR CARDS */
    .entity-container { display: flex; flex-wrap: wrap; gap: clamp(6px, 1vw, 10px); justify-content: center; width: 100%; }
    
    .avatar-card {
        background: rgba(15, 23, 42, 0.92); backdrop-filter: blur(8px);
        border: 2px solid rgba(255, 255, 255, 0.14); border-radius: 14px;
        padding: clamp(6px, 1vw, 8px) clamp(8px, 1.2vw, 14px); display: flex; align-items: center; gap: 8px;
        font-weight: 700; font-size: clamp(13px, 1.6vw, 15px); color: #f8fafc; cursor: pointer;
        box-shadow: 0 6px 12px rgba(0,0,0,0.3); transition: all 0.2s cubic-bezier(0.34, 1.56, 0.64, 1);
    }
    .avatar-card:hover { transform: translateY(-3px) scale(1.04); border-color: #60a5fa; box-shadow: 0 8px 18px rgba(96, 165, 250, 0.4); }
    .avatar-card:active { transform: scale(0.97); }

    .avatar-badge {
        width: clamp(28px, 3.2vw, 36px); height: clamp(28px, 3.2vw, 36px); border-radius: 50%;
        display: flex; align-items: center; justify-content: center;
        font-size: clamp(15px, 1.8vw, 20px); box-shadow: inset 0 2px 4px rgba(0,0,0,0.3);
    }
    .badge-farmer { background: linear-gradient(135deg, #f59e0b, #b45309); border: 2px solid #fef08a; }
    .badge-wolf { background: linear-gradient(135deg, #ef4444, #991b1b); border: 2px solid #fca5a5; }
    .badge-sheep { background: linear-gradient(135deg, #38bdf8, #0369a1); border: 2px solid #e0f2fe; }
    .badge-cabbage { background: linear-gradient(135deg, #22c55e, #15803d); border: 2px solid #bbf7d0; }

    /* ACTION CONTROLS GRID */
    .controls-wrapper { margin-top: 14px; }
    .controls-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: clamp(8px, 1.2vw, 12px); }
    
    .action-btn {
        background: linear-gradient(180deg, #2563eb 0%, #1d4ed8 100%);
        color: white; border: none; padding: clamp(12px, 1.6vw, 15px) clamp(6px, 1vw, 10px);
        border-radius: 16px; font-size: clamp(14px, 1.8vw, 16px); font-weight: 700; cursor: pointer;
        transition: all 0.15s ease; display: flex; align-items: center; justify-content: center; gap: 8px;
        box-shadow: 0 5px 0 #1e40af, 0 8px 16px rgba(37, 99, 235, 0.35);
    }
    .action-btn:hover:not(:disabled) { transform: translateY(-2px); box-shadow: 0 7px 0 #1e40af; filter: brightness(1.08); }
    .action-btn:active:not(:disabled) { transform: translateY(3px); box-shadow: 0 2px 0 #1e40af; }
    .action-btn:disabled { background: #1e293b !important; color: #475569 !important; cursor: not-allowed; box-shadow: none !important; transform: none !important; }

    /* MODAL OVERLAY */
    .modal-overlay {
        position: fixed; top: 0; left: 0; width: 100%; height: 100%;
        background: rgba(8, 12, 20, 0.88); backdrop-filter: blur(12px);
        display: flex; align-items: center; justify-content: center;
        z-index: 1000; opacity: 0; pointer-events: none; transition: opacity 0.3s ease;
    }
    .modal-overlay.active { opacity: 1; pointer-events: auto; }

    .modal-card {
        background: linear-gradient(180deg, #1e293b 0%, #0f172a 100%);
        border: 2px solid rgba(255, 255, 255, 0.12); border-radius: 26px; padding: 32px 26px;
        width: 90%; max-width: 420px; text-align: center; box-shadow: 0 25px 60px rgba(0,0,0,0.8);
    }
    .modal-icon { font-size: 56px; margin-bottom: 10px; display: inline-block; }
    .modal-title { font-size: 28px; font-weight: 700; margin-bottom: 8px; color: #fff; }
    .modal-desc { font-size: 16px; color: #94a3b8; margin-bottom: 24px; line-height: 1.5; }
    
    .modal-btn {
        width: 100%; padding: 14px; font-size: 16px; font-weight: 700;
        border-radius: 14px; border: none; cursor: pointer; transition: all 0.15s ease;
    }
    .modal-btn-win { background: #16a34a; color: white; box-shadow: 0 4px 0 #15803d; }
    .modal-btn-lose { background: #dc2626; color: white; box-shadow: 0 4px 0 #b91c1c; }

    #confetti-canvas { position: fixed; top: 0; left: 0; width: 100%; height: 100%; pointer-events: none; z-index: 999; }

    /* MOBILE RESPONSIVE LAYOUT BREAKPOINTS */
    @media (max-width: 680px) {
        .top-bar { flex-direction: column; gap: 8px; align-items: stretch; }
        .title-text { justify-content: center; }
        .right-top-controls { justify-content: center; }
        .controls-grid { grid-template-columns: repeat(2, 1fr); gap: 8px; }
        .action-btn { font-size: 14px; padding: 13px 6px; }
    }
</style>
</head>
<body>

<canvas id="confetti-canvas"></canvas>

<div class="top-bar">
    <div class="title-text" id="title-text">🚣 River Crossing</div>
    <div class="right-top-controls">
        <select class="select-control" id="mode-select" onchange="changeMode(this.value)">
            <option value="relaxed">🧘 Relaxed</option>
            <option value="timed">⏱️ Timed (60s)</option>
        </select>

        <select class="select-control" id="speed-select" onchange="changeSpeed(this.value)">
            <option value="normal">🌊 Normal</option>
            <option value="fast">⚡ Fast</option>
        </select>

        <select class="select-control" id="lang-select" onchange="switchLanguage(this.value)">
            <option value="en">🇬🇧 EN</option>
            <option value="mn">🇲🇳 MN</option>
        </select>
        
        <button class="btn btn-audio active" id="btn-sfx" onclick="toggleSfx()">🔊 SFX</button>
        <button class="btn btn-audio" id="btn-bgm" onclick="toggleBgm()">🎵 Music</button>
        <button class="btn btn-audio" onclick="toggleVolumePanel()">🎚️ Vol</button>
        
        <button class="btn btn-undo" id="btn-undo-text" onclick="undoMove()">↩️ Undo</button>
        <button class="btn btn-solve" id="btn-solve-text" onclick="autoSolve()">🤖 Solve</button>
        
        <div class="stat-badge" id="timer-container" style="display:none;">
            ⏱️ <span id="timer-val">60</span>s
        </div>
        <div class="stat-badge">
            <span id="moves-label">Moves:</span> <span id="move-count" style="color:#60a5fa;">0</span>
        </div>
        
        <button class="btn btn-reset" onclick="restartGame()" id="reset-btn-text">🔄 Reset</button>
    </div>
</div>

<!-- FLOATING VOLUME PANEL -->
<div class="volume-panel" id="vol-panel">
    <div class="vol-row">
        <span>🔊 SFX Volume</span>
        <input type="range" id="vol-sfx" min="0" max="1" step="0.1" value="0.8" oninput="setSfxVol(this.value)">
    </div>
    <div class="vol-row">
        <span>🎵 BGM Volume</span>
        <input type="range" id="vol-bgm" min="0" max="1" step="0.1" value="0.5" oninput="setBgmVol(this.value)">
    </div>
</div>

<div id="status-box">💡 Tap a character card or action button to cross!</div>

<!-- BOARD -->
<div class="stage">
    <div class="bank bank-left">
        <div class="bank-header" id="left-header">🌱 Left Shore</div>
        <div class="entity-container" id="left-entities"></div>
    </div>

    <div class="river">
        <div class="river-wave-1"></div>
        <div class="river-wave-2"></div>
        
        <div class="boat boat-left" id="boat">
            <div id="boat-slot-1"></div>
            <div id="boat-slot-2"></div>
        </div>
    </div>

    <div class="bank bank-right">
        <div class="bank-header" id="right-header">🌴 Right Shore</div>
        <div class="entity-container" id="right-entities"></div>
    </div>
</div>

<!-- CONTROLS GRID -->
<div class="controls-wrapper">
    <div class="controls-grid">
        <button class="action-btn" id="btn-alone" onclick="makeMove(null)">🚣 Cross Alone</button>
        <button class="action-btn" id="btn-wolf" onclick="makeMove('Wolf')">🐺 Take Wolf</button>
        <button class="action-btn" id="btn-sheep" onclick="makeMove('Sheep')">🐑 Take Sheep</button>
        <button class="action-btn" id="btn-cabbage" onclick="makeMove('Cabbage')">🥬 Take Cabbage</button>
    </div>
</div>

<!-- POP-UP MODAL CONTAINER -->
<div class="modal-overlay" id="modal-overlay">
    <div class="modal-card">
        <span class="modal-icon" id="modal-icon">🏆</span>
        <div class="modal-title" id="modal-title">Victory!</div>
        <div class="modal-desc" id="modal-desc">You successfully crossed everyone safely!</div>
        <button class="modal-btn" id="modal-action-btn" onclick="restartGame()">🔄 Play Again</button>
    </div>
</div>

<script>
    const EMOJIS = { Farmer: "👨‍🌾", Wolf: "🐺", Sheep: "🐑", Cabbage: "🥬" };
    const BADGE_CLASSES = { Farmer: "badge-farmer", Wolf: "badge-wolf", Sheep: "badge-sheep", Cabbage: "badge-cabbage" };
    
    // --- RE-ENGINEERED AUDIO SYNTHESIZERS ---
    let audioCtx = null;
    let isSfxOn = true, isBgmOn = false, bgmInterval = null;
    let sfxVol = 0.8, bgmVol = 0.5;
    const bgmScale = [261.63, 293.66, 329.63, 392.00, 440.00];

    function initAudio() {
        if (!audioCtx) audioCtx = new (window.AudioContext || window.webkitAudioContext)();
        if (audioCtx.state === 'suspended') audioCtx.resume();
    }

    function toggleVolumePanel() {
        document.getElementById("vol-panel").classList.toggle("active");
    }

    function setSfxVol(val) { sfxVol = parseFloat(val); }
    function setBgmVol(val) { bgmVol = parseFloat(val); }

    function toggleSfx() {
        initAudio(); isSfxOn = !isSfxOn;
        const btn = document.getElementById("btn-sfx");
        btn.className = isSfxOn ? "btn btn-audio active" : "btn btn-audio";
        btn.innerText = isSfxOn ? "🔊 SFX" : "🔇 SFX";
    }

    function toggleBgm() {
        initAudio(); isBgmOn = !isBgmOn;
        const btn = document.getElementById("btn-bgm");
        btn.className = isBgmOn ? "btn btn-audio active" : "btn btn-audio";
        btn.innerText = isBgmOn ? "🎵 Music" : "🔇 Music";
        if (isBgmOn) startBgmLoop(); else stopBgmLoop();
    }

    // 1. BOARDING CLICK (Soft acoustic wood tap)
    function playBoardClick() {
        if (!isSfxOn) return; initAudio();
        let osc = audioCtx.createOscillator(), gain = audioCtx.createGain();
        osc.type = 'sine'; osc.frequency.setValueAtTime(320, audioCtx.currentTime);
        osc.frequency.exponentialRampToValueAtTime(140, audioCtx.currentTime + 0.12);
        gain.gain.setValueAtTime(0.3 * sfxVol, audioCtx.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + 0.12);
        osc.connect(gain); gain.connect(audioCtx.destination);
        osc.start(); osc.stop(audioCtx.currentTime + 0.12);
    }

    // 2. REALISTIC ROWING WATER SPLASH (Low pass water push, no metal swish)
    function playSplashSound() {
        if (!isSfxOn) return; initAudio();
        let bufferSize = audioCtx.sampleRate * 0.65;
        let buffer = audioCtx.createBuffer(1, bufferSize, audioCtx.sampleRate);
        let data = buffer.getChannelData(0);
        for (let i = 0; i < bufferSize; i++) {
            data[i] = (Math.random() * 2 - 1) * Math.sin((i / bufferSize) * Math.PI);
        }
        
        let noise = audioCtx.createBufferSource(); noise.buffer = buffer;
        let filter = audioCtx.createBiquadFilter(); filter.type = 'lowpass';
        filter.frequency.setValueAtTime(320, audioCtx.currentTime);
        filter.frequency.exponentialRampToValueAtTime(100, audioCtx.currentTime + 0.65);
        
        let gain = audioCtx.createGain();
        gain.gain.setValueAtTime(0.01, audioCtx.currentTime);
        gain.gain.linearRampToValueAtTime(0.35 * sfxVol, audioCtx.currentTime + 0.2);
        gain.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + 0.65);
        
        noise.connect(filter); filter.connect(gain); gain.connect(audioCtx.destination);
        noise.start(); noise.stop(audioCtx.currentTime + 0.65);
    }

    // 3. TRIUMPHANT 5-NOTE BRASS VICTORY FANFARE
    function playVictoryFanfare() {
        if (!isSfxOn) return; initAudio();
        const notes = [261.63, 329.63, 392.00, 523.25, 783.99]; // C4, E4, G4, C5, G5
        notes.forEach((freq, i) => {
            let osc = audioCtx.createOscillator(), gain = audioCtx.createGain();
            osc.type = (i === notes.length - 1) ? 'triangle' : 'sine';
            osc.frequency.value = freq;
            let startTime = audioCtx.currentTime + i * 0.12;
            let duration = (i === notes.length - 1) ? 0.75 : 0.3;
            gain.gain.setValueAtTime(0.01, startTime);
            gain.gain.linearRampToValueAtTime(0.3 * sfxVol, startTime + 0.04);
            gain.gain.exponentialRampToValueAtTime(0.001, startTime + duration);
            osc.connect(gain); gain.connect(audioCtx.destination);
            osc.start(startTime); osc.stop(startTime + duration);
        });
    }

    // 4. IMPACTFUL DESCENDING GAME OVER THUD
    function playGameOverBuzz() {
        if (!isSfxOn) return; initAudio();
        const notes = [196.00, 174.61, 164.81, 130.81]; // G3 -> F3 -> E3 -> C3 Thud
        notes.forEach((freq, i) => {
            let osc = audioCtx.createOscillator(), gain = audioCtx.createGain();
            osc.type = 'sawtooth';
            osc.frequency.setValueAtTime(freq, audioCtx.currentTime + i * 0.14);
            gain.gain.setValueAtTime(0.25 * sfxVol, audioCtx.currentTime + i * 0.14);
            gain.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + i * 0.14 + 0.3);
            osc.connect(gain); gain.connect(audioCtx.destination);
            osc.start(audioCtx.currentTime + i * 0.14);
            osc.stop(audioCtx.currentTime + i * 0.14 + 0.3);
        });
    }

    function startBgmLoop() {
        if (bgmInterval) clearInterval(bgmInterval);
        bgmInterval = setInterval(() => {
            if (!isBgmOn || !audioCtx) return;
            let osc = audioCtx.createOscillator(), gain = audioCtx.createGain();
            let freq = bgmScale[Math.floor(Math.random() * bgmScale.length)];
            osc.type = 'sine'; osc.frequency.setValueAtTime(freq, audioCtx.currentTime);
            gain.gain.setValueAtTime(0.04 * bgmVol, audioCtx.currentTime);
            gain.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + 1.2);
            osc.connect(gain); gain.connect(audioCtx.destination);
            osc.start(); osc.stop(audioCtx.currentTime + 1.2);
        }, 750);
    }
    function stopBgmLoop() { if (bgmInterval) clearInterval(bgmInterval); }

    function triggerConfetti() {
        const canvas = document.getElementById('confetti-canvas');
        const ctx = canvas.getContext('2d');
        canvas.width = window.innerWidth; canvas.height = window.innerHeight;
        let particles = [];
        const colors = ['#fef08a', '#60a5fa', '#4ade80', '#f472b6', '#a78bfa'];
        for (let i = 0; i < 90; i++) {
            particles.push({
                x: canvas.width / 2, y: canvas.height / 2,
                vx: (Math.random() - 0.5) * 14, vy: (Math.random() - 0.7) * 14,
                size: Math.random() * 8 + 4, color: colors[Math.floor(Math.random() * colors.length)],
                life: 100
            });
        }
        function render() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            particles.forEach((p, idx) => {
                p.x += p.vx; p.y += p.vy; p.vy += 0.25; p.life--;
                ctx.fillStyle = p.color; ctx.beginPath(); ctx.arc(p.x, p.y, p.size, 0, Math.PI * 2); ctx.fill();
                if (p.life <= 0) particles.splice(idx, 1);
            });
            if (particles.length > 0) requestAnimationFrame(render);
        }
        render();
    }

    const DICT = {
        en: {
            title: "🚣 River Crossing", moves: "Moves:", reset: "🔄 Reset", undo: "↩️ Undo", autoSolve: "🤖 Solve",
            leftShore: "🌱 Left Shore", rightShore: "🌴 Right Shore",
            Farmer: "Farmer", Wolf: "Wolf", Sheep: "Sheep", Cabbage: "Cabbage",
            btnAlone: "🚣 Cross Alone", btnWolf: "🐺 Take Wolf", btnSheep: "🐑 Take Sheep", btnCabbage: "🥬 Take Cabbage",
            initStatus: "💡 Tap a character card or action button to cross!",
            oppositeWarning: "⚠️ {item} is on the other shore! The Farmer isn't there to move it.",
            step1: "⚓ Boarding the boat...", step2: "🌊 Rowing across the river...", step3: "🏝️ Stepping onto the shore...",
            wolfAteSheep: "💀 Game Over! The Wolf ate the Sheep.", sheepAteCabbage: "💀 Game Over! The Sheep ate the Cabbage.",
            timeOutMsg: "⏳ Time ran out! Everyone stranded.",
            victory: "🎉 VICTORY! Solved safely in {moves} moves!", safeTrip: "Safe crossing! Select your next move.",
            resetMsg: "Game reset! Help everyone cross safely.", autoSolving: "🤖 Auto-solving the puzzle...",
            noSolution: "⚠️ No valid moves available from this state. Please reset!",
            modalWinTitle: "🏆 VICTORY!", modalWinDesc: "You transported everyone safely across the river in {moves} moves!", modalWinBtn: "🔄 Play Again",
            modalLoseTitle: "💀 GAME OVER!", modalWolfDesc: "The Wolf was left alone with the Sheep and ate it!", modalSheepDesc: "The Sheep was left alone with the Cabbage and ate it!", modalTimeDesc: "You ran out of time before getting everyone across!", modalLoseBtn: "🔄 Try Again"
        },
        mn: {
            title: "🚣 Гол Гатлах", moves: "Нүүдэл:", reset: "🔄 Дахин", undo: "↩️ Буцах", autoSolve: "🤖 Бодох",
            leftShore: "🌱 Зүүн Эрэг", rightShore: "🌴 Баруун Эрэг",
            Farmer: "Тариачин", Wolf: "Чоно", Sheep: "Хонь", Cabbage: "Байцаа",
            btnAlone: "🚣 Ганцаараа гатлах", btnWolf: "🐺 Чоно авах", btnSheep: "🐑 Хонь авах", btnCabbage: "🥬 Байцаа авах",
            initStatus: "💡 Дүр эсвэл доорх сонголт дээр даран гатална уу!",
            oppositeWarning: "⚠️ {item} өөр эрэг дээр байна! Тариачин тэр эрэг дээр байхгүй байна.",
            step1: "⚓ Завин дээр сууж байна...", step2: "🌊 Гол гаталж байна...", step3: "🏝️ Эрэг дээр бууж байна...",
            wolfAteSheep: "💀 Тоглоом дууслаа! Чоно хонийг идчихлээ.", sheepAteCabbage: "💀 Тоглоом дууслаа! Хонь байцааг идчихлээ.",
            timeOutMsg: "⏳ Цаг дууслаа!",
            victory: "🎉 БАЯР ХҮРГЭЕ! {moves} нүүдлээр амжилттай гаталлаа!", safeTrip: "Амжилттай гаталлаа! Дараагийн нүүдлээ сонгоно уу.",
            resetMsg: "Тоглоом дахин эхэллээ! Бүгдийг аюулгүй гатлуулаарай.", autoSolving: "🤖 Бодлогыг автоматаар бодож байна...",
            noSolution: "⚠️ Энэ байдлаас шийдвэрлэх боломжгүй. Дахин эхлүүлнэ үү!",
            modalWinTitle: "🏆 ЯЛАЛТ!", modalWinDesc: "Та бүгдийг голын цаана {moves} нүүдлээр аюулгүй гаргалаа!", modalWinBtn: "🔄 Дахин тоглох",
            modalLoseTitle: "💀 ТОГЛООМ ДУУСЛАА!", modalWolfDesc: "Чоно хоньтой хамт үлдэж, хонийг барьж идлээ!", modalSheepDesc: "Хонь байцаатай хамт үлдэж, байцааг идчихлээ!", modalTimeDesc: "Цаг дууссан тул амжилтгүй боллоо!", modalLoseBtn: "🔄 Дахин оролдох"
        }
    };

    let currentLang = "en", boatSpeed = 1.4, gameMode = "relaxed", timerVal = 60, timerInterval = null;
    let historyStack = [];
    let gameState = {
        left: ["Farmer", "Wolf", "Sheep", "Cabbage"], right: [], farmerSide: "left",
        moves: 0, isAnimating: false, gameOver: false, modalActive: false, modalType: null,
        statusKey: "initStatus", statusType: "info"
    };

    function changeSpeed(val) {
        const boat = document.getElementById("boat");
        if (val === "fast") {
            boatSpeed = 0.8;
            boat.style.transition = `left 0.8s cubic-bezier(0.45, 0, 0.55, 1)`;
        } else {
            boatSpeed = 1.4;
            boat.style.transition = `left 1.4s cubic-bezier(0.45, 0, 0.55, 1)`;
        }
    }

    function changeMode(val) {
        gameMode = val;
        const timerContainer = document.getElementById("timer-container");
        if (gameMode === "timed") {
            timerContainer.style.display = "flex";
            startTimer();
        } else {
            timerContainer.style.display = "none";
            stopTimer();
        }
    }

    function startTimer() {
        stopTimer(); timerVal = 60;
        document.getElementById("timer-val").innerText = timerVal;
        timerInterval = setInterval(() => {
            if (gameState.gameOver || gameState.isAnimating) return;
            timerVal--;
            document.getElementById("timer-val").innerText = timerVal;
            if (timerVal <= 10) document.getElementById("timer-container").classList.add("timer-warning");
            if (timerVal <= 0) {
                stopTimer();
                setStatus("timeOutMsg", "error"); playGameOverBuzz(); gameState.gameOver = true;
                setTimeout(() => showModal('time'), 400);
            }
        }, 1000);
    }

    function stopTimer() {
        if (timerInterval) clearInterval(timerInterval);
        document.getElementById("timer-container").classList.remove("timer-warning");
    }

    function updateLanguageUI() {
        const lang = DICT[currentLang];
        document.getElementById("title-text").innerText = lang.title;
        document.getElementById("moves-label").innerText = lang.moves;
        document.getElementById("reset-btn-text").innerText = lang.reset;
        document.getElementById("btn-undo-text").innerText = lang.undo;
        document.getElementById("btn-solve-text").innerText = lang.autoSolve;
        document.getElementById("left-header").innerText = lang.leftShore;
        document.getElementById("right-header").innerText = lang.rightShore;
        document.getElementById("btn-alone").innerText = lang.btnAlone;
        document.getElementById("btn-wolf").innerText = lang.btnWolf;
        document.getElementById("btn-sheep").innerText = lang.btnSheep;
        document.getElementById("btn-cabbage").innerText = lang.btnCabbage;
        renderStatus(); renderBoard();
        if (gameState.modalActive) renderModal();
    }

    function switchLanguage(newLang) { currentLang = newLang; updateLanguageUI(); }

    function renderStatus() {
        const box = document.getElementById("status-box");
        let msg = DICT[currentLang][gameState.statusKey] || gameState.statusKey;
        msg = msg.replace("{moves}", gameState.moves);
        box.innerText = msg;
        box.className = gameState.statusType === "error" ? "status-error" : gameState.statusType === "success" ? "status-success" : "";
    }

    function setStatus(key, type) { gameState.statusKey = key; gameState.statusType = type; renderStatus(); }

    function showModal(type) {
        gameState.modalActive = true; gameState.modalType = type; renderModal();
        document.getElementById("modal-overlay").classList.add("active");
        if (type === 'win') triggerConfetti();
    }

    function hideModal() { gameState.modalActive = false; document.getElementById("modal-overlay").classList.remove("active"); }

    function renderModal() {
        const lang = DICT[currentLang];
        const iconEl = document.getElementById("modal-icon"), titleEl = document.getElementById("modal-title");
        const descEl = document.getElementById("modal-desc"), btnEl = document.getElementById("modal-action-btn");

        if (gameState.modalType === 'win') {
            iconEl.innerText = "🏆"; titleEl.innerText = lang.modalWinTitle;
            descEl.innerText = lang.modalWinDesc.replace("{moves}", gameState.moves);
            btnEl.innerText = lang.modalWinBtn; btnEl.className = "modal-btn modal-btn-win";
        } else if (gameState.modalType === 'wolf') {
            iconEl.innerText = "🐺"; titleEl.innerText = lang.modalLoseTitle; descEl.innerText = lang.modalWolfDesc;
            btnEl.innerText = lang.modalLoseBtn; btnEl.className = "modal-btn modal-btn-lose";
        } else if (gameState.modalType === 'sheep') {
            iconEl.innerText = "🐑"; titleEl.innerText = lang.modalLoseTitle; descEl.innerText = lang.modalSheepDesc;
            btnEl.innerText = lang.modalLoseBtn; btnEl.className = "modal-btn modal-btn-lose";
        } else if (gameState.modalType === 'time') {
            iconEl.innerText = "⏳"; titleEl.innerText = lang.modalLoseTitle; descEl.innerText = lang.modalTimeDesc;
            btnEl.innerText = lang.modalLoseBtn; btnEl.className = "modal-btn modal-btn-lose";
        }
    }

    function pushHistory() {
        historyStack.push({
            left: [...gameState.left],
            right: [...gameState.right],
            farmerSide: gameState.farmerSide,
            moves: gameState.moves,
            gameOver: gameState.gameOver,
            statusKey: gameState.statusKey,
            statusType: gameState.statusType
        });
    }

    function undoMove() {
        if (gameState.isAnimating || historyStack.length === 0) return;
        playBoardClick();
        hideModal();
        let prev = historyStack.pop();
        gameState.left = prev.left;
        gameState.right = prev.right;
        gameState.farmerSide = prev.farmerSide;
        gameState.moves = prev.moves;
        gameState.gameOver = prev.gameOver;
        gameState.statusKey = prev.statusKey;
        gameState.statusType = prev.statusType;

        document.getElementById("boat").className = `boat boat-${gameState.farmerSide}`;
        document.getElementById("boat-slot-1").innerHTML = "";
        document.getElementById("boat-slot-2").innerHTML = "";
        renderStatus();
        renderBoard();
    }

    function handleCardTap(item, bankSide) {
        if (gameState.isAnimating || gameState.gameOver) return;

        if (bankSide !== gameState.farmerSide) {
            playGameOverBuzz();
            const itemName = DICT[currentLang][item];
            const warningMsg = DICT[currentLang].oppositeWarning.replace("{item}", itemName);
            const box = document.getElementById("status-box");
            box.innerText = warningMsg;
            box.className = "status-error";
            return;
        }

        if (item === "Farmer") {
            makeMove(null);
        } else {
            makeMove(item);
        }
    }

    function renderAvatarCard(item, bankSide = null) {
        const onclickAttr = bankSide ? `onclick="handleCardTap('${item}', '${bankSide}')"` : '';
        return `<div class="avatar-card" ${onclickAttr}>
            <div class="avatar-badge ${BADGE_CLASSES[item]}">${EMOJIS[item]}</div>
            <span>${DICT[currentLang][item]}</span>
        </div>`;
    }

    function renderBoard() {
        document.getElementById("move-count").innerText = gameState.moves;
        document.getElementById("left-entities").innerHTML = gameState.left.map(item => renderAvatarCard(item, 'left')).join("");
        document.getElementById("right-entities").innerHTML = gameState.right.map(item => renderAvatarCard(item, 'right')).join("");

        const fBank = gameState.farmerSide === "left" ? gameState.left : gameState.right;
        const dis = gameState.isAnimating || gameState.gameOver;
        
        document.getElementById("btn-undo-text").disabled = gameState.isAnimating || historyStack.length === 0;
        document.getElementById("btn-solve-text").disabled = dis;
        document.getElementById("btn-alone").disabled = dis;
        document.getElementById("btn-wolf").disabled = dis || !fBank.includes("Wolf");
        document.getElementById("btn-sheep").disabled = dis || !fBank.includes("Sheep");
        document.getElementById("btn-cabbage").disabled = dis || !fBank.includes("Cabbage");
    }

    async function makeMove(passenger) {
        if (gameState.isAnimating || gameState.gameOver) return;
        pushHistory();
        gameState.isAnimating = true;

        const currentBankList = gameState.farmerSide === "left" ? gameState.left : gameState.right;
        const targetBankList = gameState.farmerSide === "left" ? gameState.right : gameState.left;
        const boatEl = document.getElementById("boat"), slot1 = document.getElementById("boat-slot-1"), slot2 = document.getElementById("boat-slot-2");

        playBoardClick(); setStatus("step1", "info");
        currentBankList.splice(currentBankList.indexOf("Farmer"), 1);
        slot1.innerHTML = renderAvatarCard("Farmer");

        if (passenger) {
            currentBankList.splice(currentBankList.indexOf(passenger), 1);
            slot2.innerHTML = renderAvatarCard(passenger);
        }
        renderBoard(); await new Promise(r => setTimeout(r, 500));

        playSplashSound(); setStatus("step2", "info");
        const nextSide = gameState.farmerSide === "left" ? "right" : "left";
        boatEl.className = `boat boat-${nextSide}`;
        await new Promise(r => setTimeout(r, boatSpeed * 1000));

        playBoardClick(); setStatus("step3", "info");
        slot1.innerHTML = ""; slot2.innerHTML = "";
        targetBankList.push("Farmer"); if (passenger) targetBankList.push(passenger);
        gameState.farmerSide = nextSide; gameState.moves++;
        renderBoard(); await new Promise(r => setTimeout(r, 400));

        gameState.isAnimating = false; checkRules();
    }

    function checkRules() {
        const l = gameState.left, r = gameState.right;
        if ((l.includes("Wolf") && l.includes("Sheep") && !l.includes("Farmer")) || (r.includes("Wolf") && r.includes("Sheep") && !r.includes("Farmer"))) {
            setStatus("wolfAteSheep", "error"); playGameOverBuzz(); gameState.gameOver = true; stopTimer(); setTimeout(() => showModal('wolf'), 450);
        } else if ((l.includes("Sheep") && l.includes("Cabbage") && !l.includes("Farmer")) || (r.includes("Sheep") && r.includes("Cabbage") && !r.includes("Farmer"))) {
            setStatus("sheepAteCabbage", "error"); playGameOverBuzz(); gameState.gameOver = true; stopTimer(); setTimeout(() => showModal('sheep'), 450);
        } else if (r.length === 4) {
            setStatus("victory", "success"); playVictoryFanfare(); gameState.gameOver = true; stopTimer(); setTimeout(() => showModal('win'), 450);
        } else {
            setStatus("safeTrip", "info");
        }
        renderBoard();
    }

    function findSolutionPath(startLeft, startFarmerSide) {
        const ALL = ["Farmer", "Wolf", "Sheep", "Cabbage"];
        const isSafe = (bank) => {
            if (!bank.includes("Farmer")) {
                if (bank.includes("Wolf") && bank.includes("Sheep")) return false;
                if (bank.includes("Sheep") && bank.includes("Cabbage")) return false;
            }
            return true;
        };
        let queue = [{ left: [...startLeft], fSide: startFarmerSide, path: [] }], visited = new Set();
        visited.add([...startLeft].sort().join(',') + '_' + startFarmerSide);

        while (queue.length > 0) {
            let curr = queue.shift(), right = ALL.filter(x => !curr.left.includes(x));
            if (right.length === 4) return curr.path;
            let currentBank = curr.fSide === 'left' ? curr.left : right;
            let options = [null].concat(currentBank.filter(x => x !== 'Farmer'));

            for (let item of options) {
                let nextLeft = [...curr.left], nextRight = [...right];
                let src = curr.fSide === 'left' ? nextLeft : nextRight, dst = curr.fSide === 'left' ? nextRight : nextLeft;
                src.splice(src.indexOf('Farmer'), 1); dst.push('Farmer');
                if (item) { src.splice(src.indexOf(item), 1); dst.push(item); }

                if (isSafe(nextLeft) && isSafe(nextRight)) {
                    let key = [...nextLeft].sort().join(',') + '_' + (curr.fSide === 'left' ? 'right' : 'left');
                    if (!visited.has(key)) {
                        visited.add(key);
                        queue.push({ left: nextLeft, fSide: curr.fSide === 'left' ? 'right' : 'left', path: curr.path.concat([item]) });
                    }
                }
            }
        }
        return null;
    }

    async function autoSolve() {
        if (gameState.isAnimating || gameState.gameOver) return;
        let path = findSolutionPath(gameState.left, gameState.farmerSide);
        if (!path || path.length === 0) { setStatus("noSolution", "error"); playGameOverBuzz(); return; }
        setStatus("autoSolving", "info");
        for (let item of path) {
            if (gameState.gameOver) break;
            await makeMove(item); await new Promise(r => setTimeout(r, 300));
        }
    }

    function restartGame() {
        hideModal(); playBoardClick();
        historyStack = [];
        gameState = {
            left: ["Farmer", "Wolf", "Sheep", "Cabbage"], right: [], farmerSide: "left",
            moves: 0, isAnimating: false, gameOver: false, modalActive: false, modalType: null,
            statusKey: "resetMsg", statusType: "info"
        };
        document.getElementById("boat").className = "boat boat-left";
        document.getElementById("boat-slot-1").innerHTML = ""; document.getElementById("boat-slot-2").innerHTML = "";
        if (gameMode === "timed") startTimer();
        updateLanguageUI();
    }

    updateLanguageUI();
</script>
</body>
</html>
"""

components.html(game_html, height=750, scrolling=False)