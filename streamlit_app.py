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

# Custom CSS to force Fullscreen
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
        position: fixed;
        width: 100%;
        height: 100%;
        top: 0; left: 0;
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

    /* 
       LAYOUT 25 / 50 / 25 
       Using vh units and flexbox to guarantee ratios
    */
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
    }}

    #section-game {{
        height: 50vh;
    }}

    #section-controls {{
        height: 25vh;
        padding-bottom: 20px;
    }}

    /* Typography */
    .hbd-text {{
        color: #FFD700;
        text-shadow: 3px 3px #000;
        font-size: 5vw; /* Scales with screen width */
        line-height: 1.4;
    }}
    .level-up {{ 
        color: #ff3333; 
        font-size: 4vw; 
        display: block; 
        margin-top: 5px; 
    }}

    /* Canvas */
    canvas {{
        border: 4px solid #fff;
        background-color: rgba(0,0,0,0.85);
        box-shadow: 0 4px 10px rgba(0,0,0,0.5);
        /* 
           Crucial: Fit within the 50vh container.
           Also respect width.
        */
        height: 90%; 
        max-width: 95vw;
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

    /* Joystick */
    #joystick-container {{
        display: grid;
        grid-template-columns: 60px 60px 60px;
        grid-template-rows: 60px 60px;
        gap: 5px;
    }}
    /* Make buttons slightly smaller if screen is short */
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
        box-shadow: 0 4px #5a0000;
    }}
    .d-btn:active {{
        transform: translateY(4px);
        box-shadow: 0 0 #000;
        background-color: #ff3333;
    }}
    .spacer {{ pointer-events: none; }}
    
    /* Overlay */
    #start-overlay {{
        position: fixed;
        top: 0; left: 0; width: 100%; height: 100%;
        background: rgba(0,0,0,0.8); /* Darker backdrop */
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 9999; /* Highest Z */
        flex-direction: column;
    }}
    #start-btn {{
        background: #00AA00;
        color: white;
        font-family: 'Press Start 2P';
        padding: 20px;
        border: 4px solid #fff;
        font-size: 18px;
        cursor: pointer;
        animation: blink 1s infinite;
        text-align: center;
        line-height: 1.5;
    }}
    @keyframes blink {{ 0% {{opacity: 1;}} 50% {{opacity: 0.5;}} 100% {{opacity: 1;}} }}

</style>
</head>
<body>

<!-- OVERLAY START -->
<div id="start-overlay" onclick="startGame()">
    <div id="start-btn">TAP TO START<br><small style="font-size:10px">(Enable Audio)</small></div>
</div>
<!-- OVERLAY END -->

<div id="section-header" class="section">
    <div class="hbd-text">HAPPY BIRTHDAY<br>VISHESH!</div>
    <span class="level-up">LEVEL UP! 🍄</span>
</div>

<div id="section-game" class="section">
    <div id="score">SCORE: 0</div>
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
const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');

let customImage = null;
const uploadedImageSrc = {default_image_js};

// Pre-load logic
let imageLoaded = false;
if (uploadedImageSrc) {{
    customImage = new Image();
    customImage.src = uploadedImageSrc;
    customImage.onload = () => {{ imageLoaded = true; checkDraw(); }};
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

// Audio Handling - Critical Fix
const audioCtx = new (window.AudioContext || window.webkitAudioContext)();

function unlockAudio() {{
    if (audioCtx.state === 'suspended') {{
        audioCtx.resume();
    }}
    // Play a silent buffer to verify un-mute
    const buffer = audioCtx.createBuffer(1, 1, 22050); 
    const source = audioCtx.createBufferSource(); 
    source.buffer = buffer; 
    source.connect(audioCtx.destination); 
    source.start(0); 

    // Also prime speech synthesis
    window.speechSynthesis.cancel();
    // Speak empty string to 'warm up'
    // window.speechSynthesis.speak(new SpeechSynthesisUtterance(""));
}}

function speakOfCourse() {{
    window.speechSynthesis.cancel(); // Prioritize latest
    const u = new SpeechSynthesisUtterance("Of course");
    u.pitch = 0.5; 
    u.rate = 1.1;
    u.volume = 1.0;
    window.speechSynthesis.speak(u);
}}

function startGame() {{
    const overlay = document.getElementById('start-overlay');
    overlay.style.opacity = '0';
    setTimeout(() => overlay.style.display = 'none', 500); // Fade out
    
    unlockAudio();
    gameRunning = true;
    checkDraw();
    
    // Play start jingle or test sound
    speakOfCourse(); // Test verify voice immediately on start
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
    checkDraw();
}}

// Controls
const up = () => moveOneStep(0, -1);
const down = () => moveOneStep(0, 1);
const left = () => moveOneStep(-1, 0);
const right = () => moveOneStep(1, 0);

const opts = {{passive: false}};
const btnAdd = (id, fn) => {{
    const el = document.getElementById(id);
    if(el) {{
        el.addEventListener('touchstart', (e) => {{ e.preventDefault(); fn(); }}, opts);
        el.addEventListener('mousedown', fn);
    }}
}};

btnAdd('btn-up', up);
btnAdd('btn-down', down);
btnAdd('btn-left', left);
btnAdd('btn-right', right);


function draw() {{
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    
    for(let r=0; r<ROWS; r++) {{
        for(let c=0; c<COLS; c++) {{
            let type = map[r][c];
            let x = c * TILE_SIZE;
            let y = r * TILE_SIZE;
            
            if (type === 1) {{ #0047AB
                ctx.fillStyle = "#0047AB"; 
                ctx.fillRect(x, y, TILE_SIZE, TILE_SIZE);
            }} else if (type === 0) {{
                ctx.fillStyle = "#FFD700";
                ctx.beginPath();
                ctx.arc(x + TILE_SIZE/2, y + TILE_SIZE/2, 4, 0, Math.PI*2);
                ctx.fill();
            }}
        }}
    }}

    let px = player.x * TILE_SIZE;
    let py = player.y * TILE_SIZE;
    
    if (imageLoaded && customImage) {{
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

function checkDraw() {{
    requestAnimationFrame(draw);
}}

// Initial draw, without waiting for start
checkDraw();

</script>
</body>
</html>
"""

# Increase iframe height significantly to ensure no scroll bars in Streamlit context
components.html(game_html, height=1000, scrolling=False)
