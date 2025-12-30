import streamlit as st
import streamlit.components.v1 as components
import base64
import os

st.set_page_config(page_title="HBD Vishesh", layout="wide", initial_sidebar_state="collapsed")

# Image & Audio Handling
def get_base64_of_bin_file(bin_file):
    try:
        with open(bin_file, 'rb') as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except FileNotFoundError:
        return None

# 1. VISUAL
image_path = 'vishesh.jpg'
b64_image = get_base64_of_bin_file(image_path)
default_image_js = f"'{f'data:image/jpeg;base64,{b64_image}'}'" if b64_image else "null"

# 2. AUDIO (Balicha 5.m4a)
audio_path = 'Balicha 5.m4a'
b64_audio = get_base64_of_bin_file(audio_path)
# Fallback if file missing (shouldn't happen given it's there, but good practice)
custom_audio_js = f"'{f'data:audio/mp4;base64,{b64_audio}'}'" if b64_audio else "null"

# Custom CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap');

    .stAppHeader, footer, .stToolbar {display: none !important;}
    .block-container {
        padding: 0 !important;
        margin: 0 !important;
        max-width: 100% !important;
    }
    
    .stApp {
        background-color: #5c94fc; 
        overflow: hidden; 
    }
    
    .bg-layer {
        position: fixed;
        top: 0; left: 0; width: 100%; height: 100%;
        background-image: 
            radial-gradient(circle, white 50%, transparent 50%),
            radial-gradient(circle, white 50%, transparent 50%);
        background-size: 150px 100px, 200px 120px;
        background-position: 10% 20%, 80% 10%;
        background-repeat: no-repeat;
        z-index: 0;
        pointer-events: none;
    }
</style>
<div class="bg-layer"></div>
""", unsafe_allow_html=True)

# HTML/JS Game Code
game_html = f"""
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover" />
<style>
    @import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap');
    
    html, body {{
        margin: 0;
        padding: 0;
        width: 100vw;
        height: 100vh;
        overflow: hidden;
        background-color: transparent;
        font-family: 'Press Start 2P', cursive;
        display: flex;
        flex-direction: column;
        user-select: none;
        -webkit-user-select: none;
        touch-action: none;
    }}

    .section {{
        width: 100%;
        display: flex;
        align-items: center;
        justify-content: center;
        position: relative;
        z-index: 10;
        box-sizing: border-box;
    }}

    #section-header {{
        height: 25vh;
        flex-direction: column;
        text-align: center;
        overflow: hidden;
    }}

    #section-game {{
        height: 50vh;
        background: transparent; 
    }}

    #section-controls {{
        height: 25vh;
        padding-bottom: 20px;
    }}

    .hbd-text {{
        color: #FFD700;
        text-shadow: 3px 3px #000;
        font-size: 5vw; 
        line-height: 1.4;
        display: inline-block;
        white-space: nowrap;
        animation: floatText 10s linear infinite; 
    }}
    
    @keyframes floatText {{
        0% {{ transform: translateX(100%); }}
        100% {{ transform: translateX(-100%); }}
    }}

    .level-up {{ 
        color: #ff3333; 
        font-size: 4vw; 
        display: block; 
        margin-top: 5px; 
    }}
    
    .instruction-text {{
        color: #fff;
        font-size: 2.5vw; 
        display: block;
        margin-top: 5px;
        text-shadow: 1px 1px #000;
        font-family: monospace; 
        opacity: 0.9;
    }}

    canvas {{
        border: 4px solid #fff;
        background-color: rgba(0,0,0,0.85); 
        box-shadow: 0 4px 10px rgba(0,0,0,0.5);
        width: auto;
        height: 90%; 
        aspect-ratio: 1/1;
        image-rendering: pixelated;
    }}

    #score {{
        position: absolute;
        top: 2px;
        left: 50%;
        transform: translateX(-50%);
        font-size: 10px;
        color: #fff;
        text-shadow: 1px 1px #000;
        background: rgba(0,0,0,0.8);
        padding: 4px 6px;
        border: 1px solid #fff;
        z-index: 20;
    }}

    /* Hidden Audio Status */
    #audio-status {{ display: none; }}

    #joystick-container {{
        display: grid;
        grid-template-columns: 60px 60px 60px;
        grid-template-rows: 60px 60px;
        gap: 5px;
    }}
    @media (max-height: 600px) {{
        #joystick-container {{ transform: scale(0.85); }}
    }}

    .d-btn {{
        width: 60px;
        height: 60px;
        background-color: #cc0000;
        border: 3px solid #8b0000;
        border-radius: 8px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 20px;
        cursor: pointer;
        color: #fff;
        text-shadow: 1px 1px 0 #000;
        box-shadow: 0 4px #5a0000;
    }}
    .d-btn:active {{
        transform: translateY(4px);
        box-shadow: 0 0 #000;
        background-color: #ff3333;
    }}
    .spacer {{ pointer-events: none; }}
    
