import streamlit as st
import pandas as pd
from itertools import chain
import plotly.express as px
import pickle
import numpy as np


@st.cache_data
def load_model():
    with open('model.pkl', 'rb') as file:
        loaded_model = pickle.load(file)
    return loaded_model

@st.cache_data
def preprocess_data(data):
    data['saledate'] = pd.to_datetime(data['saledate'], utc=True)
    data['sale_year'] = data['saledate'].dt.year
    sale_year = data['sale_year']
    grouped_data = data.groupby('make')[['model', 'trim', 'year']].agg(list).reset_index()
    year = data['year'].sort_values().unique()
    trim = data['trim'].sort_values().unique()
    condition = data['condition'].sort_values().unique()
    return grouped_data, year, trim, condition, sale_year

loaded_model = load_model()


data = pd.read_csv('df_last.csv',  nrows=10000)


grouped_data, year, trim, condition, sale_year = preprocess_data(data)
all_categories_filled = False

st.title('Used cars prediction')
sidebar_container = st.sidebar.empty()
sidebar_container.markdown('Заполните информацию о вашей машине')

selected_make = st.sidebar.selectbox('Марка', (grouped_data['make']))

# фильтруем модели по марке
filtered_model = grouped_data[grouped_data['make'] == selected_make]
flattened_models = list(chain.from_iterable(filtered_model['model']))
unique_models = pd.Series(flattened_models).sort_values().unique()  


selected_model = st.sidebar.selectbox('Модель', unique_models)


selected_year = st.sidebar.selectbox('Год выпуска', year)
    
selected_odometer = st.sidebar.number_input('Пробег')

flattened_trims = list(chain.from_iterable(filtered_model['trim']))
unique_trims = pd.Series(flattened_trims).sort_values().unique() 
selected_trim = st.sidebar.selectbox('Комплектация', unique_trims)

selected_condition = st.sidebar.selectbox('Оцените состояние вашей машины', condition)

selected_num_years = st.sidebar.number_input('Сколько лет вашей машине')
#st.sidebar.button("Сделать прогноз", key=25)

if (
    selected_make is not None and
    selected_model is not None and
    selected_year is not None and
    selected_odometer is not None and
    selected_trim is not None and
    selected_condition is not None and
    selected_num_years is not None
):
    all_categories_filled = True

# Create a button to trigger the prediction
if st.sidebar.button("Сделать прогноз") and all_categories_filled:

    user_input = {
        'year': selected_year,
        
        'model': selected_model,
        'trim': selected_trim,
        'transmission' : "automatic",
        'state': np.nan,
        'condition': selected_condition,
        'odometer': selected_odometer,
        'color': np.nan,
        'interior': np.nan,
        'seller': np.nan,
        'make': selected_make,
        'group': np.nan,
        'age_of_car': selected_num_years,
        'avg_price_make': np.nan
        
    }
    
    cat = ['make', 'model', 'trim', 'group', 'state', 'color',
               'transmission', 'interior', 'seller', 'condition']
    user_input_df = pd.DataFrame([user_input])
    user_input_df[cat] = user_input_df[cat].astype('str')
    prediction = loaded_model.predict(user_input_df)
    st.sidebar.text(f'Predicted Price: ${prediction[0]:,.2f}')
else:
    st.sidebar.text("Пожалуйста, заполните все поля.")    


st.header('Статистика по имеющимся данным')
st.write (data[data['model'] == selected_model].describe())

st.header('Зависимость цены от года продажи')
st.line_chart(data[data['model'] == selected_model], x = 'saledate', y = 'sellingprice') 



st.header('Зависимость цены от пробега')

fig = px.scatter(
    data[data['model'] == selected_model],
    x="odometer",
    y="sellingprice",
    color = 'model',
    
    log_x=True,
    size_max=60,
)


st.plotly_chart(fig, theme="streamlit", use_container_width=True)
