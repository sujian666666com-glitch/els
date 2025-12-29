const GRID_WIDTH = 10;
const GRID_HEIGHT = 20;
const CELL_SIZE = 30;

const COLORS = [
    '#000000',
    '#ff0000',
    '#00ff00',
    '#0000ff',
    '#ffff00',
    '#00ffff',
    '#ff00ff',
    '#ffa500'
];

const SHAPES = [
    [[1, 1, 1, 1]],
    [[1, 1], [1, 1]],
    [[1, 1, 1], [0, 1, 0]],
    [[1, 1, 1], [1, 0, 0]],
    [[1, 1, 1], [0, 0, 1]],
    [[1, 1, 0], [0, 1, 1]],
    [[0, 1, 1], [1, 1, 0]]
];

const DIFFICULTIES = {
    'easy': { speed: 800, name: '简单' },
    'medium': { speed: 500, name: '中等' },
    'hard': { speed: 300, name: '困难' }
};

let canvas, ctx, nextCanvas, nextCtx;
let grid, currentPiece, nextPiece;
let score, highScore, difficulty, gameOver;
let fallTime, fallSpeed, gameLoop;
let newHighScore = false;

function init() {
    canvas = document.getElementById('gameCanvas');
    ctx = canvas.getContext('2d');
    nextCanvas = document.getElementById('nextCanvas');
    nextCtx = nextCanvas.getContext('2d');
    
    loadHighScores();
    updateHighScoresDisplay();
}

function loadHighScores() {
    const saved = localStorage.getItem('tetrisHighScores');
    if (saved) {
        return JSON.parse(saved);
    }
    return { easy: 0, medium: 0, hard: 0 };
}

function saveHighScores(scores) {
    localStorage.setItem('tetrisHighScores', JSON.stringify(scores));
}

function updateHighScoresDisplay() {
    const scores = loadHighScores();
    document.getElementById('easyScore').textContent = scores.easy;
    document.getElementById('mediumScore').textContent = scores.medium;
    document.getElementById('hardScore').textContent = scores.hard;
}

function showMenu() {
    document.getElementById('menu').style.display = 'block';
    document.getElementById('game').style.display = 'none';
    document.getElementById('gameOver').style.display = 'none';
    updateHighScoresDisplay();
}

function startGame(diff) {
    difficulty = diff;
    const scores = loadHighScores();
    highScore = scores[difficulty];
    
    grid = Array(GRID_HEIGHT).fill(null).map(() => Array(GRID_WIDTH).fill(0));
    currentPiece = newPiece();
    nextPiece = newPiece();
    score = 0;
    gameOver = false;
    newHighScore = false;
    fallTime = 0;
    fallSpeed = DIFFICULTIES[difficulty].speed;
    
    document.getElementById('menu').style.display = 'none';
    document.getElementById('gameOver').style.display = 'none';
    document.getElementById('game').style.display = 'block';
    document.getElementById('difficulty').textContent = DIFFICULTIES[difficulty].name;
    document.getElementById('highScore').textContent = highScore;
    
    updateScore();
    if (gameLoop) cancelAnimationFrame(gameLoop);
    gameLoop = requestAnimationFrame(update);
}

function newPiece() {
    const shape = SHAPES[Math.floor(Math.random() * SHAPES.length)];
    const color = Math.floor(Math.random() * 7) + 1;
    return {
        shape: shape,
        color: color,
        x: Math.floor(GRID_WIDTH / 2) - Math.floor(shape[0].length / 2),
        y: 0
    };
}

function validMove(piece, dx, dy, newShape = null) {
    const shape = newShape || piece.shape;
    
    for (let y = 0; y < shape.length; y++) {
        for (let x = 0; x < shape[y].length; x++) {
            if (shape[y][x]) {
                const newX = piece.x + x + dx;
                const newY = piece.y + y + dy;
                
                if (newX < 0 || newX >= GRID_WIDTH || newY >= GRID_HEIGHT) {
                    return false;
                }
                
                if (newY >= 0 && grid[newY][newX]) {
                    return false;
                }
            }
        }
    }
    return true;
}

function rotatePiece(piece) {
    const shape = piece.shape;
    const rows = shape.length;
    const cols = shape[0].length;
    const newShape = [];
    
    for (let x = 0; x < cols; x++) {
        newShape[x] = [];
        for (let y = 0; y < rows; y++) {
            newShape[x][y] = shape[rows - 1 - y][x];
        }
    }
    
    return newShape;
}

function lockPiece() {
    for (let y = 0; y < currentPiece.shape.length; y++) {
        for (let x = 0; x < currentPiece.shape[y].length; x++) {
            if (currentPiece.shape[y][x]) {
                if (currentPiece.y + y < 0) {
                    gameOver = true;
                    checkHighScore();
                    return;
                }
                grid[currentPiece.y + y][currentPiece.x + x] = currentPiece.color;
            }
        }
    }
    
    clearLines();
    currentPiece = nextPiece;
    nextPiece = newPiece();
    
    if (!validMove(currentPiece, 0, 0)) {
        gameOver = true;
        checkHighScore();
    }
}

