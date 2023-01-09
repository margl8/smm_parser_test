import streamlit as st
from app import Group
from app import utility as ut

st.title("Вычислить ID")
link = st.text_input("Введите ссылку на сообщество", max_chars=70,
                     placeholder='https://vk.com/example')
if link:
    screen_name = ut.clear_link(link)
    id = Group.get_id(screen_name)
    group = Group(id)
    st.write(f'ID сообщества: {group.group_id}')
    st.subheader('Подробная информация')
    st.write(f'Название: {group.name}')
    st.write(f'Короткий адрес: {group.screen_name}')
    st.write(f'Количество подписчиков: {group.members_count}')

