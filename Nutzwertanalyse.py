import streamlit as st
import pandas as pd
import altair as alt

# Definieren Sie die möglichen Standortfaktoren
faktoren = ["Lage", "Verkehrsanbindung", "Infrastruktur", "Steuern", "Umweltbestimmungen", "Subventionen",
            "Ressourcenverfügbarkeit", "Absatzmöglichkeiten", "Bildungs- und Qualifikationsniveau",
            "Öffentliche Infrastruktur", "Angebote im Bereich Freizeit und Kultur", "Konkurrenz",
            "Kooperationspartner"]

# Initialisieren Sie eine Session State-Variable für die neuen Faktoren und die Gewichtungen
if 'alle_faktoren' not in st.session_state:
    st.session_state.alle_faktoren = faktoren.copy()
if 'gewichtungen' not in st.session_state:
    st.session_state.gewichtungen = {faktor: 5 for faktor in faktoren}

# Eingabefeld zur Erweiterung der Faktorenliste
st.sidebar.header("Neue Standortfaktoren hinzufügen")
neuer_faktor = st.sidebar.text_input("Neuen Standortfaktor hinzufügen")
if st.sidebar.button("Faktor hinzufügen"):
    if neuer_faktor and neuer_faktor not in st.session_state.alle_faktoren:
        st.session_state.alle_faktoren.append(neuer_faktor)
        st.session_state.gewichtungen[neuer_faktor] = 5  # Standardgewichtung für neue Faktoren
        st.sidebar.success(f"Faktor '{neuer_faktor}' hinzugefügt!")
    else:
        st.sidebar.error("Faktor ist bereits vorhanden oder ungültig.")


# Funktion zum Löschen eines Faktors
def delete_faktor(faktor):
    if faktor in st.session_state.alle_faktoren:
        st.session_state.alle_faktoren.remove(faktor)
        del st.session_state.gewichtungen[faktor]


# Eingabefelder für die Gewichtungen der Faktoren
st.sidebar.header("Gewichtungen der Standortfaktoren")
for faktor in st.session_state.alle_faktoren:
    st.session_state.gewichtungen[faktor] = st.sidebar.slider(faktor, 0, 10, st.session_state.gewichtungen[faktor])

# Eingabefelder für die Standorte
st.header("Standorteingabe")
standorte = []
num_standorte = st.number_input("Anzahl der Standorte", 1, 5, 3)
for i in range(num_standorte):
    with st.expander(f"Standort {i + 1}"):
        standort_name = st.text_input(f"Name des Standortes {i + 1}", f"Standort {i + 1}")
        faktorenwerte = {}
        for faktor in st.session_state.alle_faktoren:
            cols = st.columns([4, 1])
            faktorenwerte[faktor] = cols[0].number_input(f"Wert für {faktor} in {standort_name}", 0, 10, 5)
            cols[1].markdown("<br>", unsafe_allow_html=True)
            if cols[1].button("Löschen", key=f"delete_{faktor}_{i}"):
                delete_faktor(faktor)
                st.experimental_rerun()
        standorte.append((standort_name, faktorenwerte))

# Button zur Durchführung der Nutzwertanalyse
if st.button("Nutzwertanalyse durchführen"):
    ergebnisse = []
    for standort_name, faktorenwerte in standorte:
        nutzwert = sum(
            faktorenwerte[faktor] * st.session_state.gewichtungen[faktor] for faktor in st.session_state.alle_faktoren)
        ergebnisse.append((standort_name, nutzwert))

    # Gewichtungen der Faktoren je Standort anzeigen
    gewichtungen_data = []
    for faktor in st.session_state.alle_faktoren:
        gewichtung_row = {"Faktor": faktor, "Gewichtung": st.session_state.gewichtungen[faktor]}
        for standort_name, faktorenwerte in standorte:
            gewichtung_row[standort_name] = faktorenwerte[faktor]
        gewichtungen_data.append(gewichtung_row)
    gewichtungen_df = pd.DataFrame(gewichtungen_data)
    st.header("Gewichtungen der Standortfaktoren je Standort")
    st.dataframe(gewichtungen_df)

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
