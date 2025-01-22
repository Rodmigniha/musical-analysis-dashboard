import pandas as pd

def preprocess_data(data):
    """Effectue les étapes de prétraitement nécessaires sur le dataset."""
    # Suppression des lignes avec des valeurs manquantes
    data.dropna(inplace=True)
    
    # Conversion des colonnes nécessaires au bon format
    data['popularity'] = pd.to_numeric(data['popularity'], errors='coerce')
    data['duration_ms'] = pd.to_numeric(data['duration_ms'], errors='coerce')
    
    return data
