import streamlit as st
import pandas as pd
import app
import datetime as dt

st.title('Парсер подписчиков')
link = st.text_input("Введите ссылку на сообщество", max_chars=70,
                     placeholder='https://vk.com/example')


if link:
    screen_name = app.clear_link(link)
    group_id = app.Group.get_id(screen_name)
    group = app.Group(group_id)
    group.get_members()

    data = pd.DataFrame(group.members).to_csv(header=False, index=False)

    st.download_button(label=f'Скачать список подписчиков группы {group.name}',
                       data=data,
                       file_name=f'./{group.screen_name}_subscribers.csv',
                       mime='text/csv',
                       )
