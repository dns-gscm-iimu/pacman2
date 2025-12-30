import streamlit as st
import streamlit.components.v1 as components
import base64
import os

st.set_page_config(page_title="HBD Vishesh", layout="centered", initial_sidebar_state="collapsed")

# Image Handling
def get_base64_of_bin_file(bin_file):
    try:
        with open(bin_file, 'rb') as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except FileNotFoundError:
        return None

image_path = 'vishesh.jpg'
b64_image = get_base64_of_bin_file(image_path)
default_image_js = f"'{f'data:image/jpeg;base64,{b64_image}'}'" if b64_image else "null"

# Custom CSS for Mario Theme
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap');

    /* Mario World Background (CSS Painting) */
    .stApp {
        background-color: #5c94fc; /* Sky Blue */
        background-image: 
            /* Clouds */
            radial-gradient(circle, white 50%, transparent 50%),
            radial-gradient(circle, white 50%, transparent 50%),
            /* Hills - simplified as green circles at bottom */
            radial-gradient(ellipse at 50% 120%, #00a800 50%, transparent 50%),
            radial-gradient(ellipse at 20% 120%, #00a800 40%, transparent 40%),
            radial-gradient(ellipse at 80% 120%, #00a800 40%, transparent 40%);
        background-size: 150px 100px, 200px 120px, 100% 100%, 100% 100%, 100% 100%;
        background-position: 10% 20%, 80% 10%, 0 0, 0 0, 0 0;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }
    
    /* Footer Bricks Pattern */
    .stApp::after {
        content: "";
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        height: 60px;
        background-color: #883000;
        background-image: 
            linear-gradient(#000 2px, transparent 2px),
            linear-gradient(90deg, #000 2px, transparent 2px);
        background-size: 30px 30px;
        z-index: -1;
    }

    /* Floating Header - Multi-line */
    @keyframes floatText {
        0% { transform: translateX(100%); }
        100% { transform: translateX(-100%); }
    }

    .hbd-container {
        width: 100%;
        overflow: hidden;
        white-space: nowrap;
        background: rgba(0,0,0,0.6);
        border: 4px solid #fff;
        padding: 10px 0;
        margin-bottom: 20px;
        text-align: center;
    }

    .hbd-header {
        font-family: 'Press Start 2P', cursive;
        color: #FFD700;
        text-shadow: 4px 4px #000;
        font-size: 1.2em;
        line-height: 1.5;
        white-space: pre-wrap; /* Allow wrapping/newlines */
        display: inline-block;
        /* float effect logic update for multiline blocks is tricky, 
           simpler to just have it static or marquee. Request was 'float'.
           Let's marquee the whole block.
        */
        animation: floatText 15s linear infinite;
        padding-left: 100%;
    }
    
    .level-up {
        color: #ff4d4d;
        display: block; /* Force new line */
        font-size: 1.4em;
    }

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>

<div class="hbd-container">
    <div class="hbd-header">
        HAPPY BIRTHDAY VISHESH!<br>
        <span class="level-up">LEVEL UP! 🍄</span>
    </div>
</div>
""", unsafe_allow_html=True)

# HTML/JS Game Code
game_html = f"""
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no" />
<style>
    @import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap');
    
    body {{
        touch-action: none;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: flex-start;
        font-family: 'Press Start 2P', cursive;
        background-color: transparent;
        color: white;
        margin: 0;
        padding: 0;
        height: 100vh;
        overflow: hidden;
    }}
    canvas {{
        border: 6px solid #fff;
        background-color: rgba(0,0,0,0.8); /* Semi-transparent black */
        box-shadow: 0 0 20px rgba(0,0,0,0.5);
        width: 90vw;
        height: 90vw;
        max-width: 400px;
        max-height: 400px;
        margin-top: 10px;
        image-rendering: pixelated;
    }}
    #score {{
        font-size: 16px;
        margin-top: 5px;
        color: #fff;
        text-shadow: 2px 2px #000;
        background: #000;
        padding: 8px;
        border: 2px solid #fff;
    }}
    
    /* Joystick */
    #joystick-container {{
        margin-top: 15px;
        display: grid;
        grid-template-columns: 60px 60px 60px;
        grid-template-rows: 60px 60px;
        gap: 5px;
    }}
    .d-btn {{
        width: 60px;
        height: 60px;
        background-color: #d32f2f; /* NES Red Buttons */
        border: 4px solid #8b0000;
        border-radius: 5px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 24px;
        cursor: pointer;
        color: #fff;
        box-shadow: 0 4px #5a0000;
        -webkit-tap-highlight-color: transparent;
    }}
    .d-btn:active {{
        box-shadow: 0 0 #000;
        transform: translateY(4px);
    }}
    .spacer {{ pointer-events: none; }}
</style>
</head>
<body>

<div id="score">SCORE: 0</div>
<canvas id="gameCanvas" width="400" height="400"></canvas>

<div id="joystick-container">
    <div class="spacer"></div>
    <div class="d-btn" id="btn-up">▲</div>
    <div class="spacer"></div>
    <div class="d-btn" id="btn-left">◀</div>
    <div class="d-btn" id="btn-down">▼</div>
    <div class="d-btn" id="btn-right">▶</div>
</div>

<script>
const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');

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

// Palettes
const c_wall = "#0055aa"; // Brighter Blue Walls
const c_dot = "#FFD700";

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
            player.x = c;
            player.y = r;
            map[r][c] = 2;
        }}
    }}
}}

