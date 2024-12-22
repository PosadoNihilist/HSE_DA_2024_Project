# Проект

## Описание

Проект состоит из двух основных частей, сбор данных (AD_project_data.ipynb) и дэшборд (dashboard.py).

### Сбор данных

Первый файл собирает данные в один датафрейм. Берутся данные из трех мест:

1. Датасет enriched-recipes.json. 

Ссылка на датасет: https://github.com/wcedmisten/foodFinder/

2. Русский датасет all-recipes.csv собранный мной в прошлом задании

Ссылка на датасет: https://github.com/PosadoNihilist/HSE_DA_2024_HW2

3. Данные собранные с сайта https://www.recipetineats.com/category/main-dishes/

Получившийся датасет находится в папке как my_all_recipes.csv

### Дэшборд

Файл dashboard.py открывает локальный сайт, показывающий информацию про итоговый датасет. Можно фильтровать по источнику данных (enriched-recipes.json это allrecipes, русский датасет это russian, с сайта recipetineats это recipetineats). Для запуска нужно в консоле написать streamlit run dashboard.py

## Выводы

1. Фильтрование по максимальному времени готовки вообще почти не на что не влияет
2. Самые популярные ингридиенты: Соль, Сахар, Масло, Лук, и Яйца. Если брать только русские рецепты (где в основном дессерты и выпечка), топ 5: Сахар, Яйца, Пшеничная Мука, Масло, Соль. Только recipetineats (где основные блюда), топ 5: Чеснок, Соль, Лук, Оливковое Масло, Черный перец.
3. Если брать только русские рецепты или только рецепты recipetineats, самые популярные ингридиенты могут встречаются больше, чем всего рецептов. Это объясняется тем, что в каждом рецепте могло идти разделение ингридиентов, например дополнительный сегмент для соуса или крема или украшения. Тогда этот ингридиент считался несколько раз в одном рецепте.
4. Топ 100 ингридиентов покрывают 80% всех использованных ингридиентов. Так как всего 31300 уникальных ингридиентов, получается 0.3% всех уникальных ингридиентов используюися 80% раз. 
5. Топ 5 популярных специй: Ваниль, Черный перец, Корица, Петрушка, и Горчица. Если брать только русские, топ 5: Ванильнь, Черный перец, Корица, Мак, Укроп. Только recipetineats: Черный перец, Пертушка, Тимьян, Кинза, Кумин.
6. Лучше всего из специй коррелируют Корица и Ваниль, Корица и Мускатный орех, Корица и Гвоздика. 
7. Лучше всего из ингридиентов коррелируют Мука и Разрыхлитель, Мука и Яица, Сахар и Мука.