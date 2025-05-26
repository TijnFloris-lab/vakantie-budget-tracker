import streamlit as st
import pandas as pd
import datetime
import os

st.set_page_config(page_title="Vakantie Budget Tracker", layout="wide")

st.title("\U0001F3D6️ Vakantie Budget Tracker")

# Invoer vakantie-instellingen
with st.sidebar:
    st.header("Instellingen")
    start_datum = st.date_input("Startdatum", datetime.date.today())
    aantal_dagen = st.number_input("Aantal dagen", min_value=1, max_value=365, value=14)
    dagbudget = st.number_input("Dagbudget (€)", min_value=0.0, value=100.0, step=1.0)

# Laad eerder opgeslagen uitgaven indien aanwezig
csv_file = "vakantie_uitgaven.csv"
if os.path.exists(csv_file):
    st.session_state.uitgaven = pd.read_csv(csv_file).to_dict(orient="records")

# Session state voor uitgaven
if "uitgaven" not in st.session_state:
    st.session_state.uitgaven = []

# Invoer uitgaven
st.subheader("💸 Uitgave invoer")
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    datum = st.date_input("Datum", datetime.date.today())
with col2:
    hotel = st.number_input("Hotel", min_value=0.0, step=1.0)
with col3:
    eten = st.number_input("Eten", min_value=0.0, step=1.0)
with col4:
    transport = st.number_input("Transport", min_value=0.0, step=1.0)
with col5:
    activiteiten = st.number_input("Activiteiten", min_value=0.0, step=1.0)

if st.button("➕ Toevoegen"):
    nieuwe_uitgave = {
        "Datum": datum,
        "Hotel": hotel,
        "Eten": eten,
        "Transport": transport,
        "Activiteiten": activiteiten,
        "Totaal": hotel + eten + transport + activiteiten
    }
    st.session_state.uitgaven.append(nieuwe_uitgave)
    pd.DataFrame(st.session_state.uitgaven).to_csv(csv_file, index=False)
    st.success("Uitgave toegevoegd en opgeslagen!")

# Toon tabel
if st.session_state.uitgaven:
    df = pd.DataFrame(st.session_state.uitgaven).sort_values("Datum")
    st.subheader("📊 Overzicht uitgaven")
    st.dataframe(df, use_container_width=True)

    # Berekeningen
    totaal_uitgegeven = df["Totaal"].sum()
    ingevoerde_dagen = df["Datum"].nunique()
    resterende_dagen = max(aantal_dagen - ingevoerde_dagen, 0)
    nog_besteedbaar = dagbudget * aantal_dagen - totaal_uitgegeven
    nieuw_gemiddelde = nog_besteedbaar / resterende_dagen if resterende_dagen > 0 else 0

    st.markdown("""
    ### 📈 Statistieken
    - **Totaal uitgegeven:** €{:.2f}  
    - **Nog te besteden:** €{:.2f}  
    - **Nieuw daggemiddelde:** €{:.2f} (voor {} resterende dagen)
    """.format(totaal_uitgegeven, nog_besteedbaar, nieuw_gemiddelde, resterende_dagen))
else:
    st.info("Voer eerst uitgaven in om overzicht te zien.")
