import streamlit as st
import streamlit.components.v1 as components
import base64
import os

st.set_page_config(page_title="HBD Vishesh", layout="wide", initial_sidebar_state="collapsed")

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

# Custom CSS for Fullscreen Mobile
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap');

    /* Global reset for Streamlit */
    .stAppHeader, footer, .stToolbar {display: none !important;}
    .block-container {
        padding: 0 !important;
        margin: 0 !important;
        max-width: 100% !important;
    }
    
    .stApp {
        background-color: #5c94fc; /* Sky Blue */
        overflow: hidden; /* Prevent Global Scroll */
        position: fixed;
        width: 100%;
        height: 100%;
    }
    
    /* Background Elements */
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
        overflow: hidden; /* No scroll */
        background-color: transparent;
        font-family: 'Press Start 2P', cursive;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: flex-start;
        user-select: none;
        -webkit-user-select: none;
        touch-action: none;
    }}

    /* Header */
    .header-container {{
        width: 100%;
        text-align: center;
        margin-top: 10px;
        margin-bottom: 5px;
        z-index: 10;
        /* No scroll animation for banner - Instant show */
    }}
    .hbd-text {{
        color: #FFD700;
        text-shadow: 3px 3px #000;
        font-size: 16px; /* Optimized for iPhone 12 width */
        line-height: 1.5;
    }}
    .level-up {{ color: #ff3333; font-size: 14px; display: block; margin-top: 5px; }}

    /* Canvas */
    canvas {{
        border: 4px solid #fff;
        background-color: rgba(0,0,0,0.85);
        box-shadow: 0 4px 10px rgba(0,0,0,0.5);
        width: 90vw; /* Fit width */
        height: 90vw; /* Square */
        max-width: 380px; 
        max-height: 380px;
        image-rendering: pixelated;
        z-index: 10;
    }}

    #score {{
        font-size: 14px;
        margin: 5px 0;
        color: #fff;
        text-shadow: 2px 2px #000;
        background: #000;
        padding: 4px 8px;
        border: 2px solid #fff;
        z-index: 10;
    }}
    
    /* Joystick - Pushed to bottom */
    #joystick-container {{
        margin-top: auto; /* Push to bottom */
        margin-bottom: 30px; /* Safe area from bottom edge */
        display: grid;
        grid-template-columns: 60px 60px 60px;
        grid-template-rows: 60px 60px;
        gap: 8px;
        z-index: 10;
        touch-action: manipulation;
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
        box-shadow: 0 4px #5a0000;
    }}
    .d-btn:active {{
        transform: translateY(4px);
        box-shadow: 0 0 #000;
        background-color: #ff3333;
    }}
    .spacer {{ pointer-events: none; }}
    
    #start-overlay {{
        position: absolute;
        top: 0; left: 0; width: 100%; height: 100%;
        background: rgba(0,0,0,0.7);
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 100;
        flex-direction: column;
    }}
    #start-btn {{
        background: #00AA00;
        color: white;
        font-family: 'Press Start 2P';
        padding: 20px;
        border: 4px solid #fff;
        font-size: 16px;
        animation: blink 1s infinite;
    }}
    @keyframes blink {{ 0% {{opacity: 1;}} 50% {{opacity: 0.5;}} 100% {{opacity: 1;}} }}

</style>
</head>
<body>

<div id="start-overlay" onclick="startGame()">
    <div id="start-btn">TAP TO START</div>
</div>

<div class="header-container">
    <div class="hbd-text">HAPPY BIRTHDAY VISHESH!</div>
    <span class="level-up">LEVEL UP! 🍄</span>
</div>

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
    customImage.onload = () => draw(); 
}}

const ROWS = 15;
const COLS = 15;
const TILE_SIZE = canvas.width / COLS; 
let totalDots = 0;
let gameRunning = false;

// Map
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

// Init
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

// Audio
const AudioContext = window.AudioContext || window.webkitAudioContext;
const audioCtx = new AudioContext();

function beep(freq, duration) {{
    const osc = audioCtx.createOscillator();
    const gain = audioCtx.createGain();
    osc.type = 'square';
    osc.frequency.setValueAtTime(freq, audioCtx.currentTime);
    osc.connect(gain);
    gain.connect(audioCtx.destination);
    osc.start();
    osc.stop(audioCtx.currentTime + duration);
    gain.gain.setValueAtTime(0.1, audioCtx.currentTime);
}}

function speakOfCourse() {{
    const u = new SpeechSynthesisUtterance("Of course");
    u.pitch = 0.5; // Adjusted to be less deep, more audible on phone
    u.rate = 1.1;
    u.volume = 1.0;
    window.speechSynthesis.cancel();
    window.speechSynthesis.speak(u);
}}

function startGame() {{
    document.getElementById('start-overlay').style.display = 'none';
    if(audioCtx.state === 'suspended') audioCtx.resume();
    // Warm up speech synthesis
    window.speechSynthesis.cancel();
    gameRunning = true;
    draw();
}}

function canMove(x, y) {{
    if (y < 0 || y >= ROWS || x < 0 || x >= COLS) return false;
    return map[y][x] !== 1;
}}

function moveOneStep(dx, dy) {{
    if(!gameRunning) return;
    
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

const opts = {{passive: false}};
document.getElementById('btn-up').addEventListener('touchstart', (e) => {{ e.preventDefault(); up(); }}, opts);
document.getElementById('btn-down').addEventListener('touchstart', (e) => {{ e.preventDefault(); down(); }}, opts);
document.getElementById('btn-left').addEventListener('touchstart', (e) => {{ e.preventDefault(); left(); }}, opts);
document.getElementById('btn-right').addEventListener('touchstart', (e) => {{ e.preventDefault(); right(); }}, opts);

// Prevent double firing on some devices
document.getElementById('btn-up').addEventListener('mousedown', up);
document.getElementById('btn-down').addEventListener('mousedown', down);
document.getElementById('btn-left').addEventListener('mousedown', left);
document.getElementById('btn-right').addEventListener('mousedown', right);


function draw() {{
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    
    // Tiles
    for(let r=0; r<ROWS; r++) {{
        for(let c=0; c<COLS; c++) {{
            let type = map[r][c];
            let x = c * TILE_SIZE;
            let y = r * TILE_SIZE;
            
            if (type === 1) {{
                // Wall
                ctx.fillStyle = "#0047AB"; 
                ctx.fillRect(x, y, TILE_SIZE, TILE_SIZE);
            }} else if (type === 0) {{
                // Dot
                ctx.fillStyle = "#FFD700";
                ctx.beginPath();
                ctx.arc(x + TILE_SIZE/2, y + TILE_SIZE/2, 4, 0, Math.PI*2); // Bigger dots
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
        ctx.arc(px + TILE_SIZE/2, py + TILE_SIZE/2, TILE_SIZE/2 - 1, 0, Math.PI*2);
        ctx.clip();
        ctx.drawImage(customImage, px, py, TILE_SIZE, TILE_SIZE);
        ctx.restore();
    }} else {{
        ctx.fillStyle = "yellow";
        ctx.beginPath();
        ctx.arc(px + TILE_SIZE/2, py + TILE_SIZE/2, TILE_SIZE/2 - 1, 0, Math.PI*2);
        ctx.fill();
    }}
}}

// Draw initially
setTimeout(draw, 200);

</script>
</body>
</html>
"""

# Increase height to fill iframe but disable scrolling
components.html(game_html, height=850, scrolling=False)
