import streamlit as st
import random

st.set_page_config(layout="wide")
st.title("熟語を作って勝利！周回すごろく")


if "position" not in st.session_state:
    st.session_state.position = 0
if "letters" not in st.session_state:
    st.session_state.letters = [] 
if "dice_left" not in st.session_state:
    st.session_state.dice_left = 10 




BOARD_SIZE = 20

LETTERS = {
    2: "日",
    4: "本",
    6: "語",
    8: "学",
    10: "習",
    12: "生",
    14: "活",
    16: "人",
    18: "間"
}


st.header("すごろく")

st.write(f"現在位置： **{st.session_state.position} マス**")
st.write(f"残りサイコロ回数： **{st.session_state.dice_left} 回**")


if st.session_state.dice_left <= 0:
    st.warning("サイコロを振れる回数がありません！熟語を作れなければリセットしてください")


if st.button("サイコロを振る", disabled=st.session_state.dice_left <= 0):
    dice = random.randint(1, 6)
    st.write(f"サイコロの目：**{dice}**")
    st.session_state.dice_left -= 1


    st.session_state.position = (st.session_state.position + dice) % BOARD_SIZE


    if st.session_state.position in LETTERS:
        letter = LETTERS[st.session_state.position]
        st.success(f"文字を獲得！ → **{letter}**")
        st.session_state.letters.append(letter)


board = ["□"] * BOARD_SIZE
board[st.session_state.position] = "🧍"
st.write(" ".join(board))


if st.button("リセット"):
    st.session_state.position = 0
    st.session_state.letters = []
    st.session_state.dice_left = 10



st.sidebar.title("獲得した文字")

if st.session_state.letters:
    st.sidebar.write("使う文字を選んでください")
else:
    st.sidebar.write("まだ文字はありません")


selected_letters = st.sidebar.multiselect(
    "熟語に使う文字を選ぶ",
    options=st.session_state.letters,
    default=[]
)


st.sidebar.subheader("熟語を作る")

if st.sidebar.button("熟語を作成"):
    if selected_letters:
        result = "".join(selected_letters)
        st.sidebar.success(f"熟語：**{result}**")
        st.balloons()
        st.success(f"**{result}** を作成して勝利です！おめでとう！")
        st.session_state.dice_left = 0 
    else:
        st.sidebar.warning("文字を選択してください")
if st.sidebar.button("🔄 リセット"):
    st.session_state.clear()
    st.rerun()