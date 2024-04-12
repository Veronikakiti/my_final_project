import streamlit as st
import pandas as pd

@st.cache_data
def get_salaries(_connection):
    result = _connection.query("SELECT * FROM salaries.salaries")
    return pd.DataFrame(result)

@st.cache_data
def get_salaries_real(_connection):
    result = _connection.query("SELECT * FROM salaries.salaries_real")
    return pd.DataFrame(result)

@st.cache_data
def get_inflation(_connection):
    result = _connection.query("SELECT * FROM salaries.inflation")
    return pd.DataFrame(result)

@st.cache_data
def get_inflation_influence(_connection):
    result = _connection.query("SELECT * FROM salaries.inflation_influence")
    return pd.DataFrame(result)