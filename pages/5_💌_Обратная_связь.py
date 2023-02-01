import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title='Обратная связь',
                   page_icon="📝", layout="centered", initial_sidebar_state="auto", menu_items=None)

st.title(':love_letter: Форма обратной связи с разработчиком')

st.markdown(
    '''
    Через эту форму можно:
    
    - Пожаловаться на ошибку
    - Заказать функционал 
    - Задать вопрос
    - Оставить комментарий 
    
    '''
)

components.html(
    '''
    <script src="https://yastatic.net/s3/frontend/forms/_/embed.js"></script><iframe src="https://forms.yandex.ru/cloud/63a209ce068ff02a98788943/?iframe=1" frameborder="0" name="ya-form-63a209ce068ff02a98788943" width="650"></iframe>
    ''',
    height=600
)
