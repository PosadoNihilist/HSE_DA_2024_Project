import streamlit as st
import plotly.express as px
import pandas as pd
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')

#streamlit run dashboard.py <- как запустить 

st.set_page_config(page_title="Recipes",layout="wide")

st.title("Recipes")
st.divider()

df = pd.read_csv('./my_all_recipes.csv')

st.sidebar.header("Choose your filter: ") #Фильтрует по источнику данных
source = st.sidebar.multiselect("Which source", df['source'].unique())
if not source:
    df2 = df.copy()
else:
    df2 = df[df['source'].isin(source)]

how_much_time = st.sidebar.slider("Max cooking time (in minutes)", min_value=0, max_value=1440, step=10, value=1440) #Фильтрует максимальному времени приготовления в минутах

if not how_much_time:
    df3 = df2.copy()
else:
    df3 = df2[df2['total_time_minutes']<=how_much_time]

top_how_many = st.sidebar.slider("How many top ingredients?", min_value=1, max_value=30, step=1, value=10) #Сколько топ ингрилиентов показывать

col1, col2 = st.columns(2)


col1.markdown("## Most common ingredients") #Топ самых частых ингридиентов

fig1 = px.bar(df3['ingredient_name'].value_counts().reset_index()[:top_how_many], x='ingredient_name', y='count')
col1.plotly_chart(fig1)


col2.markdown("## What %  of recipes have this ingredient?") #Сколько рецептов с этим ингридиентом,

df4 = df3['ingredient_name'].value_counts().reset_index()
df4['count'] = (df4['count']/len(df3['url'].unique()))

fig2 = px.bar(df4[:top_how_many], x='ingredient_name', y='count')
col2.plotly_chart(fig2)


col1.markdown("## What % of ingredients are the top x ingredients?") #Отношение частоты топ х ингридиентов ко всем остальным ингридиентам 

how_many_ingredients_adding = col1.slider("How many ingredients on the left?", min_value=0, max_value=200, step=10, value=10)

df5 = df3['ingredient_name'].value_counts().reset_index()
df5 = df3['ingredient_name'].value_counts().reset_index()
sum_table = pd.DataFrame({
    'names':['Top x ingredients', 'All other ingredients'],
    'top ingredients': [df5[:how_many_ingredients_adding]['count'].sum()/df5['count'].sum(), df5[how_many_ingredients_adding:]['count'].sum()/df5['count'].sum()]
})
fig3 = px.bar(sum_table, x='names', y='top ingredients')
col1.plotly_chart(fig3)

#список со специями
spices = [
    'allspice', 'anise','bay leaf','basil','bergamot','black pepper','caraway','cardamom','cayenne pepper', 'chili pepper',
    'chives','cilantro','cinnamon','clove','coriander','cumin','curry','dill','fennel','garlic powder','ginger','horseradish',
    'lavender','lemon balm','lemon grass','licorice','mace','nutmeg','oregano','onion powder','paprika',
    'parsley','peppermint','poppy seed','rosemary','rue','saffron','sage','savory','sesame','sorrel','star anise','spearmint','tarragon','thyme',
    'tumeric','vanilla','wasabi', 'mustard'
]

spices_regex = r"|".join(spices)
recipes_with_spices = df3.loc[df3['ingredient_name'].str.contains(spices_regex).fillna(False)]


col2.markdown("## What are the top spices?") #топ специи

how_many_spices = col2.slider("How many top spices?", min_value=0, max_value=49, step=1, value=10)
fig4 = px.bar(recipes_with_spices['ingredient_name'].value_counts().reset_index()[:how_many_spices], x='ingredient_name', y='count')
col2.plotly_chart(fig4)


col1.markdown("## How do spices correlate?") #корреляции топ 20 специй

common_spices = set(recipes_with_spices['ingredient_name'].value_counts().head(20).index)
spices_count = recipes_with_spices.groupby("url", as_index=False).agg(spices_count=("ingredient_name", "count"), url=("url", "first"), )
recipes_with_spices_with_count = recipes_with_spices.merge(spices_count, on="url")
multi_spice_recipes = recipes_with_spices_with_count.loc[recipes_with_spices_with_count["spices_count"] > 1]
common_multi_spice_recipes = multi_spice_recipes[multi_spice_recipes['ingredient_name'].isin(common_spices)]
dummy = pd.get_dummies(common_multi_spice_recipes,columns=["ingredient_name"],prefix='',prefix_sep='').groupby(['url'], as_index=False).max(numeric_only = True )
spice_corr = dummy.drop(columns=multi_spice_recipes.columns, errors="ignore")
corr = spice_corr.corr()

fig5 = px.imshow(corr)
col1.plotly_chart(fig5)


col2.markdown("## How do ingredients correlate?") #корреляция топ 20 ингридиентов

common_ingredients = set(df3['ingredient_name'].value_counts().head(20).index)
ingredient_count = df3.groupby("url", as_index=False).agg(ingredient_count=("ingredient_name", "count"), url=("url", "first"), )
df3_with_count = df3.merge(ingredient_count, on="url")
multi_ingredient_recipes = df3_with_count.loc[df3_with_count["ingredient_count"] > 1]
common_multi_ingredient_recipes = multi_ingredient_recipes[multi_ingredient_recipes['ingredient_name'].isin(common_ingredients)]

dummy = pd.get_dummies(common_multi_ingredient_recipes,columns=["ingredient_name"],prefix='',prefix_sep='').groupby(['url'], as_index=False).max(numeric_only = True )
ingredient_corr = dummy.drop(columns=multi_ingredient_recipes.columns, errors="ignore")
corr_2 = ingredient_corr.corr()
fig6 = px.imshow(corr_2)
col2.plotly_chart(fig6)