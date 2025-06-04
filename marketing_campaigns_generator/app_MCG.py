#importy
import pandas as pd
import streamlit as st

##############################################################################################################################
#zmienne globalne
sept = ";"
df = None

##############################################################################################################################
#definicje
def wczytaj_dane(dane, s, format="csv"):
    if format == "csv":
        df = pd.read_csv(dane, sep=s)
        return df
    if format == "excel":
        df = pd.read_excel(dane)
        return df
    if format == "json":
        df = pd.read_json(dane)
        return df



##############################################################################################################################
#strona

#Imput
with st.sidebar:
    st.header("Informacje")
    st.markdown("Wybierz w jakim formacie przekazujesz dane")
    jak = st.selectbox("Format:", ["csv", "excel", "json"])
    if jak == "csv":
        sept = st.text_input("Podaj w jaki sposób są oddzielone dane.", value=';')
    dane = st.file_uploader("Wybierz plik")
    if dane is not None:
        df = wczytaj_dane(dane, sept, jak)

#output
st.header("Twoje przesłane dane")
st.dataframe(df)