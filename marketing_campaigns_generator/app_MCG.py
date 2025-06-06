#importy
import pandas as pd
import streamlit as st
import os

from dotenv import dotenv_values
from openai import OpenAI

import Klastrowanie

##############################################################################################################################
#zmienne globalne
sept = ";"
df = None
Grupy = 1
MODEL_GPT = "gpt-4o-mini"

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
    CEL = st.text_area("Przedstaw swój cel kampanii reklamowej dla Twoich grup.")



#output
#Wyswietlenie danych
st.header("Twoje przesłane dane")
st.dataframe(df)

#Klastrowanie modelu
if df is not None:
    st.header("Wizualizacja klastra")
    MODEL = Klastrowanie.klastrowanie(df, Grupy)
    vis = Klastrowanie.wizualizacja(MODEL)
    if vis is not None:
        st.image(vis)

#Wyslanie klastra z pytaniem o nazwy grup
    if MODEL is not None and CEL is not None:
        env = dotenv_values(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '.env'))
        if env["OPENAI_API_KEY"] is not None:
            openai_client = OpenAI(api_key=env["OPENAI_API_KEY"])
        else:
            openai_client = st.text_input("Klucz API", type="password")
            MODEL_GPT = st.selectbox("Podaj model GPT:", ("gpt-4o-mini", "gpt-4o", "gpt-4.1", "gpt-4.1-mini"))
        
        if st.button('Generuj'):
            st.header("Proponowane nazwy dla grup oraz proponowana reklama")
            with st.spinner("Generuje grupy i reklame"):
                nazwy_grp = Klastrowanie.send_clu(MODEL, df, CEL, MODEL_GPT, openai_client)
                for nazwy in nazwy_grp:
                    st.markdown(nazwy_grp[nazwy]['nazwa'])
                    st.markdown(nazwy_grp[nazwy]['reklama'])
