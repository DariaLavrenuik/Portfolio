import streamlit as st
import pandas as pd
import spacy
import en_core_web_sm

from english_exercise import EnglishExercise


exercise = EnglishExercise()
nlp = spacy.load("en_core_web_sm")


# создаем датафрейм
@st.cache_data
def data_creator():
    data = pd.DataFrame(columns=['raw', 'type', 'object', 'options', 'answer'])
    return data


data = data_creator()


# парсим текст
def process_text(text, data):
    try:
        doc = nlp(text)
        for sent in doc.sents:
            data.loc[len(data), 'raw'] = sent.text
    except Exception as e:
        st.error(f"Error processing text: {e}")


st.header(':blue[Генератор упражнений по английскому языку]',
          divider='rainbow')
uploaded_file = st.file_uploader("Загрузите текст", type=["txt"])
files = 'Little_red_cap.txt'

st.download_button(
    label="Скачать пример",
    data=files.encode("utf-8"),
    file_name="Little_red_cap.txt",
    key="example_text_download_button",
    help='Скачайте пример и загрузите в приложение')


@st.cache_data()
def apply_choose_variant(data):
    return data.apply(exercise.choose_variant, axis=1)


def create_columns(data):
    for index, task in data.iterrows():
        col1, col2 = st.columns(2)

        with col1:
            st.write('_____')
            if not pd.isna(task['answer']):
                hidden_sentence = task['raw'].replace(task['answer'], '....')
                st.write(hidden_sentence)
            else:
                st.write(task['raw'])

        with col2:
            st.write('_____')
            if (task['type'] == 'choose the sent') and (not pd.isna(task['answer'])):
                for i in range(len(task['options'])):
                    option = task['options']
                    key = f"{task['type']}_{i}_{index}"
                x = st.radio(label='Выберите правильное предложение',
                             options=option,
                             key=key,
                             index=None)
                if x == task['answer']:
                    st.success('', icon="✅")
                elif x is not None:
                    st.error('', icon="😟")

            if task['type'] == 'fill_the_gap' and not pd.isna(task['answer']):
                x = st.text_input(label='Впишите пропущенное слово',
                                  key={index})
                if x:
                    if x == task['answer']:
                        st.success('', icon="✅")
                    else:
                        st.error('', icon="😟")
            if pd.isna(task['answer']):
                pass

            elif task['type'] == 'choose_verb_form' and not pd.isna(task['answer']):
                for i in range(len(task['options'])):
                    option = task['options']
                    key = f"{task['type']}_{i}_{index}"

                x = st.selectbox('Выберите подходящую форму глагола',
                                 options=['____'] + option,
                                 key=key)
                if x == '____':
                    pass
                elif x == task['answer']:
                    st.success('', icon="✅")
                else:
                    st.error('', icon="😟")

            elif task['type'] == 'select_word' and not pd.isna(task['answer']):
                for i in range(len(task['options'])):
                    option = task['options']
                    key = f"{task['type']}_{i}_{index}"

                x = st.selectbox('Выберите правильный вариант',
                                 options=['____'] + option,
                                 key=key)
                if x == '____':
                    pass
                elif x == task['answer']:
                    st.success('', icon="✅")
                else:
                    st.error('', icon="😟")


def main(data, uploaded_file):
    if 'data' not in st.session_state:
        st.session_state.data = pd.DataFrame(
            columns=['raw', 'type', 'object', 'options', 'answer'])
    if uploaded_file is not None:
        text = uploaded_file.read().decode('utf-8')
        process_text(text, data)
        data = apply_choose_variant(data)
    create_columns(data)


if __name__ == "__main__":
    main(data, uploaded_file)
