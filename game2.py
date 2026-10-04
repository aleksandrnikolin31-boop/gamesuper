import random
import streamlit as st

st.set_page_config(page_title="Traffic Dodge Game", page_icon="🚙")

st.title("🚙 Симулятор выживания на дороге")
st.write(
    "Уворачивайся от встречных машин! Твоя машинка внизу (🚙). Нажимай кнопки,"
    " чтобы маневрировать."
)

# 1. Инициализация состояния игры
if "player_pos" not in st.session_state:
  st.session_state.player_pos = 1  # 0 - лево, 1 - центр, 2 - право
  st.session_state.score = 0
  st.session_state.game_over = False
  # Дорога длиной 5 клеток, на старте она пустая (везде None)
  st.session_state.road = [
      [None, None, None],
      [None, None, None],
      [None, None, None],
      [None, None, None],
      [None, None, None],
  ]


# Функция для перезапуска
def restart_game():
  st.session_state.player_pos = 1
  st.session_state.score = 0
  st.session_state.game_over = False
  st.session_state.road = [[None, None, None] for _ in range(5)]


# 2. Логика движения игры (вызывается при каждом ходе игрока)
def game_step(direction):
  if st.session_state.game_over:
    return

  # Двигаем игрока
  if direction == "left" and st.session_state.player_pos > 0:
    st.session_state.player_pos -= 1
  elif direction == "right" and st.session_state.player_pos < 2:
    st.session_state.player_pos += 1

  # Сдвигаем дорогу вниз (удаляем нижний ряд, добавляем новый сверху)
  st.session_state.road.pop()

  # Генерируем новую встречную машину сверху с шансом 40%
  new_row = [None, None, None]
  if random.random() < 0.4:
    spawn_lane = random.randint(0, 2)
    new_row[spawn_lane] = "🚗"

  st.session_state.road.insert(0, new_row)

  # Проверяем столкновение: если на 4-й строчке (самой нижней) в нашей полосе есть машина
  last_row = st.session_state.road[4]
  if last_row[st.session_state.player_pos] == "🚗":
    st.session_state.game_over = True
  else:
    st.session_state.score += 1


# 3. Интерфейс игры
if st.session_state.game_over:
  st.error(f"💥 БУМ! Столкновение! Твой итоговый счет: {st.session_state.score}")
  st.button("Сыграть еще раз 🔄", on_click=restart_game)
else:
  st.metric(label="Набранные очки 🏆", value=st.session_state.score)

  # Отрисовка дороги на экране
  road_html = "<div style='font-family: monospace; font-size: 24px; line-height: 1.5; background-color: #2b2b2b; padding: 20px; border-radius: 10px; width: 180px; margin: 0 auto; color: white;'>"

  # Рисуем препятствия
  for row in st.session_state.road:
    row_str = "️|"
    for cell in row:
      row_str += cell if cell else "⬜"
    row_str += "|"
    road_html += f"<center>{row_str}</center>"

  # Рисуем игрока на нижней строчке
  player_row = ["⬜", "⬜", "⬜"]
  player_row[st.session_state.player_pos] = "🚙"
  player_row_str = "|" + "".join(player_row) + "|"
  road_html += f"<center><b>{player_row_str}</b></center></div>"

  # Выводим дорогу в Streamlit
  st.markdown(road_html, unsafe_allow_html=True)

  st.write("")  # Отступ

  # Кнопки управления
  col1, col2, col3 = st.columns([1, 2, 1])
  with col1:
    st.button(
        "⬅️ Влево",
        on_click=game_step,
        args=("left",),
        disabled=st.session_state.game_over,
    )
  with col2:
    st.button(
        "🔲 Прямо",
        on_click=game_step,
        args=("straight",),
        disabled=st.session_state.game_over,
    )
  with col3:
    st.button(
        "Вправо ➡️",
        on_click=game_step,
        args=("right",),
        disabled=st.session_state.game_over,
    )
