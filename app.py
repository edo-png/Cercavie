import streamlit as st
import pandas as pd

@st.cache_data
def load_data():
    # Carica il file Excel "Viario.xlsx" dalla stessa cartella
    df = pd.read_excel("Viario.xlsx")
    return df

df = load_data()

st.title("Verifica Zona per Via e Numero Civico")

# Campo di ricerca per la via
via_query = st.text_input("Inserisci il nome della via:")

if via_query:
    # Filtra le righe in cui la colonna 'Via' contiene il testo inserito (ignora maiuscole/minuscole)
    filtered_df = df[df["Via"].str.contains(via_query, case=False, na=False)]
    
    if filtered_df.empty:
        st.write("Nessuna via trovata con questo nome.")
    else:
        # Creiamo una copia per evitare warning e generiamo una colonna 'descrizione'
        filtered_df = filtered_df.copy()
        filtered_df["descrizione"] = filtered_df.apply(
            lambda row: f'{row["Via"]} (dal {row["Dal civico"]} al {row["Al civico"]}, Zona: {row["Zona"]}, Comune: {row["Comune"]})',
            axis=1
        )
        opzioni = filtered_df["descrizione"].tolist()
        
        # Il widget selectbox mostra le opzioni filtrate in tempo reale
        scelta = st.selectbox("Suggerimenti per la via:", opzioni)
        
        # Estraiamo la riga selezionata
        selected_row = filtered_df[filtered_df["descrizione"] == scelta]
        
        st.subheader("Dettagli della via selezionata:")
        st.write(selected_row)
        
        # Inserimento del numero civico da verificare
        civico = st.number_input("Inserisci il numero civico:", min_value=0, value=0, step=1)
        
        if civico:
            row = selected_row.iloc[0]
            try:
                dal_civico = int(row["Dal civico"])
                al_civico = int(row["Al civico"])
            except ValueError:
                st.error("I valori per 'Dal civico' o 'Al civico' non sono numerici.")
            else:
                if dal_civico <= civico <= al_civico:
                    st.success(f"Il numero civico {civico} rientra nell'intervallo (dal {dal_civico} al {al_civico}). La Zona è: {row['Zona']} e il Comune: {row['Comune']}.")
                else:
                    st.warning(f"Il numero civico {civico} NON è compreso nell'intervallo (dal {dal_civico} al {al_civico}).")
else:
    st.write("Digita il nome della via per iniziare la ricerca.")
