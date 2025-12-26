import streamlit as st
import random

# =====================
# 基本設定
# =====================
ROWS = 5
COLS = 4
TOTAL = ROWS * COLS
MAX_DICE = 10

WIN_WORD_CANDIDATES = [
    "日本語",
    "学習",
    "生活",
    "人間",
    "勉強",
]

LETTER_SOURCE = list("日本語学習勉強生活人間")
QUESTION_MARK = "？"

# =====================
# session_state 初期化
# =====================
if "player_pos" not in st.session_state:
    st.session_state.player_pos = 0

if "letters" not in st.session_state:
    st.session_state.letters = []

if "dice_left" not in st.session_state:
    st.session_state.dice_left = MAX_DICE

if "dice" not in st.session_state:
    st.session_state.dice = None

if "win" not in st.session_state:
    st.session_state.win = False

if "win_word" not in st.session_state:
    st.session_state.win_word = random.choice(WIN_WORD_CANDIDATES)

if "board_letters" not in st.session_state:
    board = []
    for i in range(TOTAL):
        # 右列（赤マス）は文字なし
        if i % COLS == COLS - 1:
            board.append("")
        else:
            if random.random() < 0.2:
                board.append(QUESTION_MARK)
            else:
                board.append(random.choice(LETTER_SOURCE))
    st.session_state.board_letters = board

# =====================
# UI
# =====================
st.set_page_config(layout="wide")
st.title("🧩 熟語を作って勝利！周回すごろく")

st.info(f"🎯 勝利条件：「{st.session_state.win_word}」を完全一致で作る")
st.write(f"📍 現在位置：{st.session_state.player_pos}")
st.write(f"🎲 残りサイコロ回数：{st.session_state.dice_left}")

# =====================
# サイコロ
# =====================
if st.button(
    "🎲 サイコロを振る",
    disabled=st.session_state.dice_left <= 0 or st.session_state.win
):
    roll = random.randint(1, 6)
    st.session_state.dice = roll
    st.session_state.dice_left -= 1

    st.session_state.player_pos = (
        st.session_state.player_pos + roll
    ) % TOTAL

    idx = st.session_state.player_pos
    col = idx % COLS
    cell_letter = st.session_state.board_letters[idx]

    # 赤マス
    if col == COLS - 1:
        if st.session_state.letters:
            lost = random.choice(st.session_state.letters)
            st.session_state.letters.remove(lost)
            st.warning(f"🟥 赤マス！文字「{lost}」を失いました")
        else:
            st.info("🟥 赤マス！失う文字がありません")

    # 白マス
    else:
        if cell_letter == QUESTION_MARK:
            gained = random.choice(LETTER_SOURCE)
            st.success(f"❓ マス！ランダムで「{gained}」を獲得")
            st.session_state.letters.append(gained)
        elif cell_letter:
            st.success(f"⬜ 文字「{cell_letter}」を獲得")
            st.session_state.letters.append(cell_letter)

# =====================
# 出目表示
# =====================
if st.session_state.dice is not None:
    st.markdown(f"### 出目：{st.session_state.dice}")

# =====================
# CSS
# =====================
st.markdown(
    """
    <style>
    .board {
        display: grid;
        grid-template-columns: repeat(4, 50px);
        grid-template-rows: repeat(5, 50px);
        gap: 4px;
        background-color: #8B5E3C;
        padding: 6px;
        width: fit-content;
        margin: 30px auto;
        border-radius: 10px;
    }

    .cell {
        position: relative;
        background-color: #F7F3E9;
        border: 1px solid #AAA;
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 6px;
        font-weight: bold;
        font-size: 18px;
        color: black;
    }

    /* 赤マス */
    .cell.event {
        background-color: #F3C6C6;
    }

    /* 赤マスの×印 */
    .cell.event::before {
        content: "×";
        position: absolute;
        top: 6px;
        right: 8px;
        font-size: 18px;
        font-weight: bold;
        color: #B00020;
        opacity: 0.8;
    }

    /* プレイヤー */
    .cell.player {
        border: 3px solid #2ECC71;
    }

    .cell.player::after {
        content: "";
        width: 16px;
        height: 16px;
        background-color: #2ECC71;
        border-radius: 50%;
        position: absolute;
        bottom: 4px;
        right: 4px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# =====================
# 盤面描画
# =====================
cells_html = ""

for i in range(TOTAL):
    classes = ["cell"]

    if i % COLS == COLS - 1:
        classes.append("event")

    if i == st.session_state.player_pos:
        classes.append("player")

    letter = st.session_state.board_letters[i]
    cells_html += f'<div class="{" ".join(classes)}">{letter}</div>'

st.markdown(
    f"""
    <div class="board">
        {cells_html}
    </div>
    """,
    unsafe_allow_html=True
)

# =====================
# サイドバー：熟語作成
# =====================
st.sidebar.title("📦 所持文字")

if st.session_state.letters:
    selected = st.sidebar.multiselect(
        "使用する文字を選択",
        options=st.session_state.letters
    )

    if st.sidebar.button("🈴 熟語を作成"):
        word = "".join(selected)

        if word == st.session_state.win_word:
            st.sidebar.success(f"🎉 勝利！「{word}」完成！")
            st.balloons()
            st.session_state.win = True
        else:
            st.sidebar.error(f"❌ 不正解：{word}")
else:
    st.sidebar.write("なし")

st.sidebar.divider()

# =====================
# リセット（サイドバー）
# =====================
if st.sidebar.button("🔄 リセット"):
    st.session_state.clear()
    st.rerun()