</style>
</head>
<body>

<div id="section-header" class="section">
    <div class="hbd-text">HAPPY BIRTHDAY VISHESH!</div>
    <span class="level-up">LEVEL UP! 🍄</span>
    <span class="instruction-text">Swipe / Use Joystick to move Vishesh</span>
</div>

<div id="section-game" class="section">
    <div id="score">SCORE: 0</div>
    <div id="audio-status">Audio: Tap to Enable</div>
    <canvas id="gameCanvas" width="400" height="400"></canvas>
</div>

<div id="section-controls" class="section">
    <div id="joystick-container">
        <div class="spacer"></div>
        <div class="d-btn" id="btn-up">▲</div>
        <div class="spacer"></div>
        <div class="d-btn" id="btn-left">◀</div>
        <div class="d-btn" id="btn-down">▼</div>
        <div class="d-btn" id="btn-right">▶</div>
    </div>
</div>

<script>
// Contexts
const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');

// --- AUDIO SYSTEM (Custom File) ---
const customAudioSrc = {custom_audio_js};
// Preload 2 copies to allow overlapping overlapping sounds if user is fast
const soundPool = [];
const POOL_SIZE = 3;

if(customAudioSrc) {{
    for(let i=0; i<POOL_SIZE; i++) {{
        let a = new Audio(customAudioSrc);
        a.load(); 
        soundPool.push(a);
    }}
}}

// Helper to get next available sound
let poolIdx = 0;
function playCustomSound() {{
    if(soundPool.length > 0) {{
        let s = soundPool[poolIdx];
        s.currentTime = 0;
        // Important: .play() returns a promise.
        // We catch errors to avoid unhandled promise rejections if locked.
        s.play().catch(e => console.log("Audio locked or error", e));
        
        poolIdx = (poolIdx + 1) % POOL_SIZE;
    }}
}}

// Unlocker Logic (Still needed even for 'new Audio()')
// Mobile Safari/Chrome suspends Audio elements until first interaction.
let unlocked = false;
function globalUnlock() {{
    if(!unlocked) {{
        // Play one silent sound from pool to unlock them?
        // Or just resume AudioContext (good practice for general audio)
        // Actually for HTML5 Audio, usually one interaction is enough if we play() inside it.
        // But let's try to 'warm up' the pool 
        if(soundPool.length > 0) {{
            // We just need to trigger this logic once inside a user event
            soundPool.forEach(s => {{
                // Trick to unlock: play and pause immediately?
                // Or just trust that subsequent calls will work.
                // Best trick: play muted, then unmute?
                // Let's rely on the direct call in 'moveOneStep' which IS a user event (touchstart/click)
                // BUT 'swipe' logic is async (touchend), so we might lose the "user gesture" token.
                // So we MUST unlock here.
                s.muted = true;
                s.play().then(() => {{ s.pause(); s.currentTime=0; s.muted=false; }}).catch(e=>{{}});
            }});
        }}
        unlocked = true;
    }}
}}
document.body.addEventListener('touchstart', globalUnlock, {{passive: false}});
document.body.addEventListener('click', globalUnlock);
document.body.addEventListener('keydown', globalUnlock);

// Init Image
let customImage = null;
const uploadedImageSrc = {default_image_js};
if (uploadedImageSrc) {{
    customImage = new Image();
    customImage.src = uploadedImageSrc;
}}

const ROWS = 15;
const COLS = 15;
const TILE_SIZE = canvas.width / COLS; 
let totalDots = 0;

const map = [
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,0,0,0,1,0,0,0,0,0,1,0,0,0,1],
    [1,0,1,1,1,0,1,1,1,0,1,1,1,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,1,1,0,1,1,0,1,1,0,1,1,0,1],
    [1,0,0,0,0,1,2,2,2,1,0,0,0,0,1],
    [1,1,1,1,0,1,2,9,2,1,0,1,1,1,1],
    [1,0,0,0,0,1,2,2,2,1,0,0,0,0,1],
    [1,0,1,1,0,1,1,1,1,1,0,1,1,0,1],
    [1,0,0,1,0,0,0,0,0,0,0,1,0,0,1],
    [1,1,0,1,0,1,1,0,1,1,0,1,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,1,1,1,0,1,1,1,0,1,1,1,0,1],
    [1,0,0,0,0,0,0,1,0,0,0,0,0,0,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
];