function clearLines() {
    let linesCleared = 0;
    
    for (let y = GRID_HEIGHT - 1; y >= 0; y--) {
        if (grid[y].every(cell => cell !== 0)) {
            grid.splice(y, 1);
            grid.unshift(Array(GRID_WIDTH).fill(0));
            linesCleared++;
            y++;
        }
    }
    
    if (linesCleared > 0) {
        score += linesCleared * 100 * (linesCleared + 1) / 2;
        updateScore();
    }
}

function checkHighScore() {
    const scores = loadHighScores();
    if (score > scores[difficulty]) {
        scores[difficulty] = score;
        saveHighScores(scores);
        newHighScore = true;
    }
    
    setTimeout(() => {
        showGameOver();
    }, 500);
}

function updateScore() {
    document.getElementById('score').textContent = score;
}

function showGameOver() {
    document.getElementById('game').style.display = 'none';
    document.getElementById('gameOver').style.display = 'block';
    document.getElementById('finalScore').textContent = score;
    document.getElementById('newRecord').style.display = newHighScore ? 'block' : 'none';
}

function restartGame() {
    startGame(difficulty);
}

function draw() {
    ctx.fillStyle = '#000000';
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    
    for (let y = 0; y < GRID_HEIGHT; y++) {
        for (let x = 0; x < GRID_WIDTH; x++) {
            if (grid[y][x]) {
                ctx.fillStyle = COLORS[grid[y][x]];
                ctx.fillRect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE);
                ctx.strokeStyle = '#000000';
                ctx.strokeRect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE);
            }
        }
    }
    
    for (let y = 0; y < currentPiece.shape.length; y++) {
        for (let x = 0; x < currentPiece.shape[y].length; x++) {
            if (currentPiece.shape[y][x]) {
                ctx.fillStyle = COLORS[currentPiece.color];
                ctx.fillRect(
                    (currentPiece.x + x) * CELL_SIZE,
                    (currentPiece.y + y) * CELL_SIZE,
                    CELL_SIZE,
                    CELL_SIZE
                );
                ctx.strokeStyle = '#000000';
                ctx.strokeRect(
                    (currentPiece.x + x) * CELL_SIZE,
                    (currentPiece.y + y) * CELL_SIZE,
                    CELL_SIZE,
                    CELL_SIZE
                );
            }
        }
    }
    
    ctx.strokeStyle = '#00ffff';
    ctx.lineWidth = 3;
    ctx.strokeRect(0, 0, canvas.width, canvas.height);
    ctx.lineWidth = 1;
    
    drawNextPiece();
}

function drawNextPiece() {
    nextCtx.fillStyle = '#000000';
    nextCtx.fillRect(0, 0, nextCanvas.width, nextCanvas.height);
    
    const offsetX = (nextCanvas.width - nextPiece.shape[0].length * 30) / 2;
    const offsetY = (nextCanvas.height - nextPiece.shape.length * 30) / 2;
    
    for (let y = 0; y < nextPiece.shape.length; y++) {
        for (let x = 0; x < nextPiece.shape[y].length; x++) {
            if (nextPiece.shape[y][x]) {
                nextCtx.fillStyle = COLORS[nextPiece.color];
                nextCtx.fillRect(offsetX + x * 30, offsetY + y * 30, 30, 30);
                nextCtx.strokeStyle = '#000000';
                nextCtx.strokeRect(offsetX + x * 30, offsetY + y * 30, 30, 30);
            }
        }
    }
}

let lastTime = 0;

function update(time = 0) {
    if (gameOver) return;
    
    const deltaTime = time - lastTime;
    lastTime = time;
    
    fallTime += deltaTime;
    
    if (fallTime >= fallSpeed) {
        if (validMove(currentPiece, 0, 1)) {
            currentPiece.y++;
        } else {
            lockPiece();
        }
        fallTime = 0;
    }
    
    draw();
    gameLoop = requestAnimationFrame(update);
}

document.addEventListener('keydown', (e) => {
    if (gameOver) return;
    
    switch (e.key) {
        case 'ArrowLeft':
            if (validMove(currentPiece, -1, 0)) {
                currentPiece.x--;
            }
            break;
        case 'ArrowRight':
            if (validMove(currentPiece, 1, 0)) {
                currentPiece.x++;
            }
            break;
        case 'ArrowDown':
            if (validMove(currentPiece, 0, 1)) {
                currentPiece.y++;
            }
            break;
        case 'ArrowUp':
            const newShape = rotatePiece(currentPiece);
            if (validMove(currentPiece, 0, 0, newShape)) {
                currentPiece.shape = newShape;
            }
            break;
        case ' ':
            while (validMove(currentPiece, 0, 1)) {
                currentPiece.y++;
            }
            lockPiece();
            break;
        case 'Escape':
            showMenu();
            break;
    }
    
    if (!gameOver) {
        draw();
    }
});

window.onload = init;
