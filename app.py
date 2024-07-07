
import streamlit as st
import pandas as pd

# Function to load the Excel file and identify the row where the table starts
def load_data(file):
    xls = pd.ExcelFile(file)
    sheet_name = 'Smp99_Donnees'  # Change this to the correct sheet name if needed
    df = pd.read_excel(file, sheet_name=sheet_name, engine='openpyxl', header=None)
    header_row_index = None
    for i, row in df.iterrows():
        if 'Niveau intervenant' in row.values and 'Mnémo diversité' in row.values:
            header_row_index = i
            break
    if header_row_index is not None:
        df = pd.read_excel(file, sheet_name=sheet_name, engine='openpyxl', skiprows=header_row_index)
        return df
    else:
        return None

# Function to calculate statistics for a specific 'Mnémo diversité'
def calculate_statistics(df, mnemo):
    mnemo_df = df[df['Mnémo diversité'] == mnemo]
    
    if mnemo_df.empty:
        return None

    stats = {
        'Fréquence': mnemo_df['Mnémo diversité'].count(),
        'Durée moyenne de blocage': mnemo_df['Durée'].mean(),
        'Durée maximale de blocage': mnemo_df['Durée'].max(),
        'Durée minimale de blocage': mnemo_df['Durée'].min(),
        'Zone la plus fréquente': mnemo_df['Zone'].value_counts().idxmax(),
        'Module le plus fréquent': mnemo_df['Module'].value_counts().idxmax(),
        'Module détecté le plus fréquent': mnemo_df['Module détecté'].value_counts().idxmax(),
        'Module déclaré le plus fréquent': mnemo_df['Module déclaré'].value_counts().idxmax(),
        'Cause la plus fréquente': mnemo_df['Cause'].value_counts().idxmax(),
        'Code d\'arrêt le plus fréquent': mnemo_df['Code arrêt'].value_counts().idxmax(),
        'Famille d\'arrêts la plus fréquente': mnemo_df['Famille d\'arrêts'].value_counts().idxmax(),
        'Sous famille d\'arrêts la plus fréquente': mnemo_df['Sous famille d\'arrêts'].value_counts().idxmax(),
    }

    return stats

# Streamlit User Interface
st.title('Carte d\'identité des mnémo diversité')

uploaded_file = st.file_uploader("Choisissez un fichier Excel", type="xlsx")

if uploaded_file:
    df = load_data(uploaded_file)
    
    if df is not None:
        # Display column names
        st.write("Noms des colonnes :", df.columns.tolist())
        
        # Clean column names by stripping leading and trailing spaces
        if all(isinstance(col, str) for col in df.columns):
            df.columns = [col.strip() for col in df.columns]
        
        st.write("Fichier chargé avec succès")
        
        # Select 'Niveau intervenant'
        niveau_intervenant_values = df['Niveau intervenant'].unique().tolist()
        selected_niveau_intervenant = st.selectbox("Choisissez le niveau intervenant", niveau_intervenant_values)
        
        # Filter data by 'Niveau intervenant'
        filtered_df = df[df['Niveau intervenant'] == selected_niveau_intervenant]
        
        # Select 'Mnémo diversité'
        mnemo_diversite_values = filtered_df['Mnémo diversité'].unique().tolist()
        selected_mnemo_diversite = st.selectbox("Choisissez le mnémo diversité", mnemo_diversite_values)
        
        if selected_mnemo_diversite:
            stats = calculate_statistics(filtered_df, selected_mnemo_diversite)

            if stats:
                st.write(f"**Carte d'identité pour le mnémo diversité '{selected_mnemo_diversite}':**")
                for key, value in stats.items():
                    st.write(f"{key}: {value}")
            else:
                st.write(f"Aucune donnée trouvée pour le mnémo diversité '{selected_mnemo_diversite}'")
    else:
        st.error("Impossible de trouver la ligne de colonne 'Niveau intervenant' et 'Mnémo diversité'. Veuillez vérifier le fichier.")


