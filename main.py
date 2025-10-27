import streamlit as st
import time

st.title("ストリームリット 入門")

st.write('プログレスバーの表示')

'Start!!'
latest_iteration = st.empty()
bar = st.progress(0)

for i in range(100):
    latest_iteration.text(f'Iteration {i+1}')
    bar.progress(i + 1)
    time.sleep(0.1)

'Done!!!'


left_column, right_column = st.columns(2)
button = left_column.button('左カラムのボタン')
if button:
    right_column.write('右カラムに表示')

expander = st.expander('問い合わせ')
expander.write('問い合わせ内容を書く')

# text = st.text_input('あなたの趣味を教えて下さい。',)
# condition = st.slider('あなたの今の調子は？', 0, 100, 50)

# 'あなたの趣味は、', text, 'です。'
# 'コンディション', condition



# if st.checkbox('Show Image'):
#     img = Image.open('okumono_m_zatsu3_68.png')
#     st.image(img, caption='雑談')


# df = pd.DataFrame(
#     np.random.rand(100, 2) / [50, 50] + [35.69, 139.70],
#     columns=['lat', 'lon']
# )

# st.map(df)
# st.line_chart(df)








# df = pd.DataFrame({
#     '1列目': [1, 2, 3, 4],
#     '2列目': [10, 20, 30, 40]
# })

# st.dataframe(df.style.highlight_max(axis=0))

# """
# # 章
# ## 節
# ### 項

# ```python
# import streamlit as st
# import numpy as np
# import pandas as pd
# ```
# """
