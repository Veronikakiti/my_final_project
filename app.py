import streamlit as st
import matplotlib.pyplot as plt
import mpld3
import streamlit.components.v1 as components
from PIL import Image
from data import *

st.set_page_config(
    page_title='Анализ уровня заработных плат в России',
    layout='wide'
)
connection = st.connection("postgresql", type="sql")


st.header('Среднемесячная номинальная заработная плата по 3 видам экономической деятельности за 2000-2023 гг.', anchor='salaries')

df_salaries = get_salaries(connection)
st.dataframe(df_salaries)

st.write('**Динамика изменения номинальных зарплат**')
st.write('Графики можно масштабировать')
years = df_salaries['year']

construction = df_salaries['construction']
fig = plt.figure()
plt.plot(years, construction, marker='o')
plt.title('Динамика изменения зарплат в сфере строительства')
plt.xlabel('Год')
plt.ylabel('НЗП, рублей')

fig_html = mpld3.fig_to_html(fig)
components.html(fig_html, height=600)


finance = df_salaries['cinance']
fig = plt.figure()
plt.plot(years, finance, marker='o', color='orange')
plt.title('Динамика изменения зарплат в сфере финансов и страхования')
plt.xlabel('Год')
plt.ylabel('НЗП, рублей')

fig_html = mpld3.fig_to_html(fig)
components.html(fig_html, height=600)


education = df_salaries['education']
fig = plt.figure()
plt.plot(years, education, marker='o', color='green')
plt.title('Динамика изменения зарплат в сфере образования')
plt.xlabel('Год')
plt.ylabel('НЗП, рублей')

fig_html = mpld3.fig_to_html(fig)
components.html(fig_html, height=600)


st.write('Можете посмотреть изменения зарплат по всем 3 видам экономической деятельности:')

fig = plt.figure(figsize=(10, 5))
plt.title('Динамика изменения НЗП по видам деятельности')
plt.plot(years, construction, marker='.', label='Строительство')
plt.plot(years, finance, marker='.', label='Финансы и страхование')
plt.plot(years, education, marker='.', label='Образование')

plt.xlabel('Год')
plt.ylabel('НЗП, рублей')
plt.legend(loc=2)

fig_html = mpld3.fig_to_html(fig)
components.html(fig_html, height=600)


st.write('''
**Выводы**: 

* По всем видам деятельности наблюдается положительная динамика изменения уровня номинальных заработных плат.
* Самый высокий уровень НЗП в сфере финансов и страхования, а самый низкий - в образовании.
* Уровень НЗП в сфере строительства практически совпадает с уровнем НЗП в образовании и показывает схожую динамику. При этом в финансовой и страховой деятельности наблюдается сильный рост НЗП.
''')


st.header('Уровень инфляции за 2000-2023 гг.', anchor='inflation')

df_inflation = get_inflation(connection)
st.dataframe(df_inflation)


st.header('Среднемесячная реальная заработная плата по 3 видам экономической деятельности за 2000-2023 гг.', anchor='salaries-real')

df_salaries_real = get_salaries_real(connection)
st.dataframe(df_salaries_real)

st.write('**Сравнение уровня номинальной и реальной заработной платы**')

years = df_salaries_real['year']

construction_real = df_salaries_real['construction']
fig = plt.figure(figsize=(6, 3))
plt.plot(years, construction, marker='o', label='НЗП, рублей')
plt.plot(years, construction_real, marker='o', label='РЗП, рублей', color='lightblue')
plt.title('Строительство')
plt.legend(loc=2)
plt.grid()
st.pyplot(fig)

finance_real = df_salaries_real['finance']
fig = plt.figure(figsize=(6, 3))
plt.plot(years, finance, marker='o', label='НЗП, рублей', color='red')
plt.plot(years, finance_real, marker='o', label='РЗП, рублей', color='orange')
plt.title('Финансы и страхование')
plt.legend(loc=2)
plt.grid()
st.pyplot(fig)

education_real = df_salaries_real['education']
fig = plt.figure(figsize=(6, 3))
plt.plot(years, education, marker='o', label='НЗП, рублей', color='green')
plt.plot(years, education_real, marker='o', label='РЗП, рублей', color='lightgreen')
plt.title('Образование')
plt.legend(loc=2)
plt.grid()
st.pyplot(fig)

st.write('**Выводы:** по всем видам деятельности размер реальных заработных плат ниже уровня номинальных. '
         'В период с 2000 по 2008 гг. уровень номинальной и уровень реальной зарплаты в сфере строительства и финансов находятся практически на одном уровне. '
         'В сфере образования такая тенденция сохраняется до 2013 г. '
         'В 2015 г. наблюдается большой разрыв в уровне зарплат по всем 3 областям. '
         'В последующие годы РЗП продолжает расти, как и НЗП, но тем не менее сохраняется разрыв между ними.')


st.header('Анализ влияния инфляции на изменение уровня заработной платы по сравнению с предыдущим годом', anchor='inflation-influence')

df_inflation_influence = get_inflation_influence(connection)
st.dataframe(df_inflation_influence)

st.write('Отобразим график влияния инфляции на изменение реальной заработной платы по сравнению с предыдущим годом')

fig = plt.figure(figsize=(8, 4))

years = df_inflation_influence['year']

construction_real_index = df_inflation_influence['construction_real_salary_index']
finance_real_index = df_inflation_influence['finance_real_salary_index']
education_real_index = df_inflation_influence['education_real_salary_index']


plt.plot(years, construction_real_index, marker='.', label='Строительство')
plt.plot(years, finance_real_index, marker='.', label='Финансы и страхование')
plt.plot(years, education_real_index, marker='.', label='Образование')

plt.title('Динамика влияния инфляции на изменение реальной заработной платы (%)')
plt.xlabel('Год')
plt.ylabel('ИРЗП %')
plt.legend(loc=9)
plt.grid()
st.pyplot(fig)

st.write('**Выводы**: В начале рассматриваемого периода наблюдается высокий уровень ИРЗП. '
         'Это значит, что уровень РЗП значительно вырос по сравнению с предыдущим годом. '
         'В сфере строительства и финансов резкое снижение ИРЗП произошло в 2004 г., а в области образования - в 2003 г.'
         'В 2005-2008 гг. отмечается рост уровня РЗП на 20-30% во всех видах деятельности. '
         'В 2009-2010 гг. РЗП увеличилась незначительно, поэтому наблюдается резкий спад ИРЗП. '
         'В то время как с 2010 по 2015 гг. ИРЗП в строительстве и финансовой сфере снижается, в сфере образования можно наблюдать рост показателя. '
         'В 2016 г. можно увидеть резкое увеличение уровня РЗП по сравнению с предыдущим годом. '
         'Далее значение ИРЗП сохраняется на уровне 5-15% и к 2023 году достигает 120%.')


with st.sidebar:
    image = Image.open('increase_chart.jpg')
    st.image(image, width=280)

    st.subheader('Содержание')
    st.markdown(':credit_card: [Номинальная заработная плата](#salaries)')
    st.markdown(':bank: [Инфляция](#inflation)')
    st.markdown(':bar_chart: [Реальная заработная плата](#salaries-real)')
    st.markdown(':chart_with_upwards_trend: [Влияние инфляции](#inflation-influence)')