import streamlit as st

import app

links = st.text_area("Введите ссылки на группы и нажмите **Ctrl+Enter**",
    placeholder='''https://vk.com/example1, https://vk.com/example2, https://vk.com/example3...''')

x = links.split(', ')

app.vk_get_from_groups(x, )