const AudioContext = window.AudioContext || window.webkitAudioContext;
const audioCtx = new AudioContext();

function beep(freq, duration, type='square') {{
    if(audioCtx.state === 'suspended') audioCtx.resume();
    const osc = audioCtx.createOscillator();
    const gain = audioCtx.createGain();
    osc.type = type;
    osc.frequency.setValueAtTime(freq, audioCtx.currentTime);
    osc.connect(gain);
    gain.connect(audioCtx.destination);
    osc.start();
    osc.stop(audioCtx.currentTime + duration);
    gain.gain.setValueAtTime(0.1, audioCtx.currentTime);
    gain.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + duration);
}}

function playStartTune() {{
    let t = audioCtx.currentTime;
    beep(660, 0.1); 
    setTimeout(() => beep(990, 0.4), 150);
}}

function playWinTune() {{
    let notes = [523, 659, 783, 1046, 783, 1046]; 
    notes.forEach((freq, i) => {{
        setTimeout(() => beep(freq, 0.2), i * 150);
    }});
}}

function speakOfCourse() {{
    if (window.speechSynthesis) {{
        window.speechSynthesis.cancel();
        let u = new SpeechSynthesisUtterance("Of course");
        u.pitch = 0.1; 
        u.rate = 1.3;
        window.speechSynthesis.speak(u);
    }}
}}

function canMove(x, y) {{
    if (y < 0 || y >= ROWS || x < 0 || x >= COLS) return false;
    return map[y][x] !== 1;
}}

function moveOneStep(dx, dy) {{
    if(audioCtx.state === 'suspended') audioCtx.resume();

    if (canMove(player.x + dx, player.y + dy)) {{
        player.x += dx;
        player.y += dy;
        
        if (map[player.y][player.x] === 0) {{
            map[player.y][player.x] = 2; 
            score += 10;
            totalDots--;
            scoreEl.innerText = "SCORE: " + score;
            speakOfCourse();
            
            if (totalDots <= 0) {{
                playWinTune();
                scoreEl.innerText = "YOU WON! SCORE: " + score;
            }}
        }}
    }}
    draw();
}}

// Controls
const up = () => moveOneStep(0, -1);
const down = () => moveOneStep(0, 1);
const left = () => moveOneStep(-1, 0);
const right = () => moveOneStep(1, 0);

document.getElementById('btn-up').addEventListener('touchstart', (e) => {{ e.preventDefault(); up(); }});
document.getElementById('btn-down').addEventListener('touchstart', (e) => {{ e.preventDefault(); down(); }});
document.getElementById('btn-left').addEventListener('touchstart', (e) => {{ e.preventDefault(); left(); }});
document.getElementById('btn-right').addEventListener('touchstart', (e) => {{ e.preventDefault(); right(); }});

document.getElementById('btn-up').addEventListener('click', up);
document.getElementById('btn-down').addEventListener('click', down);
document.getElementById('btn-left').addEventListener('click', left);
document.getElementById('btn-right').addEventListener('click', right);

window.addEventListener('keydown', e => {{
    if(["ArrowUp","ArrowDown","ArrowLeft","ArrowRight"].indexOf(e.code) > -1) e.preventDefault();
    switch(e.key) {{
        case 'ArrowUp': up(); break;
        case 'ArrowDown': down(); break;
        case 'ArrowLeft': left(); break;
        case 'ArrowRight': right(); break;
    }}
}});


function draw() {{
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    
    // Tiles
    for(let r=0; r<ROWS; r++) {{
        for(let c=0; c<COLS; c++) {{
            let type = map[r][c];
            let x = c * TILE_SIZE;
            let y = r * TILE_SIZE;
            
            if (type === 1) {{
                ctx.fillStyle = c_wall; 
                ctx.fillRect(x, y, TILE_SIZE, TILE_SIZE);
            }} else if (type === 0) {{
                ctx.fillStyle = c_dot;
                ctx.beginPath();
                ctx.arc(x + TILE_SIZE/2, y + TILE_SIZE/2, 4, 0, Math.PI*2); 
                ctx.fill();
            }}
        }}
    }}

    // Player
    let px = player.x * TILE_SIZE;
    let py = player.y * TILE_SIZE;
    
    if (customImage && customImage.complete) {{
        ctx.save();
        ctx.beginPath();
        ctx.arc(px + TILE_SIZE/2, py + TILE_SIZE/2, TILE_SIZE/2 - 2, 0, Math.PI*2);
        ctx.clip();
        ctx.drawImage(customImage, px, py, TILE_SIZE, TILE_SIZE);
        ctx.restore();
    }} else {{
        ctx.fillStyle = "yellow";
        ctx.beginPath();
        ctx.arc(px + TILE_SIZE/2, py + TILE_SIZE/2, TILE_SIZE/2 - 2, 0, Math.PI*2);
        ctx.fill();
    }}
}}

customImage.onload = draw;
// Helper for audio unlock
const initAudio = () => {{ if(audioCtx.state==='suspended') audioCtx.resume().then(playStartTune); }};
window.addEventListener('click', initAudio, {{once:true}});
window.addEventListener('touchstart', initAudio, {{once:true}});
setTimeout(draw, 500);

</script>
</body>
</html>
"""

components.html(game_html, height=850, scrolling=False)
