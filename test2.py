import streamlit as st
import random


ROWS = 5
COLS = 4
TOTAL = ROWS * COLS
MAX_DICE = 10

LETTER_SOURCE = list("英語学習勉強生活人間")
QUESTION_MARK = "？"

WIN_WORD_CANDIDATES = [
    "英語", "学習", "生活", "人間", "勉強"
]


if "player_pos" not in st.session_state:
    st.session_state.player_pos = 0

if "letters" not in st.session_state:
    st.session_state.letters = []

if "selected_letters" not in st.session_state:
    st.session_state.selected_letters = []

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
        if i % COLS == COLS - 1:
            board.append("✖") 
        else:
            if random.random() < 0.2:
                board.append(QUESTION_MARK)
            else:
                board.append(random.choice(LETTER_SOURCE))
    st.session_state.board_letters = board


st.set_page_config(layout="wide")
st.title("熟語すごろく")
st.info(f"勝利条件：『{st.session_state.win_word}』をで作ってみよう")




left_col, right_col = st.columns([1, 2])
st.header("サイコロを振って盤面を進もう、赤マスに止まると文字を失うよ！")

with left_col:
    st.subheader("🎲 サイコロ")
    st.write(f"残り回数：**{st.session_state.dice_left}**")

    if st.button(
        "サイコロを振る",
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


        if col == COLS - 1:
            if st.session_state.letters:
                lost = random.choice(st.session_state.letters)
                st.session_state.letters.remove(lost)
                st.warning(f"赤マス！「{lost}」を失いました")
            else:
                st.info("赤マス！失う文字がありません")

        else:
            if cell_letter == QUESTION_MARK:
                gained = random.choice(LETTER_SOURCE)
                st.success(f"❓ マス！「{gained}」を獲得")
                st.session_state.letters.append(gained)
            else:
                st.success(f"文字「{cell_letter}」を獲得")
                st.session_state.letters.append(cell_letter)

    if st.session_state.dice is not None:
        st.markdown(f"### 出目：{st.session_state.dice}")


with right_col:
    
    st.markdown("""
    <style>
    .board {
        display: grid;
        grid-template-columns: repeat(4, 50px);
        grid-template-rows: repeat(5, 50px);
        gap: 4px;
        background-color: #8B5E3C;
        padding: 6px;
        width: fit-content;
        margin: 20px auto;
        border-radius: 10px;
    }
    .cell {
        background-color: #F7F3E9;
        border: 1px solid #AAA;
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 6px;
        font-weight: bold;
        font-size: 18px;
        color: black;
        position: relative;
    }
    .cell.event {
        background-color: #F3C6C6;
    }
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
    """, unsafe_allow_html=True)

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
        f'<div class="board">{cells_html}</div>',
        unsafe_allow_html=True
    )


st.sidebar.title("獲得した文字")

letters = st.session_state.letters

for row in range(0, len(letters), 2):
    cols = st.sidebar.columns(2)

    for col_idx in range(2):
        idx = row + col_idx

        if idx < len(letters):
            letter = letters[idx]
            label = f"▶ {letter}" if letter in st.session_state.selected_letters else letter

            if cols[col_idx].button(label, key=f"letter_btn_{idx}"):
                if letter in st.session_state.selected_letters:
                    st.session_state.selected_letters.remove(letter)
                else:
                    st.session_state.selected_letters.append(letter)

st.sidebar.divider()

st.sidebar.subheader("選択中")
if st.session_state.selected_letters:
    st.sidebar.write("".join(st.session_state.selected_letters))
else:
    st.sidebar.write("なし")


if st.sidebar.button("熟語を作成"):
    word = "".join(st.session_state.selected_letters)

    if word == st.session_state.win_word:
        st.sidebar.success(f"勝利！「{word}」完成！")
        st.balloons()
        st.session_state.win = True
    else:
        st.sidebar.error(f"不正解：{word}")

    st.session_state.selected_letters = []


st.sidebar.divider()

if st.sidebar.button("リセット"):
    st.session_state.clear()
    st.rerun()

