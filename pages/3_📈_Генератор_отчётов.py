import pandas as pd
import streamlit as st
import datetime as dt
import app
from io import BytesIO
import xlsxwriter

today = dt.date.today()
first_day = dt.datetime(today.year, today.month, 1)
min_date = dt.datetime(today.year - 1, today.month, 1)

with st.sidebar:
    link = st.text_input("Введите ссылку на сообщество", max_chars=70,
                         placeholder='https://vk.com/example')
    period = st.date_input(label='Выберите период',
                           value=[first_day, today],
                           min_value=min_date,
                           max_value=today)
    send = st.button('Готово')

if not send:
    st.title('Отчёт появится здесь')
    st.markdown("👈 Но для начала заполните форму сбоку и нажмите на кнопку Готово")
else:
    screen_name = app.clear_link(link)
    id = app.Group.get_id(screen_name)
    group = app.Group(id)
    wall = app.Wall(id)
    wall.get_posts_by_date(period)

    tuple = app.vk_formalize(wall.posts)
    df = pd.DataFrame(tuple)



    success_text = f'''
    Отчёт по постам собщества **{group.name}** за период: **{period[0]}** с по **{period[1]}**
    '''
    st.success(success_text, icon="✅")

    period

    buffer = BytesIO()
    with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
        df.to_excel(writer, header=True, index=False)
        writer.save()

    st.download_button(label='Скачать Excel-отчёт',
                       data=buffer,
                       file_name=f"{screen_name}_report.xlsx",
                       mime="application/vnd.ms-excel"
                       )
    col1, col2, col3 = st.columns(3)
    col1.metric('Постов за период', len(wall.posts))


    st.dataframe(df)



