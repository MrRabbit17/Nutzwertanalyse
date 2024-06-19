import streamlit as st
import pandas as pd
import os
import altair as alt
import subprocess

# Definieren Sie die möglichen Standortfaktoren
faktoren = ["Lage", "Verkehranbindung", "Infrastruktur", " Steuern", "Umweltbestimmungen", " Subventionen",
            "Ressourcenverfügbarkeit", " Absatzmöglichkeiten", "Bildungs- und Qualifikationsniveau",
            "Öffentliche Infrastruktur", " Angebote im Bereich Freizeit und Kultur", "Konkurrenz",
            "Kooperationspartner"]

# Initialisieren Sie eine Session State-Variable für die neuen Faktoren
if 'neue_faktoren' not in st.session_state:
    st.session_state.neue_faktoren = []

# Eingabefeld zur Erweiterung der Faktorenliste
st.sidebar.header("Neue Standortfaktoren hinzufügen")
neuer_faktor = st.sidebar.text_input("Neuen Standortfaktor hinzufügen")
if st.sidebar.button("Faktor hinzufügen"):
    if neuer_faktor and neuer_faktor not in faktoren and neuer_faktor not in st.session_state.neue_faktoren:
        st.session_state.neue_faktoren.append(neuer_faktor)
        st.sidebar.success(f"Faktor '{neuer_faktor}' hinzugefügt!")
    else:
        st.sidebar.error("Faktor ist bereits vorhanden oder ungültig.")

# Alle Faktoren zusammenführen
alle_faktoren = faktoren + st.session_state.neue_faktoren

# Eingabefelder für die Gewichtungen der Faktoren
gewichtungen = {}
st.sidebar.header("Gewichtungen der Standortfaktoren")
for faktor in alle_faktoren:
    gewichtungen[faktor] = st.sidebar.slider(faktor, 0, 10, 5)

# Eingabefelder für die Standorte
st.header("Standorteingabe")
standorte = []
num_standorte = st.number_input("Anzahl der Standorte", 1, 5, 3)
for i in range(num_standorte):
    with st.expander(f"Standort {i + 1}"):
        standort_name = st.text_input(f"Name des Standortes {i + 1}", f"Standort {i + 1}")
        faktorenwerte = {}
        for faktor in alle_faktoren:
            faktorenwerte[faktor] = st.number_input(f"Wert für {faktor} in {standort_name}", 0, 10, 5)
        standorte.append((standort_name, faktorenwerte))

# Button zur Durchführung der Nutzwertanalyse
if st.button("Nutzwertanalyse durchführen"):
    ergebnisse = []
    for standort_name, faktorenwerte in standorte:
        nutzwert = sum(faktorenwerte[faktor] * gewichtungen[faktor] for faktor in gewichtungen)
        ergebnisse.append((standort_name, nutzwert))

    # Ergebnis anzeigen
    ergebnisse_df = pd.DataFrame(ergebnisse, columns=["Standort", "Nutzwert"])
    st.header("Ergebnisse der Nutzwertanalyse")
    st.dataframe(ergebnisse_df)

    # Bar chart with custom color
    chart = alt.Chart(ergebnisse_df).mark_bar(color='#8B0000').encode(
        x='Standort:O',
        y='Nutzwert:Q'
    ).properties(
        width=alt.Step(80)  # bar width
    )
    st.altair_chart(chart, use_container_width=True)