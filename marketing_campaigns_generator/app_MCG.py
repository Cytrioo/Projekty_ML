#importy
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import Klastrowanie

##############################################################################################################################
#zmienne globalne
sept = ";"
df = None
Grupy = 1


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
    if format == 'xml':
        df = pd.read_xml(dane)
        return df



##############################################################################################################################
#strona

#Input 
#dane od uzytkownika
with st.sidebar:
    st.header("Informacje")
    st.markdown("Wybierz w jakim formacie przekazujesz dane")
    jak = st.selectbox("Format:", ["csv", "excel", "json", "xml"])
    if jak == "csv":
        sept = st.text_input("Podaj w jaki sposób są oddzielone dane.", value=sept)
    dane = st.file_uploader("Wybierz plik")
    if dane is not None:
        df = wczytaj_dane(dane, sept, jak)
    Grupy = int(st.text_input("Podaj jaką ilość grup docelową chcesz stworzyć:", value='4'))



#output
#Wyswietlenie danych
st.header("Twoje przesłane dane")
st.dataframe(df)

if df is not None:
    st.header("Wizualizacja klastra")
    MODEL = Klastrowanie.klastrowanie(df, Grupy)
    vis = Klastrowanie.wizualizacja(MODEL)
    if vis is not None:
        st.image(vis)