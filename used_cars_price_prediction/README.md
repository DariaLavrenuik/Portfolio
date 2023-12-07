# Предсказание стоимости авто на вторичном рынке

[ipynb](https://github.com/DariaLavrenuik/Portfolio/blob/main/used_cars_price_prediction/notebook_cars.ipynb)


### Описание проекта:
Разработать модель, предсказывающую стоимость авто на вторичном рынке. Метрикой оценки является MAPE - Mean Absolute Percentage Error.


### Навыки и инструменты:

- pandas
- matplotlib.pyplot
- seaborn
- numpy
- sklearn.preprocessing
- sklearn.model_selection
- sklearn.metrics
- lightgbm
- sklearn.linear_model
- sklearn.ensemble
- catboost



### Общие выводы:
Была сделана предобработка данных, сделан разведочный анализ. Создали синтетические признаки с возрастом машины, средней стоимосью по марке машины.
Было протестировано 3 модели: Linear Regressor, Random Forest Regressor, Catboost Regressor. Лучшую метрику выдал Catboost.
На тестовых данных с помощью кросс валидации и гиперпараметрами max_depth = 10, была достигнула метрика MAPE 15.52.
Наиболее важными прзнаками оказались марка машины, пробег, год выпуска и средняя стоимость марки машины.
