import streamlit as st
import pandas as pd

@st.cache
def load_data():
    # Carica il file Excel (assicurati che "Viario.xlsx" si trovi nella stessa cartella)
    file_path = "Viario.xlsx"
    df = pd.read_excel(file_path, header=0)  
    # Se le intestazioni non sono corrette, puoi modificarle manualmente.
    # In questo esempio, assumiamo:
    # - colonna 0: Comune
    # - colonna 1: Località (o zona)
    # - colonna 2: Nome della via
    # - colonna 3: Tipo di via (es. "VIA")
    # - colonna 6: Intervallo civico/area (es. "12- A")
    return df

df = load_data()

st.title("Ricerca Voci del Viario")

# Crea un campo di testo per la ricerca del nome della via
query = st.text_input("Inserisci il nome della via")

if query:
    # Filtra le righe che contengono la stringa (case insensitive)
    mask = df.iloc[:,2].str.contains(query, case=False, na=False)
    risultati = df[mask]

    if not risultati.empty:
        # Creiamo le opzioni per il selectbox: ogni opzione è una stringa che combina
        # il nome della via, il tipo di via e l'intervallo civico/area.
        opzioni = risultati.apply(
            lambda row: f"{row.iloc[2]} ({row.iloc[3]}) - {row.iloc[6]}", axis=1
        ).tolist()

        scelta = st.selectbox("Seleziona la via corretta", opzioni)

        # Mostriamo a schermo i dettagli della riga selezionata
        # Per trovare la riga, confrontiamo la stringa generata
        riga_selezionata = risultati[
            risultati.apply(
                lambda row: f"{row.iloc[2]} ({row.iloc[3]}) - {row.iloc[6]}" == scelta, axis=1
            )
        ]
        st.subheader("Dettagli della via selezionata")
        st.write(riga_selezionata)
    else:
        st.write("Nessuna via trovata. Prova a digitare un altro nome.")
else:
    st.write("Digita il nome della via nel campo sopra per iniziare la ricerca.")
