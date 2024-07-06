import streamlit as st
import pandas as pd

# Fonction pour charger le fichier Excel
def load_data(file):
    df = pd.read_excel(file)
    return df

# Fonction pour calculer les statistiques pour un mnémo diversité spécifique
def calculate_statistics(df, mnemo):
    filtered_df = df[df['Niveau intervenant'] == 'Fabrication 2']
    mnemo_df = filtered_df[filtered_df['Mnémo diversité'] == mnemo]
    
    if mnemo_df.empty:
        return None

    stats = {
        'Fréquence d\'arrêt': mnemo_df['Frequence d\'arrêt'].sum(),
        'Temps de bloquage moyen': mnemo_df['Temps de bloquage'].mean(),
        'Temps de bloquage min': mnemo_df['Temps de bloquage'].min(),
        'Temps de bloquage max': mnemo_df['Temps de bloquage'].max(),
        'Module le plus fréquent': mnemo_df['Module'].mode().iloc[0],
        'Code d\'arrêt le plus fréquent': mnemo_df['Code d\'arrêt'].mode().iloc[0],
        'Zone la plus fréquente': mnemo_df['Zone'].mode().iloc[0],
        'Type le plus fréquent': mnemo_df['Type'].mode().iloc[0],
        'Cause la plus fréquente': mnemo_df['Cause'].mode().iloc[0],
    }

    return stats

# Interface utilisateur avec Streamlit
st.title('Carte d\'identité des mnémo diversité')

uploaded_file = st.file_uploader("Choisissez un fichier Excel", type="xlsx")

if uploaded_file:
    df = load_data(uploaded_file)
    st.write("Fichier chargé avec succès")
    
    mnemo = st.text_input("Entrez le nom du mnémo diversité")

    if mnemo:
        stats = calculate_statistics(df, mnemo)

        if stats:
            st.write(f"**Carte d'identité pour le mnémo diversité '{mnemo}':**")
            for key, value in stats.items():
                st.write(f"{key}: {value}")
        else:
            st.write(f"Aucune donnée trouvée pour le mnémo diversité '{mnemo}'")