let player = {{ x: 7, y: 7 }};
let score = 0;
const scoreEl = document.getElementById('score');

for(let r=0; r<ROWS; r++) {{
    for(let c=0; c<COLS; c++) {{
        if(map[r][c] === 0) totalDots++;
        if(map[r][c] === 9) {{
            player.x = c; player.y = r; map[r][c] = 2;
        }}
    }}
}}

function canMove(x, y) {{
    if (y < 0 || y >= ROWS || x < 0 || x >= COLS) return false;
    return map[y][x] !== 1;
}}

function moveOneStep(dx, dy) {{
    if (canMove(player.x + dx, player.y + dy)) {{
        player.x += dx;
        player.y += dy;
        
        if (map[player.y][player.x] === 0) {{
            map[player.y][player.x] = 2; 
            score += 10;
            totalDots--;
            if(scoreEl) scoreEl.innerText = "SCORE: " + score;
            
            playCustomSound(); 
            
            if (totalDots <= 0) {{
                if(scoreEl) scoreEl.innerText = "YOU WON! SCORE: " + score;
            }}
        }}
    }}
}}

const up = () => moveOneStep(0, -1);
const down = () => moveOneStep(0, 1);
const left = () => moveOneStep(-1, 0);
const right = () => moveOneStep(1, 0);

// CONTROLS
const opts = {{passive: false}};
const btnAdd = (id, fn) => {{
    const el = document.getElementById(id);
    if(el) {{
        el.addEventListener('touchstart', (e) => {{ e.preventDefault(); fn(); }}, opts);
        el.addEventListener('mousedown', (e) => {{ e.preventDefault(); fn(); }});
    }}
}};
btnAdd('btn-up', up);
btnAdd('btn-down', down);
btnAdd('btn-left', left);
btnAdd('btn-right', right);

window.addEventListener('keydown', (e) => {{
    if(e.key === "ArrowUp") up();
    if(e.key === "ArrowDown") down();
    if(e.key === "ArrowLeft") left();
    if(e.key === "ArrowRight") right();
}});

// Swipe
let touchStartX = 0;
let touchStartY = 0;
const SWIPE_THRESHOLD = 30; 
document.addEventListener('touchstart', function(e) {{
    globalUnlock(); 
    if(e.target.closest('.d-btn')) return;
    touchStartX = e.changedTouches[0].screenX;
    touchStartY = e.changedTouches[0].screenY;
}}, false);

document.addEventListener('touchend', function(e) {{
    if(e.target.closest('.d-btn')) return;
    let touchEndX = e.changedTouches[0].screenX;
    let touchEndY = e.changedTouches[0].screenY;
    let diffX = touchEndX - touchStartX;
    let diffY = touchEndY - touchStartY;
    
    if (Math.abs(diffX) > Math.abs(diffY)) {{
        if (Math.abs(diffX) > SWIPE_THRESHOLD) {{
            if (diffX > 0) right(); else left();
        }}
    }} else {{
        if (Math.abs(diffY) > SWIPE_THRESHOLD) {{
            if (diffY > 0) down(); else up();
        }}
    }}
}}, false);

// Draw
function draw() {{
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    for(let r=0; r<ROWS; r++) {{
        for(let c=0; c<COLS; c++) {{
            let type = map[r][c];
            let x = c * TILE_SIZE;
            let y = r * TILE_SIZE;
            if (type === 1) {{ 
                ctx.fillStyle = "#0047AB"; ctx.fillRect(x, y, TILE_SIZE, TILE_SIZE);
            }} else if (type === 0) {{
                ctx.fillStyle = "#FFD700"; ctx.beginPath();
                ctx.arc(x + TILE_SIZE/2, y + TILE_SIZE/2, 4, 0, Math.PI*2); ctx.fill();
            }}
        }}
    }}
    let px = player.x * TILE_SIZE;
    let py = player.y * TILE_SIZE;
    if (customImage && customImage.complete) {{
        ctx.save(); ctx.beginPath();
        ctx.arc(px + TILE_SIZE/2, py + TILE_SIZE/2, TILE_SIZE/2 - 1, 0, Math.PI*2);
        ctx.clip(); ctx.drawImage(customImage, px, py, TILE_SIZE, TILE_SIZE); ctx.restore();
    }} else {{
        ctx.fillStyle = "yellow"; ctx.beginPath();
        ctx.arc(px + TILE_SIZE/2, py + TILE_SIZE/2, TILE_SIZE/2 - 1, 0, Math.PI*2); ctx.fill();
    }}
    requestAnimationFrame(draw);
}}
draw();
</script>
</body>
</html>
"""

components.html(game_html, height=1000, scrolling=False)
