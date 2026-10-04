import streamlit as st

st.set_page_config(
    page_title="Авто-гонки на выживание", page_icon="🚙", layout="centered"
)

st.title("🚙 Авто-гонки со стрелочками")
st.write(
    "Машинка едет вперед **автоматически**! Управляйте синей машинкой с помощью"
    " **стрелочек клавиатуры (⬅️ / ➡️)**, чтобы уворачиваться от красных"
    " автомобилей."
)

# JavaScript + HTML код для динамической игры с управлением от клавиатуры
game_html = """
<!DOCTYPE html>
<html>
<head>
    <style>
        #game-container {
            font-family: monospace;
            font-size: 28px;
            line-height: 1.4;
            background-color: #222;
            color: white;
            padding: 20px;
            border-radius: 10px;
            width: 240px;
            margin: 0 auto;
            text-align: center;
            box-shadow: 0px 4px 15px rgba(0,0,0,0.5);
        }
        #score {
            font-size: 20px;
            margin-bottom: 10px;
            color: #4CAF50;
            font-weight: bold;
        }
        #road {
            background-color: #333;
            padding: 10px 0;
            border-left: 4px dashed #fff;
            border-right: 4px dashed #fff;
        }
        .btn-restart {
            margin-top: 15px;
            padding: 8px 15px;
            font-size: 16px;
            background-color: #ff4b4b;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
        }
    </style>
</head>
<body>

<div id="game-container">
    <div id="score">Очки: 0</div>
    <div id="road"></div>
    <div id="game-over-space"></div>
</div>

<script>
    const ROWS = 7;
    const COLS = 3;
    let playerPos = 1; // 0 - лево, 1 - центр, 2 - право
    let score = 0;
    let gameOver = false;
    let gameInterval;
    
    // Создаем пустую сетку дороги
    let road = Array(ROWS).fill(null).map(() => Array(COLS).fill(null));

    const roadDiv = document.getElementById('road');
    const scoreDiv = document.getElementById('score');
    const gameOverSpace = document.getElementById('game-over-space');

    function render() {
        let html = "";
        for (let r = 0; r < ROWS; r++) {
            let rowStr = "";
            for (let c = 0; c < COLS; c++) {
                if (r === ROWS - 1 && c === playerPos) {
                    rowStr += gameOver ? "💥" : "🚙";
                } else {
                    rowStr += road[r][c] ? "🚗" : "⬛";
                }
            }
            html += rowStr + "<br>";
        }
        roadDiv.innerHTML = html;
        scoreDiv.innerText = "Очки: " + score;
    }

    function updateGame() {
        if (gameOver) return;

        // Сдвигаем все машины вниз
        road.pop();
        
        // Генерируем новую машину сверху с вероятностью 35%
        let newRow = [null, null, null];
        if (Math.random() < 0.35) {
            let lane = Math.floor(Math.random() * COLS);
            newRow[lane] = "🚗";
        }
        road.unshift(newRow);

        // Проверяем столкновение на предпоследнем шаге перед отрисовкой игрока
        // (так как игрок на самой нижней строчке ROWS-1)
        if (road[ROWS - 1][playerPos] === "🚗") {
            endGame();
            return;
        }

        score += 1;
        render();
    }

    function endGame() {
        gameOver = true;
        clearInterval(gameInterval);
        render();
        gameOverSpace.innerHTML = `
            <div style="color: #ff4b4b; font-size: 18px; margin-top: 10px; font-weight: bold;">БАБАХ! ИГРА ОКОНЧЕНА</div>
            <button class="btn-restart" onclick="resetGame()">Играть заново 🔄</button>
        `;
    }

    function resetGame() {
        playerPos = 1;
        score = 0;
        gameOver = false;
        road = Array(ROWS).fill(null).map(() => Array(COLS).fill(null));
        gameOverSpace.innerHTML = "";
        render();
        clearInterval(gameInterval);
        gameInterval = setInterval(updateGame, 400); // Скорость движения (400 мс на шаг)
    }

    // Слушатель нажатий клавиатуры
    window.addEventListener('keydown', function(event) {
        if (gameOver) return;
        
        if (event.key === 'ArrowLeft' && playerPos > 0) {
            playerPos--;
            // Сразу проверяем столкновение при маневре
            if (road[ROWS - 1][playerPos] === "🚗") {
                endGame();
            } else {
                render();
            }
        } else if (event.key === 'ArrowRight' && playerPos < COLS - 1) {
            playerPos++;
            // Сразу проверяем столкновение при маневре
            if (road[ROWS - 1][playerPos] === "🚗") {
                endGame();
            } else {
                render();
            }
        }
    });

    // Старт игры
    resetGame();
</script>

</body>
</html>
"""

# Встраиваем HTML/JS компонент в Streamlit
st.components.v1.html(game_html, height=450)
